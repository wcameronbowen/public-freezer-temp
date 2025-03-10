from machine import Pin, ADC, reset
from utime import sleep
import onewire, ds18x20, network, umail, random
import urequests as requests
import secrets

def check_temp():
    try:
        ow = onewire.OneWire(Pin(28))
        ds = ds18x20.DS18X20(ow)
        roms = ds.scan()
        ds.convert_temp()
        sleep(1)
        for rom in roms:
            return ds.read_temp(rom)
    except Exception:
        print("error reading temp")
        return 999

def connect(ssid, password):
    led.value(1)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    led.value(0)
    return ip

def send_email(smtp, message):
    connect(secrets.var_ssid, secrets.var_password)

    for email in smtp['recipient_email']:
        s = umail.SMTP('smtp.gmail.com', 465, ssl=True)
        s.login(smtp["sender_email"], smtp["sender_app_password"])
        s.to(email)

        s.write(f"From:{smtp['sender_name']}<{smtp['sender_email']}" + ">\n")
        s.write(f"Subject:{smtp['email_subject']}" + "\n")
        s.write(message)

        s.send()
        print("Email sent!")
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
    # This is specific to reading voltage from a LiPo battery connected to a Raspberry Pi Pico W via Pico Lipo SHIM
    # and uses this reading to calculate how much charge is left in the battery.
    # pico w requires setting pin 25 to high in order to measure vsys on ping 29

    charging = Pin('WL_GPIO2', Pin.IN)

    # these are specific reference voltages for a full/empty battery, in volts
    # your mileage may vary
    full_battery = 4.2
    empty_battery = 3.0

    voltage = get_vsys()
    percentage = 100 * ((voltage - empty_battery) / (full_battery - empty_battery))
    if percentage > 100:
        percentage = 100.00

    return charging.value(),percentage

def get_vsys():
    # pico w requires setting pin 25 to high in order to measure vsys on ping 29
    Pin(25, mode=Pin.OUT, pull=Pin.PULL_DOWN).high()

    # Reconfigure pin 29 as an input.
    Pin(29, Pin.IN)

    sample_count = 10
    battery_voltage = 0
    for _ in range(sample_count):
      battery_voltage += _read_vsys_voltage()
    return round( battery_voltage / sample_count, 2)

def _read_vsys_voltage():
    adc_Vsys = ADC(3)
    ADC_VOLT_CONVERSATION = 3.3 / 65535
    return adc_Vsys.read_u16() * 3.0 * ADC_VOLT_CONVERSATION

def write_to_file(filename, data):
    file = open(filename, 'w')
    led.value(1)
    file.write(f'{str(data)},')
    file.flush()
    led.value(0)

# start loop and init variables
fileid = random.randrange(10000)
tempfile = f'{fileid}-tempdata.txt'
capacityfile = f'{fileid}-capacitydata.txt'
led = Pin('WL_GPIO0', Pin.OUT)
while True:
    t = check_temp()
    c,p = check_power()
    if c == 0 or t > -15.0:
        if c == 0:
            message = f"temp is {t}, battery is not charging, capacity is {p}%"
        else:
            message = f"temp is {t}, battery is charging, capacity is {p}%"
        print(message)
        send_email(secrets.var_smtp, message)
        sleep(1800)
    else:
        message = f"temp is {t}, battery is charging, capacity is {p}%"
        print(message)
    sleep(60)
