import random
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

sender = os.getenv("sender")
password = os.getenv("password")

santas = [
    ["Santa 1", "santa1@northpole.com"],
    ["Santa 2", "santa2@southpole.com"],
]

buyingFor = [santa[0] for santa in santas]

matches = []


def match_santas():
    for santa in santas:
        foundMatch = False
        while not foundMatch:
            match = random.choice(buyingFor)
            if match != santa[0]:
                buyingFor.remove(match)
                matches.append([santa, match])
                foundMatch = True


def get_days_till_christmas():
    today = datetime.today()
    christmas = datetime(today.year, 12, 25)

    # Check if Christmas has already passed this year
    if today > christmas:
        christmas = datetime(today.year + 1, 12, 25)

    days_till_christmas = (christmas - today).days
    return days_till_christmas


def email_santas(test=True):
    print("Opening SMTP server")
    mailserver = smtplib.SMTP('smtp.gmail.com', 587)
    mailserver.ehlo()
    print("Encrypting transmissions")
    mailserver.starttls()
    mailserver.ehlo()
    print("Logging in")
    mailserver.login(sender, password)

    for match in matches:
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = match[0][1] if not test else sender
        msg['Subject'] = f'Secret Santa {datetime.today().year}!'
        message = f"""
{"Hello Santa %s!" if not test else "*** THIS IS A TEST ***"}
Its officially %s days till Christmas and its time for Secret Santa %s!
			
*-*-*-*-*-*-*-*-*-*-*-*-*-*
YOU ARE BUYING FOR %s!
*-*-*-*-*-*-*-*-*-*-*-*-*-*
			
Merry Christmas, and happy present hunting!
			""" % (
            match[0][0],
            get_days_till_christmas(),
            datetime.today().year,
            match[1].upper()
        )

        msg.attach(MIMEText(message))

        print("Sending mail to %s - %s" % (match[0][0], match[0][1] if not test else sender))
        mailserver.sendmail(sender, match[0][1] if not test else sender, msg.as_string())
        print(message + "\n\n")

    mailserver.quit()


match_santas()
email_santas(test=False)
