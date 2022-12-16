
#python
from selenium import webdriver
import os
import time
import ast
import json
from selenium.webdriver.common.by import By
import requests

def payer_data(user,password_our,count):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')	
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1400,900")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
   
    url = "https://secure.simplepractice.com/clients"
    driver.get(url)

    username = driver.find_element_by_id('user_login')
    username.send_keys(user)
    password = driver.find_element_by_id('user_password')
    password.send_keys(password_our)
    form = driver.find_element_by_id('new_user')
    form.submit()
    main = []
    for counter in range(count,count+10):
        driver.get("https://secure.simplepractice.com/frontend/insurance-plans? filter[search]=&filter[providerFilter]=search&include=insurancePayer,eligiblePayer,practicePayerAddresses,practiceInsurancePayers&page[number]={}&page[size]=50".format(counter))
        counter = counter+1
        a = json.loads(driver.find_element_by_tag_name("pre").text)
        print(counter)
        if len(a["data"]) ==0:
            break
        for x in a["data"]:
            dictionary = {}
            dictionary["id"] = str(x["attributes"]["insuranceProviderId"])
            dictionary["payer_name"] = x["attributes"]["name"]
            dictionary["payer_id"] = x["attributes"]["nameWithPayer"].split("(")[-1][:-1]
            for j in a["included"]:
                if j["type"] == "insurancePayers" and j["id"]==dictionary["id"]:
                    try:
                        dictionary["city"] = j["attributes"]["defaultAddress"]["city"]
                        dictionary["zipcode"] = j["attributes"]["defaultAddress"]["zipcode"]
                        dictionary["address"] = j["attributes"]["defaultAddress"]["address"]
                        dictionary["state"] = j["attributes"]["defaultAddress"]["state"]
                    except:
                        dictionary["city"] = ""
                        dictionary["address"] = ""
                        dictionary["state"] = ""
                        dictionary["zipcode"] = ""
                
                    main.append(dictionary)
                    break
    return main
    
    
def get_all_client(user,password_our):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1400,900")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
   
    url = "https://secure.simplepractice.com/clients"
    driver.get(url)

    username = driver.find_element_by_id('user_login')
    username.send_keys(user)
    password = driver.find_element_by_id('user_password')
    password.send_keys(password_our)
    form = driver.find_element_by_id('new_user')
    form.submit()

    url = '''https://secure.simplepractice.com/frontend/base-clients?     fields[baseClients]=emails,clinician,clientPortalSettings,clientReferralSource,reciprocalClientRelationships,insuranceInfos,clientRelationships,phones,addresses,clientAccess,permissions,hashedId,name,firstName,lastName,middleName,initials,suffix,nickname,preferredName,legalName,defaultPhoneNumber,defaultEmailAddress,generalNotes,sex,genderInfo,ignoredForMerge&fields[clients]=autopayReminder,autopayInsuranceReminder,clinician,office,upcomingAppointments,latestInvoices,latestBillingDocuments,clientBillingOverview,clientAdminNote,clientDocumentRequests,viewableDocuments,channelUploadedDocuments,currentInsuranceAuthorization,insuranceAuthorizations,insuranceClaimFields,globalMonarchChannel,stripeCards,cptCodeRates,pendingAppointmentConfirmations,billingSettings,billingType,inActiveTreatment,secondaryClinicianIds,emails,clientPortalSettings,clientReferralSource,reciprocalClientRelationships,insuranceInfos,clientRelationships,phones,addresses,clientAccess,permissions,hashedId,name,firstName,lastName,middleName,initials,suffix,nickname,preferredName,legalName,defaultPhoneNumber,defaultEmailAddress,generalNotes,sex,genderInfo,ignoredForMerge,enableEmailReminders,enableOutstandingDocumentReminders,enableSmsvoiceReminders,isMinor,reminderEmail,reminderPhone&fields[clientCouples]=autopayReminder,autopayInsuranceReminder,clinician,office,upcomingAppointments,latestInvoices,latestBillingDocuments,clientBillingOverview,clientAdminNote,clientDocumentRequests,viewableDocuments,channelUploadedDocuments,currentInsuranceAuthorization,insuranceAuthorizations,insuranceClaimFields,globalMonarchChannel,stripeCards,cptCodeRates,pendingAppointmentConfirmations,billingSettings,billingType,inActiveTreatment,secondaryClinicianIds,emails,clientPortalSettings,clientReferralSource,reciprocalClientRelationships,insuranceInfos,clientRelationships,phones,addresses,clientAccess,permissions,hashedId,name,firstName,lastName,middleName,initials,suffix,nickname,preferredName,legalName,defaultPhoneNumber,defaultEmailAddress,generalNotes,sex,genderInfo,ignoredForMerge,firstNameLastInitial&fields[insuranceInfo]=hieEnabled&filter[thisType]=Client,ClientCouple&include=phones,emails,insuranceInfos,clientRelationships.client,clientRelationships.relatedClient.phones,clientRelationships.relatedClient.emails,reciprocalClientRelationships.client.phones,reciprocalClientRelationships.client.emails,reciprocalClientRelationships.relatedClient&page[number]='''
    url_2 = '''&page[size]=50&sort=lastName'''
    full = []
    i = 1
    while True:
        response = driver.get(url+str(i)+url_2)
        json_data = driver.find_element_by_tag_name("body").text
        json_data = json.loads(json_data)["data"]
        if len(json_data) == 0:
            break
  
        full = full + json_data
        i = i+1
    return full
    

