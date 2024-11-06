from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

import pandas as pd
import time
import json

from chromedriver_manager import ChromeDriverManager
from credentialManager import CredentialManager

# some urls
URL_LOGIN = "https://x.tudelft.nl/pages/login"
USERNAME = "username"

XPATH_BUTTON_LOGIN = r"/html/body/app-root/page-layout/main/div/div/div[2]/div/login-page/div[2]/div/div/button"
XPATH_BUTTON_TUDELFT = r'//*[@id="idp-picker"]/section[2]/ul/li[1]/div'
XPATH_NETID = r'//*[@id="username"]'
XPATH_PASSWD = r'//*[@id="password"]'


def subscribe():
    # open webpage

    # deprecated:
    # cdm = ChromeDriverManager()
    # exe = cdm.getExecutable()

    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    driver.get(URL_LOGIN)
    print(driver.title)
    time.sleep(1)

    # click TU Delft login button
    driver.find_element(By.XPATH, value=XPATH_BUTTON_LOGIN).click()

    time.sleep(1)
    # select TU Delft org
    driver.find_element(By.XPATH, value=XPATH_BUTTON_TUDELFT).click()

    time.sleep(1)

    # retrieve credentials from credential manager
    cm = CredentialManager()
    password = cm.get_password(USERNAME)

    input_netid = driver.find_element(By.XPATH, value=XPATH_NETID)
    input_netid.clear()
    input_netid.send_keys(USERNAME)
    time.sleep(1)
    input_passwd = driver.find_element(By.XPATH, value=XPATH_PASSWD)
    input_passwd.clear()
    input_passwd.send_keys(password)
    time.sleep(1)
    input_passwd.send_keys(Keys.RETURN)  # login!

    time.sleep(10)


if __name__ == "__main__":
    subscribe()
