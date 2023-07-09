from machine import Pin, ADC
from time import sleep
import onewire, ds18x20, network, umail, random, utime
import urequests as requests
import secrets

def check_temp():
    ow = onewire.OneWire(Pin(28))
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

def send_email(smtp, message):
    connect(secrets.var_ssid, secrets.var_password)
    
    for email in smtp['recipient_email']:
        s = umail.SMTP('smtp.gmail.com', 465, ssl=True)
        s.login(smtp["sender_email"], smtp["sender_app_password"])
        s.to(email)

        # Write the email header
        s.write(f"From:{smtp['sender_name']}<{smtp['sender_email']}" + ">\n")
        s.write(f"Subject:{smtp['email_subject']}" + "\n")
        # Write the body of the email
        s.write(message)

        # Send the email
        s.send()
        print("Email sent!")
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

def check_power():
    # This example shows how to read the voltage from a LiPo battery connected to a Raspberry Pi Pico via our Pico Lipo SHIM
    # and uses this reading to calculate how much charge is left in the battery.
    # pico w requires setting pin 25 to high in order to measure vsys on ping 29 
    #Pin(25, mode=Pin.OUT, pull=Pin.PULL_DOWN).high()

    #vsys = ADC(29)                      # reads the system input voltage
    charging = Pin('WL_GPIO2', Pin.IN)
    #conversion_factor = 3 * 3.3 / 65535
    
    full_battery = 4.2                  # these are our reference voltages for a full/empty battery, in volts
    empty_battery = 3.0                 # the values could vary by battery size/manufacturer so you might need to adjust them
    
    # convert the raw ADC read into a voltage, and then a percentage
    #voltage = vsys.read_u16() * conversion_factor
    voltage = get_vsys()
    percentage = 100 * ((voltage - empty_battery) / (full_battery - empty_battery))
    if percentage > 100:
        percentage = 100.00
    
    return charging.value(),percentage
    # if it's plugged into battery, show true
    # if charging.value() == 1:
    #     print("battery is charging") 
    #     return charging.value(),percentage
    # # if not charging show battery capacity
    # else:
    #     print("battery is not charging")
    #     print(voltage, "v", percentage, "%")
    #     return charging.value(),percentage

def get_vsys():
    # Make sure pin 25 is high.
    # This seems to be critical to getting accurate values.
    Pin(25, mode=Pin.OUT, pull=Pin.PULL_DOWN).high()
        
    # Reconfigure pin 29 as an input.
    Pin(29, Pin.IN)
        
    sample_count = 10
    battery_voltage = 0
    for _ in range(sample_count):
      battery_voltage += _read_vsys_voltage()
    return round( battery_voltage / sample_count, 2)
    #set_pad(29, old_pad)

    # Restore the pin state and possibly reactivate WLAN
    # Pin(29, Pin.ALT, pull=Pin.PULL_DOWN, alt=7)

def _read_vsys_voltage():
  adc_Vsys = machine.ADC(3)
  ADC_VOLT_CONVERSATION = 3.3 / 65535
  return adc_Vsys.read_u16() * 3.0 * ADC_VOLT_CONVERSATION

def write_to_file(fileid, temp):
    led = Pin('WL_GPIO0', Pin.OUT)
    file = open(str(fileid) + '-tempdata.txt', 'w')
    led.value(1)
    file.write(str(temp) + ',')
    file.flush()
    led.value(0)


fileid = random.randrange(10000)
while True:
    #write_to_file(fileid, 5)
    x = check_temp()
    c,p = check_power()
    message = ""
    if c == 1:
        print(f"battery is charging, at {p}%")
        message = f"temp is {x}, battery is charging, capacity is {p}%"
    else:
        print(f"battery is not charging at {p}%")
        message = f"temp is {x}, battery is not charging, capacity is {p}%"
    print(message)
    #send_sms(secrets.var_sms, message)
    send_email(secrets.var_smtp, message)
    #x = check_temp()
    #y = check_voltage()
    #print(x)
    #if x > 30.0:
    #    message = f"temp is {x}"
    #    print(message)
        #send_email(secrets.var_smtp)
        #send_sms(secrets.var_sms, message)
    # if y < 5.0:
    #     message = f"voltage is {y}"
    #     print(message)
    #     #send_email(secrets.var_smtp)
    #     #send_sms(secrets.var_sms, message)
    sleep(60)