def convert_date(date):
    splitter = date.split("/")
    mm = splitter[0]
    dd = splitter[1]
    yyyy = splitter[2]
    
    return yyyy+"-"+mm+"-"+dd
def unbilled_create(from_date,end_date,user,password_our):

    from_date = convert_date(from_date)
    end_date = convert_date(end_date)
    url = '''https://secure.simplepractice.com/frontend/insured-clients?fields[clients]=hashedId,preferredName&filter[endDate]={}&filter[startDate]={}&include=unbilledAppointments,client,insurancePlan&page[number]={}&page[size]=50'''
    
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1400,900")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    driver.get("https://secure.simplepractice.com/users/sign_in")
    
  
    username = driver.find_element_by_id('user_login')
    username.send_keys(user)
    password = driver.find_element_by_id('user_password')
    password.send_keys(password_our)
    form = driver.find_element_by_id('new_user')
    form.submit()

    token = driver.find_element(By.CSS_SELECTOR,'meta[name="csrf-token"]').get_attribute('content')
    time.sleep(7)
    
    
    check = ["_ga","_gid","_fbp","sp_last_access","__stripe_mid","__zlcmid","user.id","_slvddv","_slvs","__stripe_sid","mp_f10ab4b365f1e746fe72d30f0e682dbf_mixpanel","user.expires_at","simplepractice-session"]
    try:
        all_cookies=driver.get_cookies();
        cookies_dict = {}    
        for cookie in all_cookies:
            cookies_dict[cookie['name']]=cookie['value']
        string = ""
        for i in check:
            string = string + i+"="+cookies_dict[i]+"; "
        string = string.strip("; ")
    except:
        time.sleep(4)
        all_cookies=driver.get_cookies();
        cookies_dict = {}    
        for cookie in all_cookies:
            try:
                cookies_dict[cookie['name']]=cookie['value']
            except:
                pass
        string = ""
        for i in check:
            string = string + i+"="+cookies_dict[i]+"; "
        string = string.strip("; ")
            
    header = {
        "user-agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "x-csrf-token":token,
        "accept":"application/vnd.api+json",
        "content-type":"application/vnd.api+json",
        "origin":"https://secure.simplepractice.com",
        "referer":"https://secure.simplepractice.com/clients/29aef6cf67198727/overview",
        "cookie":string
    }
    page_no = 1
    all_ids = []
    while True:
        loop_ids = []
        url_new = url.format(end_date,from_date,page_no)
        driver.get(url_new)
        json_data = json.loads(driver.find_element(By.CSS_SELECTOR,'pre').text)["data"]
        
        for x in json_data:
            if x["attributes"]["missingInsuranceData"] == "":
                loop_ids.append(x["relationships"]["unbilledAppointments"]["data"][0]["id"]) 
        
        if len(json_data) == 50:
            page_no = page_no+1
            all_ids = all_ids + loop_ids
            continue
        else:
            all_ids = all_ids + loop_ids
            break
            

    payload = json.dumps({"appointmentIds":all_ids,"submitClaims":False})    
    r = requests.post("https://secure.simplepractice.com/frontend/insured-clients/batch-create",data=payload,headers=header)
    
    
