import umail
import network

# Your network credentials
ssid = ''
password = ''

# Email details
sender_email = '' # Replace with the email address of the sender
sender_name = '' # Replace with the name of the sender
sender_app_password = '' # Replace with the app password of the sender's email account
recipient_email ='' # Replace with the email address of the recipient
email_subject ='' # Subject of the email

def connect_wifi(ssid, password):
  # Connect to your network using the provided credentials
  station = network.WLAN(network.STA_IF)
  station.active(True)
  station.connect(ssid, password)
  # Wait for the connection to be established
  while station.isconnected() == False:
    pass
  print('Connection successful') # Print a message if the connection is successful
  print(station.ifconfig()) # Print the network configuration
    
connect_wifi(ssid, password)

# Send the email
# Connect to the Gmail's SSL port
smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
# Login to the email account using the app password
smtp.login(sender_email, sender_app_password)
# Specify the recipient email address
smtp.to(recipient_email)
# Write the email header
smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
smtp.write("Subject:" + email_subject + "\n")
# Write the body of the email
smtp.write("Test Email from Raspberry Pi Pico W")
# Send the email
smtp.send()
# Quit the email session
smtp.quit()