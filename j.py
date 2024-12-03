import json
import time
import os
import sys
from dotenv import load_dotenv
from cryptography.fernet import Fernet
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

# region ***CONSTANT
DEBUG = True
TIMER = 2  # seconds
config = os.path.join(os.getcwd(), ".env")
if os.path.isfile(config):
    load_dotenv(config)
else:
    print(">>> Missing Config File")
    for i in range(5, -1, -1):
        print(f"Auto close after {i} seconds....", end="\r", flush=True)
        time.sleep(1)
    sys.exit(0)

DEV_URL = "https://developer.servicenow.com/dev.do#!/home?wu=true"
CALU = os.getenv("CALU") == "True"
SILENT = os.getenv("SILENT") == "True"
key = os.getenv("K", Fernet.generate_key().decode())
fernet = Fernet(key.encode())
ENC = "utf-8"
INSTANCE_URL = os.getenv("INSTANCE_URL")
J_USERNAME = fernet.decrypt(os.getenv("J_USERNAME")).decode(
) if CALU else os.getenv("J_USERNAME")
J_PASSWORD = fernet.decrypt(os.getenv("J_PASSWORD")).decode(
) if CALU else os.getenv("J_PASSWORD")
A_USERNAME = fernet.decrypt(os.getenv("A_USERNAME")).decode(
) if CALU else os.getenv("A_USERNAME")
A_PASSWORD = fernet.decrypt(os.getenv("A_PASSWORD")).decode(
) if CALU else os.getenv("A_PASSWORD")

# LOAD PATTERNs
__PATTERN = None
if os.path.isfile("pattern.jl"):
    with open('pattern.jl', 'r', encoding=ENC) as file:
        data = file.read()
        __PATTERN = json.loads(fernet.decrypt(data.encode(ENC)).decode(ENC))

# endregion

# region ***INIT
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
if SILENT:
    print("*****Start with silent mode")
    chrome_options.add_argument("--headless")
else:
    print("*****Start with normal mode")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 60)
# endregion

# region ****FUNCs


def log(msg):
    print(">>> ", msg)


def login():
    print("--------- START LOGIN PROCESS")
    log("Start Authenticate...")
    time.sleep(TIMER)
    username_field = driver.find_element(By.ID, "user_name")
    password_field = driver.find_element(By.ID, "user_password")
    submit_btn = driver.find_element(By.ID, "sysverb_login")
    username_field.send_keys(J_USERNAME)
    password_field.send_keys(J_PASSWORD)
    submit_btn.click()
    time.sleep(TIMER)
    try:
        ele = WebDriverWait(driver, 5).until(EC.presence_of_element_located(
            (By.XPATH, "//*[@id='output_messages']/div/div/div")))
        if ele.text == "User name or password invalid":
            log("Login failed!")
            log("Wrong username/password")
            return False
    except Exception:
        pass

    wait.until(EC.url_contains(INSTANCE_URL +
               "/now/nav/ui/classic/params/target/ui_page.do"))
    log("Login successful")
    return True


def action():
    print("--------- START ACTION PROCESS")
    log("Check admin role")
    wait.until(EC.url_contains(INSTANCE_URL +
               "/now/nav/ui/classic/params/target/ui_page.do"))
    time.sleep(TIMER)
    ele = driver.execute_script(
        "return window.frames[0].g_user.roles.indexOf('admin') > -1")

    if not ele:
        log("User has not admin role")
        return False
    log("User has admin role")
    log("Access to Scripts - Background page....")
    driver.get(
        INSTANCE_URL+"/now/nav/ui/classic/params/target/sys.scripts.modern.do")
    log("Waiting navigate to Scripts - Background page....")
    wait.until(EC.url_to_be(
        INSTANCE_URL+"/now/nav/ui/classic/params/target/sys.scripts.modern.do"))
    time.sleep(TIMER)
    WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it(driver.execute_script(
        "return document.querySelector('body > macroponent-f51912f4c700201072b211d4d8c26010').shadowRoot.querySelector('#gsft_main');")))
    log("Scripts - Background page Loaded!")
    try:
        time.sleep(TIMER)
        driver.execute_script(
            "changeJsEditorPreference_script_editor('false');")
        wait.until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except Exception:
        pass
    time.sleep(TIMER)
    driver.execute_script(
        "document.querySelector('#script').value = 'gs.info(gs.now());'")
    driver.execute_script("document.querySelector('#MANDATORY').click();")
    log("Executing script....")
    time.sleep(TIMER)
    wait.until(EC.url_to_be(
        INSTANCE_URL+"/now/nav/ui/classic/params/target/sys.scripts.do"))
    # time.sleep(timer)
    ele = driver.execute_script(
        "return document.querySelector('body > pre').innerText;")
    log(ele)
    log("Execute script successful!")
    return True


