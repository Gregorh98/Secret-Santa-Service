import random
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv
import csv

load_dotenv()

santas = csv.reader(open("santa_name_email.csv", encoding="utf8"))

sender = os.getenv("sender")

santas = [
	["TEST 1","test1@test.com"],
    ["TEST 2","test2@test.com"]
]

buyingFor = [santa[0] for santa in santas]

matches = []

def matchSantas():
	for santa in santas:
		foundMatch = False
		while foundMatch != True:
			match = random.choice(buyingFor)
			if match != santa[0]:
				buyingFor.remove(match)
				matches.append([santa, match])
				foundMatch = True

def getDaysTillChristmas():
    today = datetime.today()
    christmas = datetime(today.year, 12, 25)
    
    # Check if Christmas has already passed this year
    if today > christmas:
	    christmas = datetime(today.year + 1, 12, 25)
    
    days_till_christmas = (christmas - today).days
    return days_till_christmas


def emailSantas():
		print("Opening SMTP server")
		mailserver = smtplib.SMTP('smtp.office365.com',587)
		mailserver.ehlo()
		print("Encrypting transmissions")
		mailserver.starttls()
		mailserver.ehlo()
		print("Logging in")
		mailserver.login(sender, 'lG4M#@0WTB&y')
		
		for match in matches:
			msg = MIMEMultipart()
			msg['From'] = sender
			msg['To'] = match[0][1]
			msg['Subject'] = 'Secret Santa 2023!'
			message = """
Hello Santa %s!
Its officially %s days till Christmas and its time for Secret Santa %s!
			
*-*-*-*-*-*-*-*-*-*-*-*-*-*
YOU ARE BUYING FOR %s!
*-*-*-*-*-*-*-*-*-*-*-*-*-*
			
Merry Christmas, and happy present hunting!
			""" % (
			    match[0][0],
			    getDaysTillChristmas(),
			    datetime.today().year,
			    match[1].upper()
			)
			
			msg.attach(MIMEText(message))

			print("Sending mail to %s - %s" % (match[0][0], match[0][1]))
			#print("\n\n" + message + "\n\n")
			mailserver.sendmail('sender@test.com',match[0][1],msg.as_string())
			
		mailserver.quit()
				
matchSantas()
emailSantas()
