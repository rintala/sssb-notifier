import os
import time
import smtplib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def checkIfPreviousExists(filePath):
    # Check if previous number exists locally
    return os.path.isfile(filePath)


def getPreviousNumberOfApartments(fileName):
    # Fetch from locally stored file
    file = open(fileName, "r")
    numberOfApartments = file.read()
    return numberOfApartments


def getUpdatedNumberOfApartments():
    # Fetch from remote SSSB
    url = "https://www.sssb.se"

    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    driver = webdriver.Chrome(options=chromeOptions)

    driver.get(url)
    elem = driver.find_element(
        By.XPATH, "//*[@data-widget='objektsummering@lagenheter']")
    fetchedNumber = elem.text
    driver.close()

    return fetchedNumber


def sendMail(prevNumber, updatedNumber):
    # Send mail from user specified in USER_GMAIL and USER_PASSWORD to RECEIVING_USER
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(os.environ["GMAIL_USER"], os.environ["GMAIL_PASSWORD"])
    subject = "SSSB - Updated number of apartments"
    bodyText = "SSSB has changed the number of apartments \n\n SSSB has updated number of apartments from "+prevNumber + \
        " to " + updatedNumber + \
        "\n Check them out: https: // www.sssb.se/soka-bostad/sok-ledigt/lediga-bostader/ \n\n /SSSB-notifier"
    bodyHTML = "<html><body>"+"<h1>SSSB has changed the number of apartments </h1>" + "<p>SSSB has updated number of apartments from <b>" + prevNumber+"</b>" + " to <b>"+updatedNumber + \
        "</b></br></br>Check them out: <a href='https://www.sssb.se/soka-bostad/sok-ledigt/lediga-bostader/'>https://www.sssb.se/soka-bostad/sok-ledigt/lediga-bostader/</a></br></br>/SSSB-notifier</body></html>"

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = os.environ["GMAIL_USER"]
    message["To"] = os.environ["RECEIVING_USER"]

    part1 = MIMEText(bodyText, "plain")
    part2 = MIMEText(bodyHTML, "html")

    message.attach(part1)
    message.attach(part2)

    server.sendmail(
        os.environ["GMAIL_USER"],
        os.environ["RECEIVING_USER"],
        message.as_string()
    )


def updateLocal(absFilePath, updatedNumber):
    # Update number saved locally
    file = open(absFilePath, "w")
    file.write(updatedNumber)
    file.close()


def checkIfUpdated():
    # Check if previously saved number differs from newly fetched one and take action accordingly
    scriptDirectoryPath = os.path.dirname(__file__)
    fileName = "previous-number.txt"
    absFilePath = os.path.join(scriptDirectoryPath, fileName)

    prevExists = checkIfPreviousExists(absFilePath)

    if(prevExists):
        previousNumberOfApartments = getPreviousNumberOfApartments(absFilePath)
        updatedNumberOfApartments = getUpdatedNumberOfApartments()

        if(previousNumberOfApartments != updatedNumberOfApartments):
            sendMail(previousNumberOfApartments, updatedNumberOfApartments)
            updateLocal(absFilePath, updatedNumberOfApartments)

    else:
        updatedNumberOfApartments = getUpdatedNumberOfApartments()
        updateLocal(absFilePath, updatedNumberOfApartments)


def main():
    updateFrequencyInSeconds = 3600

    while(True):
        checkIfUpdated()
        time.sleep(updateFrequencyInSeconds)


if __name__ == "__main__":
    main()
