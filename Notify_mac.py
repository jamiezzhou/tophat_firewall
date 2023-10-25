from selenium import webdriver
import re
from bs4 import BeautifulSoup
from typing import List
import time
import os
import subprocess
import ast

class ConfigData():
    websites: list = []


class WebsiteData():
    url: str = ""
    questions: int = 0
    isNotifying: bool = False


def loadConfig(configFile: str) -> ConfigData:
    import configparser
    import json
    configData = ConfigData()
    iniParse = configparser.ConfigParser()
    iniParse.read(configFile)
    configData.websites = json.loads(iniParse.get("URLs", "urls"))
    return configData


def main(configFile: str):
    configData = loadConfig(configFile)
    while True:
        driver = getDriver()
        try:
            runSelenium(driver, configData)
        except Exception as error:
            print("Caught exception!", error)
        driver.quit()

def login_cookie(driver):
    with open('cookies.txt', 'r') as cookies_file:
        cookies = ast.literal_eval(cookies_file.read())
        for cookie in cookies:
            driver.add_cookie(cookie)

def runSelenium(driver, configData: ConfigData):
    print("running selenium")
    driver.get("https://app.tophat.com/e")
    time.sleep(2)
    login_cookie(driver)
    driver.get(configData.websites[0])
    time.sleep(4)

    websiteArray: List[WebsiteData] = []
    for url in configData.websites:
        websiteData = WebsiteData()
        websiteData.url = url
        driver.get(url)
        time.sleep(4)
        websiteData.questions = find_questions(driver.page_source)
        websiteArray.append(websiteData)

    while True:
        checkDifferences(driver, websiteArray)

def find_questions(htmlCode):
    soup = BeautifulSoup(htmlCode, 'lxml')
    # Find the element containing the desired content
    pattern = re.compile(r"Questions & Attendance.*")
    element = soup.find(text=pattern).find_parent()
    # List to store all siblings of the target element
    siblings = []
    # Iterate over the next siblings of the element
    for sibling in element.find_next_siblings():
        siblings.append(sibling)
    return len(sibling)


def checkDifferences(driver, websiteArray: List[WebsiteData]):
    for websiteData in websiteArray:
        driver.get(websiteData.url)
        time.sleep(4)
        questions = find_questions(driver.page_source)
        if questions != websiteData.questions:
            websiteData.questions = questions
            notify(websiteData)
            websiteData.isNotifying = True
        else:
            if websiteData.isNotifying:
                websiteData.isNotifying = False


def notify(websiteData: WebsiteData):
    if websiteData.isNotifying:
        print("Reminder! New Top Hat question on " + websiteData.url)
        playNotifySound()
    else:
        print("Notification! New Top Hat question on " + websiteData.url)
        playNotifySound()
        notifyMac(websiteData.url)


def playNotifySound():
    # playsound library can be used on Mac as well
    from playsound import playsound
    playsound("notifySound.wav")


def notifyMac(urlName: str):
    # Use AppleScript to send a notification on Mac
    applescript_command = f'display notification "New question on {urlName}" with title "Top Hat Question!"'
    subprocess.run(["osascript", "-e", applescript_command])


def getDriver():
    # Specify the path to the Chrome driver for macOS
    driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    return driver


if __name__ == "__main__":
    main("config.ini")