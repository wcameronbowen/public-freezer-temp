try:
  import urequests as requests
except:
  import requests
  
import network
import gc
gc.collect()

ssid = ''
password = ''

# Your Account SID and Auth Token from twilio.com/console
account_sid = ''
auth_token = ''
recipient_num = ''
sender_num = ''

def send_sms(recipient, sender,
             message, auth_token, account_sid):
      
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = "To={}&From={}&Body={}".format(recipient,sender,message)
    url = "https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json".format(account_sid)
    
    print("Trying to send SMS with Twilio")
    
    response = requests.post(url,
                             data=data,
                             auth=(account_sid,auth_token),
                             headers=headers)
    
    if response.status_code == 201:
        print("SMS sent!")
    else:
        print("Error sending SMS: {}".format(response.text))
    
    response.close()

def connect_wifi(ssid, password):
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  while station.isconnected() == False:
    pass
  print('Connection successful')
  print(station.ifconfig())

connect_wifi(ssid, password)
message = "Hello This is a test message"
send_sms(recipient_num, sender_num, message, auth_token, account_sid)