from selenium import webdriver
import os
import time
import ast
import json
from selenium.webdriver.common.by import By
import requests
import pandas as pd
import json
import numpy as np
from datetime import datetime, timedelta

dir_path = os.path.dirname(os.path.realpath(__file__))

rename_dict = {'Date':'claim_serviceLines_0_serviceDateFrom',
       'Service Code':'claimserviceLines_0_procedureCode', 'POS':'claimserviceLines_0_placeOfService', 'Units':'claimserviceLines_0_units', 'Last Name':'patient_lastName',
       'First Name':'patient_firstName', 'DOB':'patient_dob', 'Patient Member ID':'insured_id',
       'Clinician NPI':'claimserviceLines_0_renderingProvidernpi',
       'Primary Insurer Name':'payer_name',
       'Primary Diagnosis':'icdA','Rate':'claimserviceLines_0_chargeAmount',
       'Modifier Code 1':'claim_serviceLines_0_procedureModifiers_0', 'Modifier Code 2':'claim_serviceLines_0_procedureModifiers_1',
       'Modifier Code 3':'claim_serviceLines_0_procedureModifiers_2', 'Modifier Code 4':'claim_serviceLines_0_procedureModifiers_3'}


drop_columns = ['Type','Appointment Type','Billing Method','Payment Type','Service Description','Clinician Type','Bill as Supervisor','Supervisor Name','Supervisor NPI','Location',
               'Primary Insurer Group', 'In Network', 'Secondary Insurer Name','Secondary Insurer Group', 'Note Status',
               'Payment Assigned to Practice' , 'Patient Amount Due','Patient Amount Paid', 'Patient Unassigned Credit',
               'Patient Balance Status', 'Insurance Amount Due','Insurance Amount Paid', 'Insurance Unassigned Credit','Insurance Balance Status',
               'Documents Created', 'Comments','Clinician Name'
               ]


all_columns = ['claim_serviceLines_3_Diagnose_pointer', 'claimserviceLines_3_procedureCode', 'claimserviceLines_1_units', 'patient_streetLine1', 'patient_telephone', 'claimserviceLines_1_placeOfService', 'claim_serviceLines_4_procedureModifiers_0', 'icdI', 'claim_serviceLines_1_serviceDateTo', 'claimserviceLines_5_placeOfService', 'claimserviceLines_2_procedureCode', 'claimserviceLines_2_placeOfService', 'claim_serviceLines_4_procedureModifiers_1', 'claim_serviceLines_4_serviceDateFrom', 'patient_city', 'claimserviceLines_2_chargeAmount', 'icdB', 'claim_serviceLines_4_serviceDateTo', 'claimserviceLines_5_procedureCode', 'claim_serviceLines_5_serviceDateFrom', 'claim_serviceLines_1_procedureModifiers_0', 'claim_serviceLines_3_procedureModifiers_0', 'claimserviceLines_4_placeOfService', 'claim_serviceLines_3_serviceDateTo', 'claim_serviceLines_3_serviceDateFrom', 'claim_serviceLines_0_serviceDateTo', 'claim_serviceLines_2_Diagnose_pointer', 'claim_serviceLines_5_serviceDateTo', 'claimserviceLines_1_procedureCode', 'claimserviceLines_3_placeOfService', 'claimserviceLines_1_chargeAmount', 'claim_serviceLines_4_procedureModifiers_2', 'claim_serviceLines_1_Diagnose_pointer', 'claim_serviceLines_1_procedureModifiers_2', 'icdL', 'patient_zip', 'claim_serviceLines_2_procedureModifiers_3', 'icdJ', 'claim_serviceLines_2_serviceDateTo', 'claim_serviceLines_5_Diagnose_pointer', 'claim_serviceLines_2_procedureModifiers_0', 'claimserviceLines_5_units', 'icdK', 'claim_serviceLines_3_procedureModifiers_3', 'claim_serviceLines_2_procedureModifiers_1', 'payer_id', 'claimserviceLines_5_chargeAmount', 'icdH', 'icdD', 'claim_serviceLines_5_procedureModifiers_3', 'claim_serviceLines_5_procedureModifiers_1', 'claim_serviceLines_1_serviceDateFrom', 'patient_state', 'claimserviceLines_3_chargeAmount', 'claimserviceLines_4_chargeAmount', 'claim_serviceLines_1_procedureModifiers_3', 'claimserviceLines_3_units', 'claim_serviceLines_4_procedureModifiers_3', 'patient_middleName', 'claim_serviceLines_0_Diagnose_pointer', 'claim_serviceLines_3_procedureModifiers_2', 'claim_serviceLines_2_procedureModifiers_2', 'claimserviceLines_2_units', 'claim_serviceLines_3_procedureModifiers_1', 'patient_gender', 'claimserviceLines_4_units', 'claim_serviceLines_4_Diagnose_pointer', 'icdF', 'claim_serviceLines_2_serviceDateFrom', 'icdC', 'claim_serviceLines_5_procedureModifiers_0', 'claimserviceLines_4_procedureCode', 'claim_serviceLines_1_procedureModifiers_1', 'claim_serviceLines_5_procedureModifiers_2', 'icdE', 'patient_streetLine2', 'icdG']


