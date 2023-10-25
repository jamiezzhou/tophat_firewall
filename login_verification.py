from selenium import webdriver
import time

def main():
    driver = webdriver.Chrome()
    try:
        runSelenium(driver)
    except Exception as error:
        print("Caught exception!", error)
    

def runSelenium(driver):
    driver.get("https://app.tophat.com/e")
    time.sleep(60)
    # After logging in:
    all_cookies = driver.get_cookies()

    # Saving the cookies to a local file
    with open('cookies.txt', 'w') as file:
        file.write(str(all_cookies))

if __name__ == "__main__":
    main()