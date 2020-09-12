#!/usr/bin/python3
# For using DS18B20 to get temperature with a raspberry pi
# Based on https://learn.adafruit.com/pages/1108/elements/227198/download

import os
import glob
import time
from twilio.rest import Client


# Authenticate to Twilio account

account_sid = "yoursidhere"
auth_token = "yourtokenhere"

client = Client(account_sid, auth_token)

# Setup DS sensor

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        tempC = float(temp_string) / 1000.0
        tempF = tempC * 9.0 / 5.0 + 32.0
        return tempC, tempF

tempC, tempF = read_temp()

print(tempC)
print(tempF)

print('Current Temperature Sensor Info')
print('The temperature is:',tempC,'degrees C')
print('The temperature is:',tempF,'degrees F')

user1Number="+<somephonenumber>"
user2Number="+<somephonenumber>"
user1Email='someemail'
user2Email='someemail'

def sendText(x):

        try:
                client.api.account.messages.create(
                        to=x,
                        from_="+",
                        body="""

The freezer is critically hot.
The temperature is %sF.
The temperature is %sC.

                        """ % (tempF, tempC))

                print("Text sent!")
        
        except: 
                print("Text not sent!")



def sendEmail(x,y):

        import smtplib

        gmail_user = 'youremailuser'
        gmail_password = 'youremailpassword'

        sent_from = gmail_user
        to = [x,y]
        subject = 'Garage Freezer Temp Warning'
        body = 'The freezer is critically hot. The temperature is {}'.format(tempF)

        email_text = """

The freezer is critically hot.
The temperature is %sF.
The temperature is %sC.

        """ % (tempF, tempC)

        try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(sent_from, to, email_text)
                server.close()

                print('Email sent!')
        except:
                print('Email not sent!')


if tempF > 10:

        sendText(user1Number)
        sendText(user2Number)
        sendEmail(user1Email, user2Email)
