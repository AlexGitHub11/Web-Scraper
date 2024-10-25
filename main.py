from functions import *

URL = "http://programmer100.pythonanywhere.com/tours/"

# Run scraper every 2 seconds
while True:
    # Get scraped data
    scraped = scrape(URL)
    extracted = extract(scraped)
    print(extracted)

    # Query db
    if extracted != "No upcoming tours":
        row = read(extracted)
        if not row:
            store(extracted)
            # Trigger alert
            send_email(message="New tour event!")

    time.sleep(2)