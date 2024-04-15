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


# constant
timer = 2
config = os.path.join(os.getcwd(), ".env")
# config = 'dist/.env'
if os.path.isfile(config):
    load_dotenv(config)
else:
    print(">>> Missing Config File")
    for i in range(5, -1, -1):
        print(f"Auto close after {i} seconds....", end="\r", flush=True)
        time.sleep(1)
    sys.exit(0)


CALU = os.getenv("CALU") == "True"
SILENT = os.getenv("SILENT") == "True"
key = os.getenv("K", Fernet.generate_key().decode())
fernet = Fernet(key.encode())
DEBUG = False
INSTANCE_URL = os.getenv("INSTANCE_URL")
J_USERNAME = fernet.decrypt(os.getenv("J_USERNAME")).decode(
) if CALU else os.getenv("J_USERNAME")
J_PASSWORD = fernet.decrypt(os.getenv("J_PASSWORD")).decode(
) if CALU else os.getenv("J_PASSWORD")
A_USERNAME = fernet.decrypt(os.getenv("A_USERNAME")).decode(
) if CALU else os.getenv("A_USERNAME")
A_PASSWORD = fernet.decrypt(os.getenv("A_PASSWORD")).decode(
) if CALU else os.getenv("A_PASSWORD")

if DEBUG:
    print(CALU)
    print("-----------------------------")
    print(f"SLIENT MODE: {SILENT}")
    print(f"INSTANCE URL: {INSTANCE_URL}")
    print(f"J_USERNAME: {J_USERNAME}")
    print(f"J_PASSWORD: {J_PASSWORD}")
    print(f"A_USERNAME: {A_USERNAME}")
    print(f"A_PASSWORD: {A_PASSWORD}")

# init
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

def login():
    print("--------- START LOGIN PROCESS")
    log("Start Authenticate...")
    time.sleep(timer)
    username_field = driver.find_element(By.ID, "user_name")
    password_field = driver.find_element(By.ID, "user_password")
    submit_btn = driver.find_element(By.ID, "sysverb_login")
    username_field.send_keys(J_USERNAME)
    password_field.send_keys(J_PASSWORD)
    submit_btn.click()
    time.sleep(timer)
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
    log("Find Script-background menu")
    time.sleep(timer)
    ele = wait.until(EC.visibility_of(driver.execute_script(
        "return document.querySelector('body > macroponent-f51912f4c700201072b211d4d8c26010').shadowRoot.querySelector('div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout').shadowRoot.querySelector('div.sn-polaris-layout.polaris-enabled > div.layout-main > div.header-bar > sn-polaris-header').shadowRoot.querySelector('#d6e462a5c3533010cbd77096e940dd8c');")))
    ele.click()
    time.sleep(timer)
    # check admin role
    try:
        ele = wait.until(EC.visibility_of(driver.execute_script(
            "return document.querySelector('body > macroponent-f51912f4c700201072b211d4d8c26010').shadowRoot.querySelector('div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout').shadowRoot.querySelector('div.sn-polaris-layout.polaris-enabled > div.layout-main > div.header-bar > sn-polaris-header').shadowRoot.querySelector('nav > div > sn-polaris-menu:nth-child(1)').shadowRoot.querySelector('#filter');")))
        ele.click()
        ele.send_keys("Scripts - Background")
        time.sleep(timer)
        wait.until(EC.visibility_of(driver.execute_script(
            "return document.querySelector('body > macroponent-f51912f4c700201072b211d4d8c26010').shadowRoot.querySelector('div > sn-canvas-appshell-root > sn-canvas-appshell-layout > sn-polaris-layout').shadowRoot.querySelector('div.sn-polaris-layout.polaris-enabled > div.layout-main > div.header-bar > sn-polaris-header').shadowRoot.querySelector('nav > div > sn-polaris-menu:nth-child(1)').shadowRoot.querySelector('nav > div.sn-polaris-nav.d6e462a5c3533010cbd77096e940dd8c.can-animate > div.super-filter-container.all-results-open > div.all-results-section.section-open.results-section > div > div.sn-polaris-tab-content.-left.is-visible.can-animate > div > sn-collapsible-list').shadowRoot.querySelector('a[data-id=\"5e24af15c0a80a940121f06c64cf5982\"] > span > span.label > mark');")))

    except Exception:
        log("User has not admin role")
        return False

    driver.get(
        INSTANCE_URL+"/now/nav/ui/classic/params/target/sys.scripts.modern.do")
    log("Waiting navigate to Scripts - Background page....")
    wait.until(EC.url_to_be(
        INSTANCE_URL+"/now/nav/ui/classic/params/target/sys.scripts.modern.do"))
    time.sleep(timer)
    WebDriverWait(driver, 60).until(EC.frame_to_be_available_and_switch_to_it(driver.execute_script(
        "return document.querySelector('body > macroponent-f51912f4c700201072b211d4d8c26010').shadowRoot.querySelector('#gsft_main');")))
    log("Scripts - Background page Loaded!")
    try:
        time.sleep(timer)
        driver.execute_script(
            "changeJsEditorPreference_script_editor('false');")
        wait.until(EC.alert_is_present())
        driver.switch_to.alert.accept()
    except Exception:
        pass
    time.sleep(timer)
    driver.execute_script(
        "document.querySelector('#script').value = 'gs.info(gs.now());'")
    driver.execute_script("document.querySelector('#MANDATORY').click();")
    log("Executing script....")
    time.sleep(timer)
    wait.until(EC.url_to_be(
        INSTANCE_URL+"/now/nav/ui/classic/params/target/sys.scripts.do"))
    # time.sleep(timer)
    ele = driver.execute_script(
        "return document.querySelector('body > pre').innerText;")
    log(ele)
    log("Execute script successful!")

    return True


def log(msg):
    print(">>> ", msg)


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
    time.sleep(timer)
    ele.click()
    log("Go to next step")
    wait.until(EC.presence_of_all_elements_located((By.ID, "password")))
    log("Get Password field")
    ele = driver.find_element(By.ID, "password")
    ele.click()
    log("Enter Password")
    ele.send_keys(A_PASSWORD)
    ele = driver.find_element(By.ID, "password_submit_button")
    time.sleep(timer)
    ele.click()
    log("Start Authenticate...")
    time.sleep(timer)

    # Waiting instance wakeup
    log("Waiting instance wakeup.....")
    wait.until(EC.url_to_be(
        "https://developer.servicenow.com/dev.do#!/home"))
    time.sleep(timer)
    ele = WebDriverWait(driver, 180).until(EC.element_to_be_clickable(driver.execute_script(
        "return document.querySelector('body > dps-app').shadowRoot.querySelector('div > main > dps-home-auth-quebec').shadowRoot.querySelector('div > section:nth-child(1) > div > dps-page-header > div:nth-child(1) > button');")))
    log("instance has been wake up!!!")
    return True


def main():
    try:
        driver.get(INSTANCE_URL)
        if driver.title == "Instance Hibernating page":
            log("Instance has been hibernated!")
            wakeup()
        else:
            log("Instance still alive!")
        if login():
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
