from selenium import webdriver
import os
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import requests
import pandas as pd
from datetime import datetime, timedelta
from config import *
from helper import *
import logging
import gc

dir_path = os.path.dirname(os.path.realpath(__file__))

def cleanup_driver(driver):
    if driver is None:
        return
    
    try:
        driver.close()  # Closes current window
        driver.quit()  # Terminates the browser process completely
        del driver  # Remove reference to the driver object
        
    except Exception as e:
        print(f"Error during driver cleanup: {str(e)}")
    
    finally:
        gc.collect()

def login_health_app(url,username,password,secret_key):

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')	
        # options.add_argument('--headless')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")  # Add this
        options.add_argument("--disable-extensions")  # Add this
        options.add_argument("--disable-infobars")  # Add this
        options.add_argument("--disable-notifications")  # Add this
        options.add_argument("--disable-application-cache")  # Add this
        options.add_argument("--window-size=1280,700")  # Fixed syntax

        options.add_argument("--disable-browser-side-navigation")  # Add this
        options.add_argument("--dns-prefetch-disable")  # Add this
        options.add_argument("--disable-setuid-sandbox")  # Add this
        # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_experimental_option("prefs",{
            "download.default_directory" : dir_path,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.images": 2
            })   
        
        # service = webdriver.ChromeService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        # driver = webdriver.Chrome(service=service, options=options)
        driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)  # Set maximum page load time

        driver.get(url)
        
        # Wait specifically for login fields (not full page load)
        wait = WebDriverWait(driver, 10)
        email_field = driver.find_element(By.ID, 'user_email')
        password_field = driver.find_element(By.ID, 'user_password')
        submit_btn = wait.until(EC.element_to_be_clickable((By.ID, 'submitBtn')))

        # Perform login actions
        email_field.send_keys(username)
        password_field.send_keys(password)
        submit_btn.click()

        # Handle 2FA with optimized waiting
        otp_code = get_otp(secret_key)
        letters = ['a', 'b', 'c', 'd', 'e', 'f']
        
        try:
            # Wait for OTP fields to be present (not necessarily visible)
            wait.until(EC.presence_of_element_located((By.ID, 'code_a')))
            
            # Fill OTP quickly
            for i in range(6):
                code_field = driver.find_element(By.ID, f"code_{letters[i]}")
                code_field.clear()
                code_field.send_keys(otp_code[i])
            
            # Submit 2FA
            commit_btn = wait.until(EC.element_to_be_clickable((By.NAME, 'commit')))
            commit_btn.click()
                        
        except Exception as e:
            logging.error(e,exc_info=True)
            raise Exception("2FA is not setup properly or timed out")
            
        return driver

    except Exception as e:
        logging.error(f"Login failed: {str(e)}", exc_info=True)
        if 'driver' in locals():
            driver.quit()
        raise Exception(f"Login failed: {str(e)}")



def submit_claim_data_test(url,user,password_our,secret_key,modifier,is_submit):
    try:
        driver = login_health_app(url,user,password_our,secret_key)
    except Exception as e:
        raise Exception(e)
    try:
        driver.get(url+"/edit")
        time.sleep(4)
        for y in range(len(modifier)):
            for x in range(len(modifier[y])):
                hit = f"claim[serviceLines][{y}][procedureModifiers][{x}]"
                element = driver.find_element(By.NAME,f"claim[serviceLines][{y}][procedureModifiers][{x}]")
                element.send_keys(modifier[y][x])

        time.sleep(2)
        save_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Save')]")
        save_button.click()
        time.sleep(2)
        if is_submit:
            submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Submit')]").click()
            time.sleep(2)
        return "successful"
    except Exception as e:
        logging.error(e,exc_info=True)
        raise Exception(e)
    finally:
        cleanup_driver(driver)


# modifier = [["GT","HO"],[],["MG","GH"],[],[],["KJ","RT","DR"]]
# submit_claim_data_test("https://secure.simplepractice.com/clients/614d1e186e1f0d8f/insurance_claims/216180619","info+1@gina4med.com","Rakovski@345",
# "AW7WGIL4BFQO6B3K2TGDKCMXEJ7EHLI2NV7B4RP7IJBBTH5IDQKA",modifier,True)