def add_one_day(date_string):
    """
    Adds one day to the given date string.

    Parameters:
    date_string (str): A date string in the format 'YYYY-MM-DD'

    Returns:
    str: A new date string with one day added
    """
    date_object = datetime.strptime(date_string, '%Y-%m-%d')
    new_date_object = date_object + timedelta(days=1)
    new_date_string = new_date_object.strftime('%Y-%m-%d')
    return new_date_string

def process_date(date):
    year,month,day = date.split("-")
    month = month.lstrip("0")
    day = day.lstrip("0")
    return month,day,year
    
def process_df(df):

    length = len(df)
    df = df.drop(drop_columns, axis=1)
    df['Service Code'] = df['Service Code'].fillna(-1).astype(int).astype(str).replace("-1","")
    df['Clinician NPI'] = df['Clinician NPI'].fillna(-1).astype(np.int64).astype(str).replace("-1","")
    df['Rate'] = df['Rate'].astype(float, errors='ignore') 
    df = (df.replace(r'^\s*$', np.nan, regex=True))
    df.rename(columns = rename_dict, inplace = True)
    df["claim_serviceLines_0_serviceDateFrom"] = df["claim_serviceLines_0_serviceDateFrom"].dt.strftime('%Y-%m-%d')
    df["patient_dob"] =  pd.to_datetime(df["patient_dob"], infer_datetime_format=True)
    df["patient_dob"] = df["patient_dob"].dt.strftime('%Y-%m-%d')
    df["Date"] = df["claim_serviceLines_0_serviceDateFrom"]
    for i in all_columns:
        df[i] = [np.nan]*length

    return df.to_json(orient="records") 

