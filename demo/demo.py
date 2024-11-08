from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


from autosubber.credentialmanager import CredentialManager
import time
import os

DEMO_PATH = os.path.dirname(os.path.realpath(__file__))
DEMO_PAGE_URL = f"file:///{DEMO_PATH}/demo.html"


def subscribe():

    # hardcoded credentials for demo purposes
    username = "user"
    password = "pass"
    # or use credential manager
    # cm = CredentialManager()
    # password = cm.get_password(username)

    # optional, run headless:
    options = Options()
    # options.headless = True

    # open a browser and load the demo page
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)
    driver.get(DEMO_PAGE_URL)

    time.sleep(1)

    XPATH_USERNAME = r"/html/body/div/input[1]"
    XPATH_PASSWORD = r"/html/body/div/input[2]"
    XPATH_BUTTON = r"/html/body/div/button"
    XPATH_PROMPT = r"/html/body/div[2]"

    # fill in the form
    input_username = driver.find_element(By.XPATH, value=XPATH_USERNAME)
    input_username.clear()  # clears the current contents
    input_username.send_keys(username)  # types the username

    input_password = driver.find_element(By.XPATH, value=XPATH_PASSWORD)
    input_password.clear()
    input_password.send_keys(password)

    # click the button
    driver.find_element(By.XPATH, value=XPATH_BUTTON).click()

    # check if login was successful. if successful, the webpage titlebar will display "Success"
    time.sleep(1)
    msg_box = driver.find_element(By.XPATH, value=XPATH_PROMPT)
    print("Prompt text:")
    print(msg_box.text)

    task_success = False
    if "Login successful!" in msg_box.text:
        task_success = True
        print("Login Success!")
    else:
        print("Login failed")

    # close the browser
    driver.quit()

    return task_success


if __name__ == "__main__":
    subscribe()