def id_scrapper(from_date,end_date,status,user,password_our):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1400,900")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    url = "https://secure.simplepractice.com/billings/insurance/claims?endDate={}&startDate={}&status={}".format(end_date,from_date,status)
    driver.get(url)
    username = driver.find_element_by_id('user_login')
    username.send_keys(user)
    password = driver.find_element_by_id('user_password')
    password.send_keys(password_our)
    form = driver.find_element_by_id('new_user')
    form.submit()    
    
    all_data = []
    elems = driver.find_elements_by_tag_name('tr')
    for elem in elems:
        try:
            href = elem.find_elements_by_tag_name('td')[-1].find_elements_by_tag_name('a')[0].get_attribute('href')
            first = href.split("/")[-3]
            second = href.split("/")[-1]
            dicti = {"first_id":first,"second_id":second}
            all_data.append(dicti)

        except:
            pass
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage

        elems = driver.find_elements_by_tag_name('tr')
        for elem in elems:
            try:
                href = elem.find_elements_by_tag_name('td')[-1].find_elements_by_tag_name('a')[0].get_attribute('href')
                first = href.split("/")[-3]
                second = href.split("/")[-1]
                dicti = {"first_id":first,"second_id":second}
                all_data.append(dicti)

            except:
                pass
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True
    elems = driver.find_elements_by_tag_name('tr')
    for elem in elems:
        try:
            href = elem.find_elements_by_tag_name('td')[-1].find_elements_by_tag_name('a')[0].get_attribute('href')
            first = href.split("/")[-3]
            second = href.split("/")[-1]
            dicti = {"first_id":first,"second_id":second}
            all_data.append(dicti)

        except:
            pass
    all_data = ([dict(y) for y in set(tuple(x.items()) for x in all_data)])
    return all_data
    
def id_scrapper_page(from_date,end_date,number_page,user,password_our):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1400,900")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    url = "https://secure.simplepractice.com/billings/insurance"
    driver.get(url)
    
  
    username = driver.find_element_by_id('user_login')
    username.send_keys(user)
    password = driver.find_element_by_id('user_password')
    password.send_keys(password_our)
    form = driver.find_element_by_id('new_user')
    form.submit()


    
    
    driver.get(url+"#claims")
    time.sleep(2)
    driver.find_element_by_xpath("//input[@id='insurance-claims-daterangepicker']").click()
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[1]/input").clear()
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[1]/input").send_keys(from_date)
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[2]/input").clear()
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[2]/input").send_keys(end_date)
    time.sleep(2)
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/button[1]").click()  
    time.sleep(5)
    elems = driver.find_elements_by_xpath("//a[@data-page]")

    try:
        value_all = max([int(x.get_attribute("data-page")) for x in elems])
        
        our_number = 5
        while int(number_page) >our_number:
            string = '//a[@data-page="'+str(our_number)+'"]'
            driver.find_element_by_xpath(string).click()
            our_number = our_number+4
            time.sleep(2)
    
    
        string = '//a[@data-page="'+str(number_page)+'"]'
        driver.find_element_by_xpath(string).click()
    except:
        value_all =1

        
    time.sleep(2)
    all_data = []
    elems = driver.find_elements_by_tag_name('tr')
    for elem in elems:
        try:
            href = elem.get_attribute('data-url')
            all_data.append({"first_id":href.split("/")[-3],"second_id":href.split("/")[-1]})
        except:
            pass
    driver.quit()
    return all_data,value_all

