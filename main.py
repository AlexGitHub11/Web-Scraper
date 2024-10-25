import time
import requests
import selectorlib
import smtplib, ssl
import os
from email.message import EmailMessage


URL = "http://programmer100.pythonanywhere.com/tours/"

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
    """ Store known values from extract function """
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")


def read(extracted):
    """ Read content of data.txt """
    with open("data.txt", "r") as file:
        return file.read()



if __name__ == "__main__":

    # Run scraper every 2 seconds
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        print(extracted)

        content = read(extracted)

        if extracted != "No upcoming tours":
            if extracted not in content:
                store(extracted)
                send_email(message="New tour event!")

        time.sleep(2)