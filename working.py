

from selenium import webdriver
import os
import time


def id_scrapper(from_date,end_date,user,password_our):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
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
    driver.find_element_by_xpath("//input[@id='insurance-claims-daterangepicker']").click()
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[1]/input").clear()
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[1]/input").send_keys(from_date)
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[2]/input").clear()
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/div[2]/input").send_keys(end_date)
    driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/div[2]/div/div[3]/div/div[2]/div[1]/form/div/div[2]/div/div/div[3]/div/button[1]").click()  
    time.sleep(5)
    all_data = []

    i = 1
    while True:
        i = i+1
        elems = driver.find_elements_by_tag_name('tr')
        for elem in elems:
            try:
                href = elem.get_attribute('data-url')
                all_data.append(href.split("/")[-1])
            except:
                pass
        string = '//a[@data-page="'+str(i)+'"]'
        break
        try:
            driver.find_element_by_xpath(string).click()
        except:
            break
        time.sleep(10)
        
    return all_data
    
def video_scrapper(url,user,password_our):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
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
    data["patient_id"] = (driver.execute_script("return document.getElementsByName('dependent[address][zip]')[0].value"))
    data["patient_id"] = (driver.execute_script("return document.getElementsByName('dependent[phoneNumber]')[0].value"))


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
    data["billingProvider_lastName"] = (driver.execute_script("return document.getElementsByName('billingProvider[lastName]')[0].value"))
    data["billingProvider_firstName"] = (driver.execute_script("return document.getElementsByName('billingProvider[firstName]')[0].value"))
    data["billingProvider_middleName"] = (driver.execute_script("return document.getElementsByName('billingProvider[middleName]')[0].value"))
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

    return data