get_letter = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J",10:"K",11:"L"}
def video_scrapper(url,user,password_our):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1400,900")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    x = driver.get(url)
    
    username = driver.find_element_by_id('user_login')
    #username.send_keys('george_gina4med')
    username.send_keys(user)
    password = driver.find_element_by_id('user_password')
    #password.send_keys('Akoznaeh#88')
    password.send_keys(password_our)
    form = driver.find_element_by_id('new_user')
    form.submit()

    data = {}
    time.sleep(10)
    data["payer_id"] = driver.execute_script("return document.getElementsByName('payer[id]')[0].value")
    data["payer_name"] = (driver.execute_script("return document.getElementsByName('payer[name]')[0].value"))
    data["payer_streetLine1"] = (driver.execute_script("return document.getElementsByName('payer[address][streetLine1]')[0].value"))
    data["payer_streetLine2"] = (driver.execute_script("return document.getElementsByName('payer[address][streetLine2]')[0].value"))
    data["payer_city"] = (driver.execute_script("return document.getElementsByName('payer[address][city]')[0].value"))
    data["payer_state"] = (driver.execute_script("return document.getElementsByName('payer[address][state]')[0].value"))
    data["payer_zip"] = (driver.execute_script("return document.getElementsByName('payer[address][zip]')[0].value"))
    data["insured_id"] = (driver.execute_script("return document.getElementsByName('subscriber[id]')[0].value"))
    data["patient_lastName"] = (driver.execute_script("return document.getElementsByName('dependent[lastName]')[0].value"))
    data["patient_firstName"] = (driver.execute_script("return document.getElementsByName('dependent[firstName]')[0].value"))
    data["patient_middleName"] = (driver.execute_script("return document.getElementsByName('dependent[middleName]')[0].value"))
    data["patient_dob"] = (driver.execute_script("return document.getElementsByName('dependent[dob]')[0].value"))

    data["insured_lastName"] = (driver.execute_script("return document.getElementsByName('subscriber[lastName]')[0].value"))
    data["insured_firstName"] = (driver.execute_script("return document.getElementsByName('subscriber[firstName]')[0].value"))
    data["insured_middleName"] = (driver.execute_script("return document.getElementsByName('subscriber[middleName]')[0].value"))   
    
    
    data["patient_streetLine1"] = (driver.execute_script("return document.getElementsByName('dependent[address][streetLine1]')[0].value"))
    data["patient_streetLine2"] = (driver.execute_script("return document.getElementsByName('dependent[address][streetLine2]')[0].value"))
    data["patient_state"] = (driver.execute_script("return document.getElementsByName('dependent[address][state]')[0].value"))
    data["patient_city"] = (driver.execute_script("return document.getElementsByName('dependent[address][city]')[0].value"))
    data["patient_zip"] = (driver.execute_script("return document.getElementsByName('dependent[address][zip]')[0].value"))
    data["patient_telephone"] = (driver.execute_script("return document.getElementsByName('dependent[phoneNumber]')[0].value"))
    try:
        data["patient_id"] = (driver.execute_script("return document.getElementsByName('dependent[id]')[0].value"))
    except:
        data["patient_id"] = ""

    data["insured_streetLine1"] = (driver.execute_script("return document.getElementsByName('subscriber[address][streetLine1]')[0].value"))
    data["insured_streetLine2"] = (driver.execute_script("return document.getElementsByName('subscriber[address][streetLine2]')[0].value"))
    data["insured_city"] = (driver.execute_script("return document.getElementsByName('subscriber[address][city]')[0].value"))   
    data["insured_state"] = (driver.execute_script("return document.getElementsByName('subscriber[address][state]')[0].value"))   
    data["insured_zip"] = (driver.execute_script("return document.getElementsByName('subscriber[address][zip]')[0].value"))   
    data["insured_number"] = (driver.execute_script("return document.getElementsByName('subscriber[phoneNumber]')[0].value"))   

    data["otherinsured_lastName"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][lastName]')[0].value"))
    data["otherinsured_firstName"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][firstName]')[0].value"))
    data["otherinsured_mi"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][middleName]')[0].value")) 
    

    
    data["otherinsured_relationship"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][relationship]')[0].options[document.getElementsByName('otherPayers[0][subscriber][relationship]')[0].selectedIndex].text"))
       
    data["otherinsured_policy"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][groupId]')[0].value"))   
    data["otherinsured_insuredid"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][id]')[0].value"))  
    data["otherinsured_indicatorcode"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][claimFilingIndicator]')[0].options[document.getElementsByName('otherPayers[0][claimFilingIndicator]')[0].selectedIndex].text"))
    
    data["otherinsured_insurancePlanName"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][name]')[0].value"))
    data["otherinsured_insuranceTypeCode"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][insuranceTypeCode]')[0].options[document.getElementsByName('otherPayers[0][subscriber][insuranceTypeCode]')[0].selectedIndex].text"))   
    data["otherinsured_resSequence"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][responsibilitySequence]')[0].options[document.getElementsByName('otherPayers[0][responsibilitySequence]')[0].selectedIndex].text"))   
    data["otherinsured_payerId"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][id]')[0].value"))   
    
    data["patient_autoAccidentState"] = (driver.execute_script("return document.getElementsByName('claim[autoAccidentState]')[0].value")) 
    
    data["patient_claimCode"] = (driver.execute_script("return document.getElementsByName('code')[0].value")) 
    
    data["insured_policy"] = (driver.execute_script("return document.getElementsByName('subscriber[groupId]')[0].value")) 
    data["insured_dob"] = (driver.execute_script("return document.getElementsByName('subscriber[dob]')[0].value")) 
    data["insured_planName"] = (driver.execute_script("return document.getElementsByName('subscriber[groupName]')[0].value")) 
    
    
    data["dataOfIllness"] = (driver.execute_script("return document.getElementsByName('claim[additionalClaimInfo]')[0].value")) 
    data["dataOfIllness_qual"] = (driver.execute_script("return document.getElementsByName('claim[additionalClaimInfoCode]')[0].options[document.getElementsByName('claim[additionalClaimInfoCode]')[0].selectedIndex].text "))
   
    data["lastWorkData"] = (driver.execute_script("return document.getElementsByName('claim[lastWorkedDate]')[0].value")) 
    data["workReturnDate"] = (driver.execute_script("return document.getElementsByName('claim[workReturnDate]')[0].value"))  
    

    data["provider"] = (driver.execute_script("return document.getElementsByName('box17ProviderOption')[0].options[document.getElementsByName('box17ProviderOption')[0].selectedIndex].text")) 
    data["provider_lastName"] = (driver.execute_script("return document.getElementsByName('box17Provider[lastName]')[0].value"))  
    data["provider_firstName"] = (driver.execute_script("return document.getElementsByName('box17Provider[firstName]')[0].value")) 
    data["provider_middleName"] = (driver.execute_script("return document.getElementsByName('box17Provider[middleName]')[0].value"))  

    data["secondayIdType"] = (driver.execute_script("return document.getElementsByName('box17Provider[secondaryIdType]')[0].options[document.getElementsByName('box17Provider[secondaryIdType]')[0].selectedIndex].text"))     
    data["secondaryId"] = (driver.execute_script("return document.getElementsByName('box17Provider[secondaryId]')[0].value"))        
    data["npi"] = (driver.execute_script("return document.getElementsByName('box17Provider[npi]')[0].value"))         
    
    data["hospitalizationDate_current_from"] = (driver.execute_script("return document.getElementsByName('claim[admissionDate]')[0].value")) 
    data["hospitalizationDate_current_to"] = (driver.execute_script("return document.getElementsByName('claim[dischargeDate]')[0].value")) 
    


    data["additionalClaimInfo"] = (driver.execute_script("return document.getElementsByName('claim[additionalClaimInfo]')[0].value"))  
    data["additionalClaimInfoCode"] = (driver.execute_script("return document.getElementsByName('claim[additionalClaimInfoCode]')[0].options[document.getElementsByName('claim[additionalClaimInfoCode]')[0].selectedIndex].text"))   
 
    data["supplementalClaim_typeCode"] = (driver.execute_script("return document.getElementsByName('claim[reportTypeCode]')[0].value"))  
    data["supplementalClaim_transCode"] = (driver.execute_script("return document.getElementsByName('claim[reportTransmissionCode]')[0].value"))  
    data["supplementalClaim_attachmentId"] = (driver.execute_script("return document.getElementsByName('claim[attachmentId]')[0].value"))    
    data["outsideLabCharges"] = (driver.execute_script("return document.getElementsByName('claim[outsideLabCharges]')[0].value"))
    
    data["icdInd"] = (driver.execute_script("return document.getElementsByName('claim[icdIndicator]')[0].value"))
    data["icdA"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][0]')[0].value"))
    data["icdB"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][1]')[0].value"))
    data["icdC"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][2]')[0].value"))
    data["icdD"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][3]')[0].value"))
    data["icdE"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][4]')[0].value"))
    data["icdF"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][5]')[0].value"))
    data["icdG"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][6]')[0].value"))
    data["icdH"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][7]')[0].value"))
    data["icdI"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][8]')[0].value"))
    data["icdJ"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][9]')[0].value"))
    data["icdK"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][10]')[0].value"))
    data["icdL"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][11]')[0].value"))

    data["resubmission_refNo"] = (driver.execute_script("return document.getElementsByName('claim[payerControlNumber]')[0].value"))
    data["priorAuthNo"] = (driver.execute_script("return document.getElementsByName('claim[priorAuthorizationNumber]')[0].value"))
    data["CLIANo"] = (driver.execute_script("return document.getElementsByName('claim[cliaNumber]')[0].value"))

    
    data["billingProvider_taxId"] = (driver.execute_script("return document.getElementsByName('billingProvider[taxId]')[0].value"))
    data["claim_totalCharge"] = (driver.execute_script("return document.getElementsByName('claim[totalCharge]')[0].value"))
    data["claim_patientAmountPaid"] = (driver.execute_script("return document.getElementsByName('claim[patientAmountPaid]')[0].value"))
    data["claim_claimSignatureDate"] = (driver.execute_script("return document.getElementsByName('claim[claimSignatureDate]')[0].value"))
    data["serviceFacility_name"] = (driver.execute_script("return document.getElementsByName('serviceFacility[name]')[0].value"))
    data["serviceFacility_streetLine1"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][streetLine1]')[0].value"))
    data["serviceFacility_streetLine2"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][streetLine2]')[0].value"))
    data["serviceFacility_city"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][city]')[0].value"))
    data["serviceFacility_state"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][state]')[0].value"))
    data["serviceFacility_zip"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][zip]')[0].value"))
    data["serviceFacility_npi"] = (driver.execute_script("return document.getElementsByName('serviceFacility[npi]')[0].value"))
    
    
    data["billingProvider_phoneNumber"] = (driver.execute_script("return document.getElementsByName('billingProvider[phoneNumber]')[0].value"))
    try:
        data["billingProvider_lastName"] = (driver.execute_script("return document.getElementsByName('billingProvider[lastName]')[0].value"))
        data["billingProvider_firstName"] = (driver.execute_script("return document.getElementsByName('billingProvider[firstName]')[0].value"))
        data["billingProvider_middleName"] = (driver.execute_script("return document.getElementsByName('billingProvider[middleName]')[0].value"))
        
    except:
        data["billingProvider_organization"] = (driver.execute_script("return document.getElementsByName('billingProvider[organizationName]')[0].value"))
    data["billingProvider_streetLine1"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][streetLine1]')[0].value"))
    data["billingProvider_streetLine2"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][streetLine2]')[0].value"))
    data["billingProvider_city"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][city]')[0].value"))
    data["billingProvider_state"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][state]')[0].value"))
    data["billingProvider_zip"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][zip]')[0].value"))
    data["billingProvider_npi"] = (driver.execute_script("return document.getElementsByName('billingProvider[npi]')[0].value"))
    data["billingProvider_taxonomyCode"] = (driver.execute_script("return document.getElementsByName('billingProvider[taxonomyCode]')[0].value"))