def therapynotes_claims_data(code, user_name,pass_word, date_start,date_end):
    
    s_m,s_d,s_y = process_date(date_start)
    e_m,e_d,e_y = process_date(date_end)

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')	
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1400,900")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    prefs = {"download.default_directory" : dir_path}
    options.add_experimental_option("prefs",prefs)   
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
       
    url = f"https://www.therapynotes.com/app/login/{code}/"
    driver.get(url)
    time.sleep(2)
    username = driver.find_element(By.ID,'Login__UsernameField')
    username.send_keys(user_name)
    password = driver.find_element(By.ID,'Login__Password')
    password.send_keys(pass_word)
    form = driver.find_element(By.ID,'Login__LogInButton')
    form.submit()
    url_to_hit = f"https://www.therapynotes.com/app/billing/#StatementPayments=false&StatementDirectPayments=false&StatementInNetworkInsurancePayments=false&StatementOutOfNetworkInsurancePayments=false&StatementMinimumDate={s_m}%2f{s_d}%2f{s_y}&StatementMaximumDate={e_m}%2f{e_d}%2f{e_y}&StatementFilterMaximumDate={e_m}%2f{e_d}%2f{e_y}"
    time.sleep(2)
    driver.get(url_to_hit)
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/form/div[5]/div/main/div[2]/div/div[3]/div/div[2]/div/div/div[1]/a").click();
    time.sleep(2)
    out = driver.find_element(By.XPATH,"/html/body/form/div[3]/div/div/div/div/a").get_attribute("href")
    driver.get(out)  
    time.sleep(2)  
    
    files = os.listdir(dir_path)
    file_to = [x for x in files if x.endswith("xlsx")]
    df_path = os.path.join(dir_path,file_to[0])
    df = pd.read_excel(df_path)[:5]
    output = process_df(df)
    os.remove(df_path) 
    return output 
    
           
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

    username = driver.find_element(By.ID,'user_email')
    username.send_keys(user)
    password = driver.find_element(By.ID,'user_password')
    password.send_keys(password_our)
    form = driver.find_element(By.ID,'submitBtn')
    form.submit()
    main = []
    for counter in range(count,count+10):
        driver.get("https://secure.simplepractice.com/frontend/insurance-plans? filter[search]=&filter[providerFilter]=search&include=insurancePayer,eligiblePayer,practicePayerAddresses,practiceInsurancePayers&page[number]={}&page[size]=50".format(counter))
        counter = counter+1
        a = json.loads(driver.find_element(By.TAG_NAME,"pre").text)
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

    username = driver.find_element(By.ID,'user_email')
    username.send_keys(user)
    password = driver.find_element(By.ID,'user_password')
    password.send_keys(password_our)
    form = driver.find_element(By.ID,'submitBtn')
    form.submit()

    url = '''https://secure.simplepractice.com/frontend/base-clients?fields[baseClients]=emails,clinician,clientPortalSettings,clientReferralSource,reciprocalClientRelationships,insuranceInfos,clientRelationships,phones,addresses,clientAccess,permissions,hashedId,name,firstName,lastName,middleName,initials,suffix,nickname,preferredName,legalName,defaultPhoneNumber,defaultEmailAddress,generalNotes,sex,genderInfo,ignoredForMerge&fields[clients]=autopayReminder,autopayInsuranceReminder,clinician,office,upcomingAppointments,latestInvoices,latestBillingDocuments,clientBillingOverview,clientAdminNote,clientDocumentRequests,viewableDocuments,channelUploadedDocuments,currentInsuranceAuthorization,insuranceAuthorizations,insuranceClaimFields,globalMonarchChannel,stripeCards,cptCodeRates,pendingAppointmentConfirmations,billingSettings,billingType,inActiveTreatment,secondaryClinicianIds,emails,clientPortalSettings,clientReferralSource,reciprocalClientRelationships,insuranceInfos,clientRelationships,phones,addresses,clientAccess,permissions,hashedId,name,firstName,lastName,middleName,initials,suffix,nickname,preferredName,legalName,defaultPhoneNumber,defaultEmailAddress,generalNotes,sex,genderInfo,ignoredForMerge,enableEmailReminders,enableOutstandingDocumentReminders,enableSmsvoiceReminders,isMinor,reminderEmail,reminderPhone&fields[clientCouples]=autopayReminder,autopayInsuranceReminder,clinician,office,upcomingAppointments,latestInvoices,latestBillingDocuments,clientBillingOverview,clientAdminNote,clientDocumentRequests,viewableDocuments,channelUploadedDocuments,currentInsuranceAuthorization,insuranceAuthorizations,insuranceClaimFields,globalMonarchChannel,stripeCards,cptCodeRates,pendingAppointmentConfirmations,billingSettings,billingType,inActiveTreatment,secondaryClinicianIds,emails,clientPortalSettings,clientReferralSource,reciprocalClientRelationships,insuranceInfos,clientRelationships,phones,addresses,clientAccess,permissions,hashedId,name,firstName,lastName,middleName,initials,suffix,nickname,preferredName,legalName,defaultPhoneNumber,defaultEmailAddress,generalNotes,sex,genderInfo,ignoredForMerge,firstNameLastInitial&fields[insuranceInfo]=hieEnabled&filter[thisType]=Client,ClientCouple&include=phones,emails,insuranceInfos,clientRelationships.client,clientRelationships.relatedClient.phones,clientRelationships.relatedClient.emails,reciprocalClientRelationships.client.phones,reciprocalClientRelationships.client.emails,reciprocalClientRelationships.relatedClient&page[number]='''
    url_2 = '''&page[size]=50&sort=lastName'''
    full = []
    i = 1
    while True:
        response = driver.get(url+str(i)+url_2)
        json_data = driver.find_element(By.TAG_NAME,"body").text
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

    if "/" in from_date:
        from_date = convert_date(from_date)
        end_date = convert_date(end_date)
    

    url = '''https://secure.simplepractice.com/frontend/insured-clients?fields%5Bclients%5D=hashedId%2CinsuranceBillingSubtype%2CpreferredName%2CinsuranceInfos&fields%5BteamMembers%5D=name%2Csuffix%2CfirstName%2ClastName%2Croles&filter%5BendDate%5D={}&filter%5BstartDate%5D={}&include=unbilledAppointments.client.insuranceInfos.insurancePlan.practiceInsurancePayers%2CunbilledAppointments.clinician%2Cclient%2CinsurancePlan%2CunbilledAppointments.appointmentClients.client.insuranceInfos.insurancePlan.practiceInsurancePayers%2CunbilledAppointments.appointmentClients.appointment&page%5Bnumber%5D={}&page%5Bsize%5D=50'''

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1400,900")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)

    driver.get("https://secure.simplepractice.com/users/sign_in")
    
  
    username = driver.find_element(By.ID,'user_email')
    username.send_keys(user)
    password = driver.find_element(By.ID,'user_password')
    password.send_keys(password_our)
    form = driver.find_element(By.ID,'submitBtn')
    form.submit()
    time.sleep(2)
    token = driver.find_element(By.CSS_SELECTOR,'meta[name="csrf-token"]').get_attribute('content')
    time.sleep(5)

    page_no = 1
    all_ids = {}
    while True:
        url_new = url.format(end_date,from_date,page_no)
        driver.get(url_new)
        json_data = json.loads(driver.find_element(By.CSS_SELECTOR,'pre').text)["data"]
        for x in json_data:
            if x["attributes"]["missingInsuranceData"] == "":
                for y in x["relationships"]["unbilledAppointments"]["data"]:
                    if x["id"] not in all_ids:
                        all_ids[x["id"]] = []
                    all_ids[x["id"]].append(y["id"])
        
        if len(json_data) == 50:
            page_no = page_no+1
            continue
        else:
            break

    all_cookies = driver.get_cookies()

    header = {
        "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "x-csrf-token":token,
        "acccept":"application/vnd.api+json",
        "content-type":"application/vnd.api+json",
        "origin":"https://secure.simplepractice.com",
        "referer":f"https://secure.simplepractice.com/billings/insurance?endDate={end_date}&startDate={from_date}",
        "cookie":"; ".join([f"{cookie['name']}={cookie['value']}" for cookie in all_cookies]),
    }
    if not all_ids:
        return "No Record Found to Convert"

    payload = json.dumps({"appointmentIds":all_ids,"submitClaims":False,"updateAllBillingZipCodes":False})    
    r = requests.post("https://secure.simplepractice.com/frontend/insured-clients/batch-create",data=payload,headers=header)
    print(r.status_code)
    print(r.text)
    if r.status_code == 201:
        return "successful"
    else:
        return "unsuccessful"


