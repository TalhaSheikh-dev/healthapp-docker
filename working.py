

from selenium import webdriver
import json
import os
import time
import pathlib
def video_scrapper(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    x = driver.get(url)
    
    
    username = driver.find_element_by_id('user_login')
    x = username.send_keys('george_gina4med')
    password = driver.find_element_by_id('user_password')
    x = password.send_keys('Akoznaeh#88')
    form = driver.find_element_by_id('new_user')
    x = form.submit()

    res = driver.execute_script("return document.documentElement.outerHTML")   

    
    time.sleep(5)
    driver.find_element_by_id("ember92").click()
    time.sleep(5)
    driver.find_elements_by_class_name("button-link")[1].click()
    

    opts = sorted(pathlib.Path('../../').glob('**/*.pdf'))
    a = str(opts[0])
    
    return a

#    with open("table_data.json","w") as f:
#        json.dump(data,f,indent=4)




