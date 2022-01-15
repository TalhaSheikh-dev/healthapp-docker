
from bs4 import BeautifulSoup,SoupStrainer
from selenium import webdriver
import json
import os

def video_scrapper(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    driver.get(url)
    
    
    username = driver.find_element_by_id('user_login')
    username.send_keys('george_gina4med')
    password = driver.find_element_by_id('user_password')
    password.send_keys('Akoznaeh#88')
    form = driver.find_element_by_id('new_user')
    form.submit()

    res = driver.execute_script("return document.documentElement.outerHTML")
    soup = BeautifulSoup(res, 'lxml')    

    driver.quit()
    html_str = str(soup)
    start = end = 0
    start = html_str.find("//<![CDATA[")+43
    end = html_str.find("//]]>")-2
    data = html_str[start:end]
    #print(data)
    return data

#    with open("table_data.json","w") as f:
#        json.dump(data,f,indent=4)