def id_get(from_date,end_date,status,user,password_our):
    end_date = add_one_day(end_date)
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

    username = driver.find_element(By.ID,'user_email')
    username.send_keys(user)
    password = driver.find_element(By.ID,'user_password')
    password.send_keys(password_our)
    form = driver.find_element(By.ID,'submitBtn')
    form.submit()
    time.sleep(2)
    all_data = []
    page = 1
    
    while True:
        url = f'https://secure.simplepractice.com/frontend/insurance-claims?fields%5BinsuranceClaims%5D=hasPendingStatus%2CclaimSubmittedDate%2Cclient%2CinsurancePlan%2CcreatedAt%2Cstatus%2CcurrentSubmission&fields%5Bclients%5D=hashedId%2CpreferredName&fields%5BinsurancePlans%5D=name&fields%5BclaimSubmissions%5D=clearinghouse%2CadditionalInformation&filter%5BclientHashedId%5D=&filter%5BinsurancePayerId%5D=&filter%5Bstatus%5D=prepared&filter%5BtimeRange%5D={from_date}T05%3A00%3A00.000Z%2C{end_date}T04%3A59%3A59.999Z&filter%5BincludeClaimData%5D=false&filter%5BincludeOutOfNetwork%5D=false&include=client%2CinsurancePlan%2CcurrentSubmission&page%5Bnumber%5D={page}&page%5Bsize%5D=50&sort=priority%2C-createdDate%2Cclients.lastName%2Cclients.firstName'

        driver.get(url)
        time.sleep(2)
        full = json.loads(driver.find_element(By.TAG_NAME,"pre").text)
        data = full["data"]
        included = full["included"]

        for x in data:
            new_dict = {}
            second_id = (x["id"])
            new_dict["second_id"] = second_id
            match_id = x["relationships"]["client"]["data"]["id"]
            for y in included:
                if y["id"] == match_id:
                    new_dict["first_id"] = y["attributes"]["hashedId"]
                    break
            
            all_data.append(new_dict)
        if len(data) <50:
            break
        else:
            page = page+1
        
    return all_data

