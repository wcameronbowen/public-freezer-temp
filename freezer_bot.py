from machine import Pin
from time import sleep
import onewire, ds18x20, network, umail
import urequests as requests
import secrets

def check_temp():
    ow = onewire.OneWire(Pin(2))
    ds = ds18x20.DS18X20(ow)
    roms = ds.scan()
    ds.convert_temp()
    sleep(1)
    for rom in roms:
        return ds.read_temp(rom)
    
def connect(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

def send_email(smtp):
    connect(secrets.var_ssid, secrets.var_password)
    
    for email in smtp['recipient_email']:
        s = umail.SMTP('smtp.gmail.com', 465, ssl=True)
        s.login(smtp["sender_email"], smtp["sender_app_password"])
        s.to(email)

        # Write the email header
        s.write(f"From:{smtp['sender_name']}<{smtp['sender_email']}" + ">\n")
        s.write(f"Subject:{smtp['email_subject']}" + "\n")
        # Write the body of the email
        s.write("Test Email from Raspberry Pi Pico W")

        # Send the email
        s.send()
        # Quit the email session
        s.quit()

def send_sms(sms, message):
    connect(secrets.var_ssid, secrets.var_password)

    for number in sms['recipient_num']:  
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = f"To={number}&From={sms['sender_num']}&Body={message}"
        url = f"https://api.twilio.com/2010-04-01/Accounts/{sms['account_sid']}/Messages.json"

        print("Trying to send SMS with Twilio")

        response = requests.post(url,
                                 data=data,
                                 auth=(sms["account_sid"],sms["auth_token"]),
                                 headers=headers)

        if response.status_code == 201:
            print("SMS sent!")
        else:
            print(f"Error sending SMS: {response.text}")

        response.close()


while True:
    x = check_temp()
    #y = check_voltage()
    print(x)
    if x > 30.0:
        message = f"temp is {x}"
        print(message)
        #send_email(secrets.var_smtp)
        #send_sms(secrets.var_sms, message)
    # if y < 5.0:
    #     message = f"voltage is {y}"
    #     print(message)
    #     #send_email(secrets.var_smtp)
    #     #send_sms(secrets.var_sms, message)
    sleep(5)