########################################################################

    data["patient_gender"] = "" 
    if (driver.execute_script("return document.getElementsByName('dependent[gender]')[0].checked")):
        data["patient_gender"] = "m"
    if (driver.execute_script("return document.getElementsByName('dependent[gender]')[1].checked")):
        data["patient_gender"] = "f"

    data["patient_employment"] = "" 
    if (driver.execute_script("return document.getElementsByName('claim[relatedToEmployment]')[0].checked")):
        data["patient_employment"] = "yes"
    if (driver.execute_script("return document.getElementsByName('claim[relatedToEmployment]')[1].checked")):
        data["patient_employment"] = "no"
        
    #new addition
    data["patient_relationship_to_insecured"] = "" 
    if (driver.execute_script("return document.getElementsByName('dependent[relationship]')[0].checked")):
        data["patient_relationship_to_insecured"] = "self"
    if (driver.execute_script("return document.getElementsByName('dependent[relationship]')[1].checked")):
        data["patient_relationship_to_insecured"] = "spouse"
    if (driver.execute_script("return document.getElementsByName('dependent[relationship]')[2].checked")):
        data["patient_relationship_to_insecured"] = "child"
    if (driver.execute_script("return document.getElementsByName('dependent[relationship]')[3].checked")):
        data["patient_relationship_to_insecured"] = "other"        

    data["auto_accident"] = "" 
    if (driver.execute_script("return document.getElementsByName('claim[autoAccident]')[0].checked")):
        data["auto_accident"] = "yes"
    if (driver.execute_script("return document.getElementsByName('claim[autoAccident]')[1].checked")):
        data["auto_accident"] = "no"


    data["other_accident"] = "" 
    if (driver.execute_script("return document.getElementsByName('claim[otherAccident]')[0].checked")):
        data["other_accident"] = "yes"
    if (driver.execute_script("return document.getElementsByName('claim[otherAccident]')[1].checked")):
        data["other_accident"] = "no"


    data["insured_gender"] = "" 
    if (driver.execute_script("return document.getElementsByName('subscriber[gender]')[0].checked")):
        data["insured_gender"] = "m"
    if (driver.execute_script("return document.getElementsByName('subscriber[gender]')[1].checked")):
        data["insured_gender"] = "f"

    data["anyother_healthPlan"] = "" 
    if (driver.execute_script("return document.getElementsByName('otherPayer')[0].checked")):
        data["anyother_healthPlan"] = "yes"
    if (driver.execute_script("return document.getElementsByName('otherPayer')[1].checked")):
        data["anyother_healthPlan"] = "no"

    data["claim_directPaymentAuthorized"] = ""
    if (driver.execute_script("return document.getElementsByName('claim[directPaymentAuthorized]')[0].checked")):
        data["claim_directPaymentAuthorized"] = "yes"    
        
        
    data["claim_outsideLab"] = "" 
    if (driver.execute_script("return document.getElementsByName('claim[outsideLab]')[0].checked")):
        data["claim_outsideLab"] = "yes"
    if (driver.execute_script("return document.getElementsByName('claim[outsideLab]')[1].checked")):
        data["claim_outsideLab"] = "no"
        
    data["claim_frequency"] = "" 
    if (driver.execute_script("return document.getElementsByName('claim[frequency]')[0].checked")):
        data["claim_frequency"] = "original"
    if (driver.execute_script("return document.getElementsByName('claim[frequency]')[1].checked")):
        data["claim_frequency"] = "resubmission"
    if (driver.execute_script("return document.getElementsByName('claim[frequency]')[2].checked")):
        data["claim_frequency"] = "cancel"


    data["billingProvider_taxIdType"] = "" 
    if (driver.execute_script("return document.getElementsByName('billingProvider[taxIdType]')[0].checked")):
        data["billingProvider_taxIdType"] = "SSN"
    if (driver.execute_script("return document.getElementsByName('billingProvider[taxIdType]')[1].checked")):
        data["billingProvider_taxIdType"] = "EIN"
        
    data["claim_acceptAssignmentCode"] = "" 
    if (driver.execute_script("return document.getElementsByName('claim[acceptAssignmentCode]')[0].checked")):
        data["claim_acceptAssignmentCode"] = "yes"
    if (driver.execute_script("return document.getElementsByName('claim[acceptAssignmentCode]')[1].checked")):
        data["claim_acceptAssignmentCode"] = "no"
        
        
        
    data["billingProvider_entity"] = "" 
    if (driver.execute_script("return document.getElementsByName('billingProvider[entity]')[0].checked")):
        data["billingProvider_entity"] = "individual"
    if (driver.execute_script("return document.getElementsByName('billingProvider[entity]')[1].checked")):
        data["billingProvider_entity"] = "organization"
        
             	
