from selenium import webdriver
from playsound import playsound
import re
from bs4 import BeautifulSoup
from typing import List
import time
import subprocess
import ast
import os
from plyer import notification
import platform

class ConfigData():
    login: str = ""
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
    configData.login = json.loads(iniParse.get("Login", "url"))
    configData.websites = json.loads(iniParse.get("URLs", "urls"))
    return configData

def save_cookies(driver, configData):
    driver.get(configData.login)

    if not os.path.exists('cookies.txt'):
        with open('cookies.txt', 'w') as cookies_file:
            cookies_file.write('')
    with open('cookies.txt', 'r') as cookies_file:
        cookies = cookies_file.read()
        if not cookies:
            # Wait for user input
            input("Log in through the browser and then press Enter to continue...")
            # After logging in:
            all_cookies = driver.get_cookies()
            # Saving the cookies to a local file
            with open('cookies.txt', 'w') as file:
                file.write(str(all_cookies))

def login_cookie(driver):
    with open('cookies.txt', 'r') as cookies_file:
        cookies = ast.literal_eval(cookies_file.read())
        if not cookies:
            raise Exception("Login was unsuccessful. Cookies not successfully set.")
        for cookie in cookies:
            driver.add_cookie(cookie)

def main(configFile: str):
    configData = loadConfig(configFile)
    driver = getDriver()
    save_cookies(driver, configData)
    while True:
        # driver = getDriver()
        try:
            runSelenium(driver, configData)
        except Exception as error:
            print("Caught exception!", error)
            driver.quit()
            quit()

def runSelenium(driver, configData: ConfigData):
    print("running selenium")
    driver.get(configData.login)
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
        time.sleep(8)
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
        send_notification(websiteData.url)

def send_notification(urlName: str):
    if platform.system() == "Windows":
        notify_windows(urlName)
    elif platform.system() == "Darwin":  # macOS
        notifyMac(urlName)
    else:
        # Implement other OS or raise not supported error
        pass

def playNotifySound():
    playsound("notifySound.wav")


def notify_windows(urlName: str):
    notification.notify(
        title="Top Hat Question!",
        message=f"New question on {urlName}",
        app_name="Top Hat Notifier",
        timeout=10  # Show the notification for 10 seconds
    )

def notifyMac(urlName: str):
    # Use AppleScript to send a notification on Mac
    applescript_command = f'display notification "New question on {urlName}" with title "Top Hat Question!"'
    subprocess.run(["osascript", "-e", applescript_command])


def getDriver():
    # Specify the path to the Chrome driver for macOS
    if platform.system() == "Windows":
        driver = webdriver.Chrome(executable_path="chromedriver.exe")
    elif platform.system() == "Darwin":  # macOS
        driver = webdriver.Chrome()
    driver.implicitly_wait(15)
    return driver


if __name__ == "__main__":
    main("config.ini")