def wakeup():
    print("--------- START WAKEUP PROCESS")

    # waiting redirect to dev page
    log("Navigate to DEV page")
    log("Waiting DEV page loaded.....")
    wait.until(EC.url_to_be(
        "https://developer.servicenow.com/dev.do#!/home?wu=true"))
    ele = wait.until(EC.visibility_of(driver.execute_script(
        "return document.querySelector('body > dps-app').shadowRoot.querySelector('div > header > dps-navigation-header').shadowRoot.querySelector('header > div > div.dps-navigation-header-utility > ul > li:nth-child(2) > dps-login').shadowRoot.querySelector('div > dps-button').shadowRoot.querySelector('button')")))
    log("DEV page loaded!")
    ele.click()
    # waiting redirect to login page
    log("Navigate to LOGIN page")
    log("Waiting LOGIN page loaded.....")
    wait.until(EC.url_to_be(
        "https://signon.service-now.com/x_snc_sso_auth.do?pageId=username"))
    wait.until(EC.presence_of_all_elements_located((By.ID, "email")))
    log("LOGIN page loaded!")

    # Fulfilment authenticate
    log("Get Email field")
    ele = driver.find_element(By.ID, "email")
    ele.click()
    log("Enter Email")
    ele.send_keys(A_USERNAME)
    ele = driver.find_element(By.ID, "username_submit_button")
    # time.sleep(timer)
    ele.click()
    log("Go to next step")
    wait.until(EC.presence_of_all_elements_located((By.ID, "password")))
    log("Get Password field")
    ele = driver.find_element(By.ID, "password")
    ele.click()
    log("Enter Password")
    ele.send_keys(A_PASSWORD)
    ele = driver.find_element(By.ID, "password_submit_button")
    # time.sleep(timer)
    ele.click()
    log("Start Authenticate...")
    time.sleep(TIMER)

    # Waiting instance wakeup
    try:
        log("Waiting DEV page loaded.....")
        wait.until(EC.url_to_be("https://developer.servicenow.com/dev.do"))
        log("Waiting instance wakeup.....")
        __retry = 0
        while __retry < 5:  # 3min
            time.sleep(45)
            driver.get(INSTANCE_URL)
            if driver.title.startswith("Log in"):
                log("Instance has been wake up!!!")
                return True
            __retry = __retry + 1

        log("WAKEUP PROCESS has been failed!")
        log("Please retry after 2 minutes.")

    except Exception as e:
        log("WAKEUP PROCESS has been failed!")
        log("Please retry after 2 minutes.")
        print(e)

    return False

# endregion

# region ****MAIN


def main():
    try:
        isWakeUpSuccessful = True
        driver.get(INSTANCE_URL)
        if driver.title == "Instance Hibernating page":
            log("Instance has been hibernated!")
            isWakeUpSuccessful = wakeup()
        else:
            log("Instance still alive!")
        if isWakeUpSuccessful and login():
            action()
    except Exception as e:
        print("------------------has been error")
        print(e)

    for i in range(5, -1, -1):
        print(f"Auto close after {i} seconds....", end="\r", flush=True)
        time.sleep(1)
    driver.close()
    sys.exit(0)


if __name__ == "__main__":
    if not DEBUG:
        main()
    else:
        driver.get(DEV_URL)
        wakeup()
        driver.close()

# endregion
