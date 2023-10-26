# Top Hat Question Notifier (for mac)

A Python script that notifies macOS/Windows users of new questions on Top Hat classrooms.

### Prerequisites

- Python 3.x
- Chrome browser
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
  - macOS: Install with homebrew:
    ```bash
    brew install --cask chromedriver
    ```
  - Windows: A executable is provided in this repo. You can also download it yourself and place it in the same folder.

## Setup and Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/jamiezzhou/tophat_firewall.git
    ```

2. **Install Required Libraries**:
    Use pip to install the necessary Python libraries:
    ```bash
    pip install selenium bs4 playsound configparser ast plyer
    ```

3. **Configuration**:
    - Adjust the `config.ini` file to your needs.
        - `Login`: Add the `url` of the login page.
        - `URLs`: Add the `urls` (a list) that you want to monitor.
    Example of a `config.ini` file:
    ```ini
    [Login]
    url = "https://app.tophat.com/e"
    
    [URLs]
    urls = [
        "https://app.tophat.com/e/12345678/lecture/"
        ]
    ```

## Usage

1. **Run the Script**:
    ```bash
    python3 Notify.py
    ```

2. **First-time Login**:
    - During the first execution, the script opens a browser for manual login. 
    - After successfully logging in, return to the terminal and press Enter. This action saves the login cookies for subsequent uses.

3. **Monitoring**:
    The script will then keep an eye on the websites you specified. When there's a new question, you'll get a notification.

## Important Notes

- **Operating System**: This script is tailored for macOS and Windows. Adaptations might be necessary for other operating systems.
  
- **Automatic Login**: The script enables auto-login using saved cookies. If these cookies expire, empty the `cookie.txt` file and rerun the program to log in again.

