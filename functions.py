import time
import requests
import selectorlib
import smtplib, ssl
import os
from email.message import EmailMessage
import sqlite3

# Establish db conn
connection = sqlite3.connect("data.db")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36'}

def scrape(url):
    """ Scrape page source from URL """
    response = requests.get(url, headers=HEADERS)
    source = response.text
    return source


def extract(source):
    """ Extract id associated value from source """
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]
    return value


def send_email(message):
    """ Send email notification """

    host = "smtp.gmail.com"
    port = 465
    username = os.getenv("EMAILUSERNAME")
    password = os.getenv("PASSWORD3")
    receiver = os.getenv("EMAILUSERNAME")
    context = ssl.create_default_context()

    message = EmailMessage()
    message["Subject"] = "New Tour Event!"
    message.set_content("Dont miss out")

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message.as_string())
    print("Email Sent!")


def store(extracted):
    """ Store known values from extract function into db """
    row = extracted.split(",")
    row = [item.strip() for item in row]
    cursor = connection.cursor()
    cursor.execute("INSERT INTO events VALUES(?,?,?)", row)
    connection.commit()


def read(extracted):
    """ Prepare string then query content from db """
    row = extracted.split(",")
    row = [item.strip() for item in row]
    band, city, date = row
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
    rows = cursor.fetchall()
    return rows