#########################################################################################


    for i in range(0,6):
        key = "claim_serviceLines_" + str(i) +"_serviceDateFrom" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][serviceDateFrom]')[0].value"
        check_data = (driver.execute_script(name))
        
        if check_data == "":
            break
        data[key] = check_data 
        key = "claim_serviceLines_" + str(i) +"_serviceDateTo" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][serviceDateTo]')[0].value"
        data[key] = (driver.execute_script(name))

        key = "claimserviceLines_" + str(i) +"_placeOfService" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][placeOfService]')[0].options[document.getElementsByName('claim[serviceLines][" + str(i)+"][placeOfService]')[0].selectedIndex].text"      
        data[key] = (driver.execute_script(name)) 


        key = "claimserviceLines_" + str(i) +"_procedureCode" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][procedureCode]')[0].value"
        data[key] = (driver.execute_script(name))
    
    
        key = "claimserviceLines_" + str(i) +"_description" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][description]')[0].value"
        data[key] = (driver.execute_script(name))      
         
        lit_let = []
        for ss in range(0,9):
            
            name = "return document.getElementsByClassName('dc-pointers-table')["+str(i)+"].getElementsByTagName('input')["+str(ss)+"].checked"
            name = (driver.execute_script(name))  

            if name == True:

                letter = get_letter[ss]
                lit_let.append(letter)
    
        key = "claim_serviceLines_"+str(i)+ "_Diagnose_pointer"  
        data[key] = lit_let
        
        for x in range(0,4):
            key = "claim_serviceLines_" + str(i) +"_procedureModifiers_"+str(x) 	
            name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][procedureModifiers]["+str(x)+"]')[0].value"
            data[key] = (driver.execute_script(name))
   
        key = "claimserviceLines_" + str(i) +"_chargeAmount" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][chargeAmount]')[0].value"     
        data[key] = (driver.execute_script(name))

        key = "claimserviceLines_" + str(i) +"_units" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][units]')[0].value"    
        data[key] = (driver.execute_script(name))
    
        key = "claimserviceLines_" + str(i) +"_epsdtIndicator" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][epsdtIndicator]')[0].value"
        data[key] = (driver.execute_script(name))

        key = "claimserviceLines_" + str(i) +"_renderingProviderlastName" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][renderingProvider][lastName]')[0].value"
        data[key] = (driver.execute_script(name))

        key = "claimserviceLines_" + str(i) +"_renderingProviderfirstName" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][renderingProvider][firstName]')[0].value"
        data[key] = (driver.execute_script(name))

        key = "claimserviceLines_" + str(i) +"_renderingProvidernpi" 	
        name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][renderingProvider][npi]')[0].value"
        data[key] = (driver.execute_script(name))

    driver.quit()
    return data




