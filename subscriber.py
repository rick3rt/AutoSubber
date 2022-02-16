
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
import time
import json


# some urls
SPORT_NAME = "SPINNING"
SPORT_TABLE_NAME = "SPINNING"
URL_LOGIN = "https://www.olympos.nl/Inloggen/tabid/422/language/nl-NL/Default.aspx?returnurl=%2f"
URL_SUBSCRIBE = "https://www.olympos.nl/nl-nl/sportaanbod/groepslessen/allegroepslessen/details.aspx?sportgroep={}#Groepsles".format(
    SPORT_NAME)

# sensitive information
with open('info.json', 'r') as f:
    data = json.load(f)
print(data)

DAY_STR = 'di'
SCO_NUM = data['sco']
SCO_PASSWD = data['word']
IS_LOGIN = True

# website info
XPATH_SCO_NUM = '//*[@id="dnn_ctr896_MainView_txtSconummer"]'
XPATH_SCO_PASSWD = '//*[@id="dnn_ctr896_BestaandView_txtWachtwoord"]'


def subscribe():
    # open webpage
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(executable_path="./chromedriver")
    driver.implicitly_wait(10)
    driver.get(URL_LOGIN)
    print(driver.title)
    assert "Sportcentrum Olympos" in driver.title

    # login
    if IS_LOGIN:
        elem = driver.find_element(By.XPATH, value=XPATH_SCO_NUM)
        elem.clear()
        elem.send_keys(SCO_NUM)
        elem.send_keys(Keys.RETURN)
        time.sleep(1.123)

        elem = driver.find_element(By.XPATH, value=XPATH_SCO_PASSWD)
        elem.clear()
        elem.send_keys(SCO_PASSWD)
        elem.send_keys(Keys.RETURN)

    # go to spin inschrijven page
    driver.get(URL_SUBSCRIBE)

    # read table
    # table = driver.find_elements(By.XPATH, value=XPATH_SPORT_TABLE)
    #                     //*[@id="{}"]/div[3]/table
    # XPATH_SPORT_TABLE = '//*[@id="{}"]/div[3]/table'.format(SPORT_NAME)
    tab2 = driver.find_element(
        By.CSS_SELECTOR, "#{sport} > div.aanbod.visibleTrue > table".format(sport=SPORT_TABLE_NAME))
    html = tab2.get_attribute('outerHTML')
    with open('webpage.html', 'w') as f:
        f.write(html)

    # convert table to pandas
    df = pd.read_html(html)[0]
    ROW_NUM = df.index[df.Dag == DAY_STR].tolist()[0]
    print("ROW: ", ROW_NUM)

    # find a button
    DAY_NUM = ROW_NUM + 1
    XPATH_BUT = '//*[@id="{sport}"]/div[3]/table/tbody/tr[{dag}]/td[9]/a'.format(
        sport=SPORT_TABLE_NAME,
        dag=DAY_NUM)
    # print(XPATH_BUT)
    but = driver.find_element(By.XPATH, XPATH_BUT)

    IS_RESERVING = False
    time.sleep(1.35)  # s
    if "VOLGEBOEKT" in but.text or \
            "KAN NU NIET MEER" in but.text or \
            "VANAF" in but.text:
        print("dag is al vol of kan nog niet: ", but.text)
        driver.close()
        print("MISKULLLKT!")
        return 0
    elif "RESERVEER" in but.text:
        print("dag reserveren")
        but.click()
        IS_RESERVING = True
    else:
        print("No match, but.text: ", but.text)

    XPATH_RESULT = '//*[@id="evenwachten"]/span/a'
    XPATH_RESERVE = '//*[@id="sportpas"]/a[3]'

    isVol = False
    if IS_RESERVING:
        time.sleep(1.1235)  # s
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "evenwachten"))
            )
            if "De geselecteerde cursus of les is vol." in elem.text:
                print("Les is vol. ABORT!")
                but = driver.find_element(By.XPATH, XPATH_RESULT)
                but.click()
                isVol = True
            print('am here:')
            print(elem.text)
        finally:
            isVol = False
            # print('Reservation kan wel? ')
            print(elem.text)

    print('revereer knoppen indrukken:')
    print(isVol)
    # act on result
    if not isVol:
        try:
            elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "sportpas"))
            )
            print(elem.text)
            if elem:
                print("En nu klikken om te reverereren!")
                but = driver.find_element(By.XPATH, XPATH_RESERVE)
                but.click()
                isVol = True
        finally:
            print('Reservation is onderweg en gaat wel lukken hoor.')

    print("Thats it :) daAAAAAG")
    time.sleep(1.12837)  # s
    driver.close()
    print("WE HEBBEN GERESERVEERD!")
    return 1


if __name__ == '__main__':
    sucess = subscribe()
