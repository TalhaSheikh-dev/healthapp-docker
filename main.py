
from bs4 import BeautifulSoup,SoupStrainer
from selenium import webdriver
import json

def video_scrapper(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path="/home/talhasheikh/Documents/health_scraper/chromedriver",chrome_options=options)
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
    
    print("grea")
    with open("table_data.json","w") as f:
        json.dump(data,f,indent=4)



client_id = "88672929"
url = "https://secure.simplepractice.com/clients/83cdf3a00620ca58/insurance_claims/"+client_id
video_scrapper(url)
