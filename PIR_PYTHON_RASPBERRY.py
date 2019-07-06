#created by Raghav Aadithya S
#ping me on my youtube channel TRANDIO
import RPi.GPIO as GPIO
import time
import smtplib
from subprocess import call
import time;
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
GPIO.setmode(GPIO.BOARD) #Set GPIO to pin numbering
pir = 8 #Assign pin 8 to PIR
led = 10 #Assign pin 10 to LED
GPIO.setup(pir, GPIO.IN) #Setup GPIO pin PIR as input
GPIO.setup(led, GPIO.OUT) #Setup GPIO pin for LED as output
print ("Sensor initializing . . .")
time.sleep(2) #Give sensor time to startup
print ("Active")
print ("Press Ctrl+c to end program")
def main():
    call("raspistill -o intruder.jpg",shell=True)#lower your camera qualityy by using q with any value betweem 0 to 100 "-q 50"same for  height and width
    email_user = "YOUR_MAIL_ID"
    email_password = "YOUR_PASSWORD"
    localtime = time.asctime( time.localtime(time.time()) )
    email_rcver = "RECIEVER_MAIL_ID"
    subject = 'Intruder Alert '
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_rcver
    msg['Subject'] = subject + localtime
    body = 'hey it seems there is an intruder'
    msg.attach(MIMEText(body, 'plain'))
    filename = 'intruder.jpg'
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('content-disposition', "attachment; filename= "+filename)
    msg.attach(part)
    text = msg.as_string()
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo_or_helo_if_needed()
    server.starttls()
    server.ehlo_or_helo_if_needed()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_rcver,text)
    server.quit()
    print("sent!")
try:
    while True:
        if GPIO.input(pir) == True: #If PIR pin goes high, motion is detected
            print ("Motion Detected!")
            main()
            GPIO.output(led, True) #Turn on LED
            time.sleep(4) #Keep LED on for 4 seconds
            GPIO.output(led, False) #Turn off LED
            time.sleep(0.1)

except KeyboardInterrupt: #Ctrl+c
    pass #Do nothing, continue to finally

finally:
    GPIO.output(led, False) #Turn off LED in case left on
    GPIO.cleanup() #reset all GPIO
    print ("Program ended")
    