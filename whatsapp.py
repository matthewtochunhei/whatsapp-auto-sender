from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions

# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait

import datetime
import time
import os


def check_is_new_user(user_data_dir: str):
    # check if the user_data_dir exists
    if not os.path.exists(user_data_dir):
        return True
    # check if the user_data_dir is empty
    if len(os.listdir(user_data_dir)) == 0:
        return True
    return False


def whatsapp_init(user_data_dir: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get("https://web.whatsapp.com/")
    driver.maximize_window()
    # wait for user to scan QR code
    # print it 10 times
    for i in range(10):
        print(f"Waiting for QR code to be scanned {i}")
        time.sleep(1)
    driver.close()


def send_message(group_id: str, message: str, user_data_dir: str):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    # run in headless mode
    chrome_options.add_argument("--headless")
    temp_driver = webdriver.Chrome()
    user_agent = temp_driver.execute_script("return navigator.userAgent;")
    temp_driver.close()
    chrome_options.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Chrome(chrome_options=chrome_options)

    # https://web.whatsapp.com/accept?code=
    driver.get(f"https://web.whatsapp.com/accept?code={group_id}")
    driver.maximize_window()

    # find the input box
    inp_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
    input_box = WebDriverWait(driver, 60).until(
        expected_conditions.presence_of_element_located((By.XPATH, inp_xpath))
    )
    # type the message
    input_box.send_keys(message)
    time.sleep(5)
    # press enter
    input_box.send_keys(Keys.ENTER)
    time.sleep(5)
    # close the tab
    driver.close()

    print(f"Message sent successfully at {datetime.datetime.now()}")