def id_get_page(from_date,end_date,number_page,user,password_our):
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
    
  
    username = driver.find_element(By.ID,'user_email')
    username.send_keys(user)
    password = driver.find_element(By.ID,'user_password')
    password.send_keys(password_our)
    form = driver.find_element(By.ID,'submitBtn')
    form.submit()

    
    
    driver.get(url+"#claims")
    time.sleep(2)
    driver.find_element(By.XPATH,"//input[@id='insurance-claims-daterangepicker']").click()
    driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[1]/input").clear()
    driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[1]/input").send_keys(from_date)
    driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[2]/input").clear()
    driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[2]/input").send_keys(end_date)
    time.sleep(2)
    driver.find_element(By.XPATH,"/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/button[1]").click()  
    time.sleep(5)
    elems = driver.find_elements(By.XPATH,"//a[@data-page]")

    try:
        value_all = max([int(x.get_attribute("data-page")) for x in elems])
        
        our_number = 5
        while int(number_page) >our_number:
            string = '//a[@data-page="'+str(our_number)+'"]'
            driver.find_element(By.XPATH,string).click()
            our_number = our_number+4
            time.sleep(2)
    
    
        string = '//a[@data-page="'+str(number_page)+'"]'
        driver.find_element(By.XPATH,string).click()
    except:
        value_all =1

        
    time.sleep(2)
    all_data = []
    elems = driver.find_elements(By.TAG_NAME,'tr')
    for elem in elems:
        try:
            href = elem.get_attribute('data-url')
            all_data.append({"first_id":href.split("/")[-3],"second_id":href.split("/")[-1]})
        except:
            pass
    driver.quit()
    return all_data,value_all

get_letter = {0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J",10:"K",11:"L"}
def video_get(url,user,password_our):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("window-size=1400,900")
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)
    x = driver.get(url)
    
    username = driver.find_element(By.ID,'user_email')
    username.send_keys(user)
    password = driver.find_element(By.ID,'user_password')
    password.send_keys(password_our)
    form = driver.find_element(By.ID,'submitBtn')
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




