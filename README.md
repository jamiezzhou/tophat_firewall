# Top Hat Question Notifier

A Python script that notifies the mac user when there's a new question on Top Hat classrooms. 

## Setup

## Setup and Install

0. **Clone the repository**:
    git clone https://github.com/jamiezzhou/tophat_firewall.git


1. **Prerequisites**: 
    - Python 3.x
    - Chrome browser
    - [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/); or install with homebrew 
    ```bash
    brew install --cask chromedriver
    ```

2. **Libraries to Install**:
   Install the required Python libraries with the following command:

    ```bash
    pip install playsound selenium bs4 playsound configparser ast
    ```

3. **Config File Setup**:
    - Modify the `config.ini` file accordingly
        - `Login`: `url` pointing to the login page.
        - `URLs`: `urls` being a list of URLs to be monitored.

    Sample `config.ini`:

    ```ini
    # Login page for website
    [Login]
    url = "https://app.tophat.com/e"
    # Array of top hat urls you want to check/access
    [URLs]
    urls = [
        "https://app.tophat.com/e/12345678/lecture/"
        ]
    ```

## Usage

1. Run the script:

    ```bash
    python3 Notify_mac.py
    ```

2. The first time you run the script, it will open a browser window for you to manually log in. After logging in, press Enter in the terminal to save the login cookies.

3. The script will continuously monitor the specified websites and notify you of any new questions.

## Note

- This script is specifically designed for macOS. For other OS, some modifications might be required.
- This script allows automatic login through cookie setting. If the login cookie expiers, please delete the content in the `cookie.txt` file and rerun the program to login in again.