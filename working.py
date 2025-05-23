from selenium import webdriver
import os
import time
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
import pandas as pd
from datetime import datetime, timedelta
from config import *
from helper import *
import logging
import gc
import tempfile
import psutil

dir_path = os.path.dirname(os.path.realpath(__file__))

def kill_chrome_processes():
    """Forcefully kill any remaining Chrome processes"""
    try:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and ('chrome' in proc.info['name'].lower() or 'chromedriver' in proc.info['name'].lower()):
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
    except Exception as e:
        logging.warning(f"Error killing Chrome processes: {str(e)}")

def cleanup_driver(driver):
    """Enhanced driver cleanup"""
    if driver is None:
        return
    
    try:
        try:
            driver.close()
        except:
            pass
        
        try:
            driver.quit()
        except:
            pass
        
        del driver
    except Exception as e:
        logging.error(f"Cleanup error: {str(e)}")
    finally:
        # kill_chrome_processes()  
        gc.collect()

def login_health_app(url,username,password,secret_key):

    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')	
        options.add_argument('--headless=new')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-gpu")  # Add this
        options.add_argument("--disable-extensions")  # Add this
        options.add_argument("--disable-infobars")  # Add this
        options.add_argument("--disable-notifications")  # Add this
        options.add_argument("--disable-application-cache")  # Add this
        options.add_argument("--window-size=1280,700")  # Fixed syntax
        options.add_argument("--incognito")
        options.add_argument("--disable-browser-side-navigation")  # Add this
        options.add_argument("--dns-prefetch-disable")  # Add this
        options.add_argument("--disable-setuid-sandbox")  # Add this
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--disable-background-timer-throttling')
        options.add_argument('--disable-backgrounding-occluded-windows')
        options.add_argument('--disable-features=NetworkService')
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_experimental_option("prefs",{
            "download.default_directory" : dir_path,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.images": 2
            })   
        
        service = webdriver.ChromeService(executable_path=os.environ.get("CHROMEDRIVER_PATH"))
        driver = webdriver.Chrome(service=service, options=options)
        # driver = webdriver.Chrome(options=options)
        driver.set_page_load_timeout(30)  # Set maximum page load time

        # Navigate to URL and wait only for essential elements
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





def therapy_notes_claims_data(code, user_name,pass_word, date_start,date_end):
    try:
        s_m,s_d,s_y = process_date(date_start)
        e_m,e_d,e_y = process_date(date_end)

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')	
        options.add_argument('--headless')
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("window-size=1400,900")
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_experimental_option("prefs",{"download.default_directory" : dir_path})   
        driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=options)

    except Exception as e:
        raise Exception(e)

    try:
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
    except Exception as e:
        raise Exception(e)
    finally:
        cleanup_driver(driver)

    
def payer_data(user,password_our,count,secret_key):
    try:
        url = "https://secure.simplepractice.com/clients"
        driver = login_health_app(url,user,password_our,secret_key)
    except Exception as e:
        raise Exception(e)
    try:
        main = []
        for counter in range(count,count+10):
            driver.get("https://secure.simplepractice.com/frontend/insurance-plans?filter[search]=&filter[providerFilter]=search&include=insurancePayer,eligiblePayer,practicePayerAddresses,practiceInsurancePayers&page[number]={}&page[size]=50".format(counter))
            raw_json = json.loads(driver.find_element(By.TAG_NAME,"pre").text)
            if len(raw_json["data"]) ==0:
                break

            for x in raw_json["data"]:
                dictionary = {
                    "id": str(x["attributes"]["insuranceProviderId"]),
                    "payer_name": x["attributes"]["name"],
                    "payer_id": x["attributes"]["nameWithPayer"].split("(")[-1][:-1],
                }

                for j in raw_json.get("included",[]):
                    if j["type"] == "insurancePayers" and j["id"] == dictionary["id"]:
                        address = j["attributes"].get("defaultAddress", {})
                        if address:
                            dictionary["city"] = address.get("city", "")
                            dictionary["zipcode"] = address.get("zipcode", "")
                            dictionary["address"] = address.get("address", "")
                            dictionary["state"] = address.get("state", "")
                            break  # Exit loop after finding the matching payer

                main.append(dictionary)
        return main
    except Exception as e:
        logging.error(e,exc_info=True)
        raise Exception(e)
    finally:
        cleanup_driver(driver)

    
def get_all_client(user,password_our,secret_key):
    try:
        url = "https://secure.simplepractice.com/clients"
        driver = login_health_app(url,user,password_our,secret_key)
    except Exception as e:
        raise Exception(e)
    try:
        base_url = "https://secure.simplepractice.com/frontend/base-clients?fields[baseClients]=emails,clinician,clientPortalSettings,clientReferralSource,reciprocalClientRelationships,insuranceInfos,clientRelationships,phones,addresses,clientAccess,permissions,hashedId,name,firstName,lastName,middleName,initials,suffix,nickname,preferredName,legalName,defaultPhoneNumber,defaultEmailAddress,generalNotes,sex,genderInfo,ignoredForMerge&fields[clients]=autopayReminder,autopayInsuranceReminder,clinician,office,upcomingAppointments,latestInvoices,latestBillingDocuments,clientBillingOverview,clientAdminNote,clientDocumentRequests,viewableDocuments,channelUploadedDocuments,currentInsuranceAuthorization,insuranceAuthorizations,insuranceClaimFields,globalMonarchChannel,stripeCards,cptCodeRates,pendingAppointmentConfirmations,billingSettings,billingType,inActiveTreatment,secondaryClinicianIds,emails,clientPortalSettings,clientReferralSource,reciprocalClientRelationships,insuranceInfos,clientRelationships,phones,addresses,clientAccess,permissions,hashedId,name,firstName,lastName,middleName,initials,suffix,nickname,preferredName,legalName,defaultPhoneNumber,defaultEmailAddress,generalNotes,sex,genderInfo,ignoredForMerge,enableEmailReminders,enableOutstandingDocumentReminders,enableSmsvoiceReminders,isMinor,reminderEmail,reminderPhone&fields[clientCouples]=autopayReminder,autopayInsuranceReminder,clinician,office,upcomingAppointments,latestInvoices,latestBillingDocuments,clientBillingOverview,clientAdminNote,clientDocumentRequests,viewableDocuments,channelUploadedDocuments,currentInsuranceAuthorization,insuranceAuthorizations,insuranceClaimFields,globalMonarchChannel,stripeCards,cptCodeRates,pendingAppointmentConfirmations,billingSettings,billingType,inActiveTreatment,secondaryClinicianIds,emails,clientPortalSettings,clientReferralSource,reciprocalClientRelationships,insuranceInfos,clientRelationships,phones,addresses,clientAccess,permissions,hashedId,name,firstName,lastName,middleName,initials,suffix,nickname,preferredName,legalName,defaultPhoneNumber,defaultEmailAddress,generalNotes,sex,genderInfo,ignoredForMerge,firstNameLastInitial&fields[insuranceInfo]=hieEnabled&filter[thisType]=Client,ClientCouple&include=phones,emails,insuranceInfos,clientRelationships.client,clientRelationships.relatedClient.phones,clientRelationships.relatedClient.emails,reciprocalClientRelationships.client.phones,reciprocalClientRelationships.client.emails,reciprocalClientRelationships.relatedClient&page[number]={}&page[size]=50&sort=lastName"

        full_data = []
        page = 1
        while True:
            url = base_url.format(page)
            response = driver.get(url)
            json_data = driver.find_element(By.TAG_NAME,"body").text
            json_data = json.loads(json_data)["data"]
            if len(json_data) == 0:
                break
            full_data.extend(json_data)
            page += 1
        return full_data
    except Exception as e:
        raise Exception(e)
    finally:
        cleanup_driver(driver)




def create_un_bill_user(from_date,end_date,user,password_our,secret_key):

    if "/" in from_date:
        from_date = convert_date(from_date)
        end_date = convert_date(end_date)
    

    url_template = '''https://secure.simplepractice.com/frontend/insured-clients?fields%5Bclients%5D=hashedId%2CinsuranceBillingSubtype%2CpreferredName%2CinsuranceInfos&fields%5BteamMembers%5D=name%2Csuffix%2CfirstName%2ClastName%2Croles&filter%5BendDate%5D={}&filter%5BstartDate%5D={}&include=unbilledAppointments.client.insuranceInfos.insurancePlan.practiceInsurancePayers%2CunbilledAppointments.clinician%2Cclient%2CinsurancePlan%2CunbilledAppointments.appointmentClients.client.insuranceInfos.insurancePlan.practiceInsurancePayers%2CunbilledAppointments.appointmentClients.appointment&page%5Bnumber%5D={}&page%5Bsize%5D=50'''
    try:
        url = "https://secure.simplepractice.com/users/sign_in"
        driver = login_health_app(url,user,password_our,secret_key)
    except Exception as e:
        raise Exception(e)

    try:
        
        time.sleep(2)
        token = driver.find_element(By.CSS_SELECTOR,'meta[name="csrf-token"]').get_attribute('content')
        time.sleep(5)

        page_no = 1
        all_ids = {}
        while True:
            url_new = url_template.format(end_date,from_date,page_no)
            driver.get(url_new)
            json_data = json.loads(driver.find_element(By.CSS_SELECTOR,'pre').text)["data"]

            if not json_data:
                print("No more data. Stopping pagination.")
                break

            for client in json_data:
                if client["attributes"].get("missingInsuranceData", "") == "":
                    appointment_ids = [appt["id"] for appt in client["relationships"]["unbilledAppointments"]["data"]]
                    if appointment_ids:
                        all_ids[client["id"]] = appointment_ids

            driver.execute_script("window.stop();") 
            page_no = page_no+1

        if not all_ids:
            return "No Record Found to Convert"    

        all_cookies = driver.get_cookies()
        cleanup_driver(driver)

        header = {
            "user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            "x-csrf-token":token,
            "acccept":"application/vnd.api+json",
            "content-type":"application/vnd.api+json",
            "origin":"https://secure.simplepractice.com",
            "referer":f"https://secure.simplepractice.com/billings/insurance?endDate={end_date}&startDate={from_date}",
            "cookie":"; ".join([f"{cookie['name']}={cookie['value']}" for cookie in all_cookies]),
        }


        payload = json.dumps({"appointmentIds":all_ids,"submitClaims":False,"updateAllBillingZipCodes":False})    
        r = requests.post("https://secure.simplepractice.com/frontend/insured-clients/batch-create",data=payload,headers=header)     
        logging.error(r.status_code)
        logging.error(r.text)
        if r.status_code == 201:
            return "Successful"
        else:
            return "Unsuccessful"
    except Exception as e:
        logging.error(e,exc_info=True)
        raise Exception(e)
    finally:
        cleanup_driver(driver)

def get_all_claims(from_date,end_date,status,user,password_our,secret_key):
    try:
        url = "https://secure.simplepractice.com/billings/insurance/claims?endDate={}&startDate={}&status={}".format(end_date,from_date,status)
        driver = login_health_app(url,user,password_our,secret_key)
    except Exception as e:
        raise Exception(e)

    try:
        time.sleep(2)
        end_date = add_one_day(end_date)
        all_data = []
        page = 1    
        while True:
            url = f'https://secure.simplepractice.com/frontend/insurance-claims?fields%5BinsuranceClaims%5D=hasPendingStatus%2CclaimSubmittedDate%2Cclient%2CinsurancePlan%2CcreatedAt%2Cstatus%2CcurrentSubmission%2CclaimSupportRequest%2Cappointments%2CmanagedBillingClaim&fields%5Bclients%5D=hashedId%2CpreferredName&fields%5BinsurancePlans%5D=name&fields%5BclaimSubmissions%5D=clearinghouse%2CadditionalInformation&fields%5Bappointments%5D=managedByManagedBilling&fields%5BmanagedBillingClaim%5D=revopsClaimStatus&filter%5BclientHashedId%5D=&filter%5BinsurancePayerId%5D=&filter%5Bstatus%5D={status}&filter%5BclaimSupportStatus%5D=&filter%5BtimeRange%5D={from_date}T06%3A00%3A00.000Z%2C{end_date}T05%3A59%3A59.999Z&filter%5BincludeClaimData%5D=false&filter%5BincludeOutOfNetwork%5D=false&include=client%2CinsurancePlan%2CcurrentSubmission%2CclaimSupportRequest%2CclaimSupportRequest.claimSupportMessages%2Cappointments&page%5Bnumber%5D={page}&page%5Bsize%5D=50&sort=priority%2C-createdDate%2Cclients.lastName%2Cclients.firstName'
            driver.get(url)
            time.sleep(1)
            full = json.loads(driver.find_element(By.TAG_NAME,"pre").text)
            data = full.get("data",[])
            included = full.get("included",[])
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
    except Exception as e:
        logging.error(e,exc_info=True)
        raise Exception(e)
    finally:
        cleanup_driver(driver)

def id_get_page(from_date,end_date,number_page,user,password_our):
    try:
        url = "https://secure.simplepractice.com/billings/insurance"
        driver = login_health_app(url,user,password_our,secret_key)
    except Exception as e:
        raise Exception(e)

    try:

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
        return all_data,value_all
    except Exception as e:
        raise Exception(e)
    finally:
        cleanup_driver(driver)



def get_insurance_client_data(url,user,password_our,secret_key):
    try:
        # url = "https://secure.simplepractice.com/billings/insurance"
        driver = login_health_app(url,user,password_our,secret_key)
    except Exception as e:
        raise Exception(e)
    try:
        data = {}
        time.sleep(5)
        try:
            data["payer_id"] = driver.execute_script("return document.getElementsByName('payer[id]')[0].value")
        except:
            print("here in new line")
            driver.get(url)
            time.sleep(5)
            data["payer_id"] = driver.execute_script("return document.getElementsByName('payer[id]')[0].value")
        print("done1")
        data["payer_name"] = (driver.execute_script("return document.getElementsByName('payer[name]')[0].value"))
        print("done2")
        # data["payer_streetLine1"] = (driver.execute_script("return document.getElementsByName('payer[address][streetLine1]')[0].value"))
        # data["payer_streetLine2"] = (driver.execute_script("return document.getElementsByName('payer[address][streetLine2]')[0].value"))
        # data["payer_city"] = (driver.execute_script("return document.getElementsByName('payer[address][city]')[0].value"))
        # data["payer_state"] = (driver.execute_script("return document.getElementsByName('payer[address][state]')[0].value"))
        # data["payer_zip"] = (driver.execute_script("return document.getElementsByName('payer[address][zip]')[0].value"))
        # data["insured_id"] = (driver.execute_script("return document.getElementsByName('subscriber[id]')[0].value"))
        data["patient_lastName"] = (driver.execute_script("return document.getElementsByName('dependent[lastName]')[0].value"))
        print("done3")
        data["patient_firstName"] = (driver.execute_script("return document.getElementsByName('dependent[firstName]')[0].value"))
        print("done4")
        # data["patient_middleName"] = (driver.execute_script("return document.getElementsByName('dependent[middleName]')[0].value"))
        # data["patient_dob"] = (driver.execute_script("return document.getElementsByName('dependent[dob]')[0].value"))

        # data["insured_lastName"] = (driver.execute_script("return document.getElementsByName('subscriber[lastName]')[0].value"))
        # data["insured_firstName"] = (driver.execute_script("return document.getElementsByName('subscriber[firstName]')[0].value"))
        # data["insured_middleName"] = (driver.execute_script("return document.getElementsByName('subscriber[middleName]')[0].value"))   
        
        
        # data["patient_streetLine1"] = (driver.execute_script("return document.getElementsByName('dependent[address][streetLine1]')[0].value"))
        # data["patient_streetLine2"] = (driver.execute_script("return document.getElementsByName('dependent[address][streetLine2]')[0].value"))
        # data["patient_state"] = (driver.execute_script("return document.getElementsByName('dependent[address][state]')[0].value"))
        # data["patient_city"] = (driver.execute_script("return document.getElementsByName('dependent[address][city]')[0].value"))
        # data["patient_zip"] = (driver.execute_script("return document.getElementsByName('dependent[address][zip]')[0].value"))
        # data["patient_telephone"] = (driver.execute_script("return document.getElementsByName('dependent[phoneNumber]')[0].value"))
        # try:
        #     data["patient_id"] = (driver.execute_script("return document.getElementsByName('dependent[id]')[0].value"))
        # except:
        #     data["patient_id"] = ""

        # data["insured_streetLine1"] = (driver.execute_script("return document.getElementsByName('subscriber[address][streetLine1]')[0].value"))
        # data["insured_streetLine2"] = (driver.execute_script("return document.getElementsByName('subscriber[address][streetLine2]')[0].value"))
        # data["insured_city"] = (driver.execute_script("return document.getElementsByName('subscriber[address][city]')[0].value"))   
        # data["insured_state"] = (driver.execute_script("return document.getElementsByName('subscriber[address][state]')[0].value"))   
        # data["insured_zip"] = (driver.execute_script("return document.getElementsByName('subscriber[address][zip]')[0].value"))   
        # data["insured_number"] = (driver.execute_script("return document.getElementsByName('subscriber[phoneNumber]')[0].value"))   

        # data["otherinsured_lastName"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][lastName]')[0].value"))
        # data["otherinsured_firstName"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][firstName]')[0].value"))
        # data["otherinsured_mi"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][middleName]')[0].value")) 
        

        
        # data["otherinsured_relationship"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][relationship]')[0].options[document.getElementsByName('otherPayers[0][subscriber][relationship]')[0].selectedIndex].text"))
        
        # data["otherinsured_policy"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][groupId]')[0].value"))   
        # data["otherinsured_insuredid"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][id]')[0].value"))  
        # data["otherinsured_indicatorcode"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][claimFilingIndicator]')[0].options[document.getElementsByName('otherPayers[0][claimFilingIndicator]')[0].selectedIndex].text"))
        
        # data["otherinsured_insurancePlanName"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][name]')[0].value"))
        # data["otherinsured_insuranceTypeCode"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][subscriber][insuranceTypeCode]')[0].options[document.getElementsByName('otherPayers[0][subscriber][insuranceTypeCode]')[0].selectedIndex].text"))   
        # data["otherinsured_resSequence"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][responsibilitySequence]')[0].options[document.getElementsByName('otherPayers[0][responsibilitySequence]')[0].selectedIndex].text"))   
        # data["otherinsured_payerId"] = (driver.execute_script("return document.getElementsByName('otherPayers[0][id]')[0].value"))   
        
        # data["patient_autoAccidentState"] = (driver.execute_script("return document.getElementsByName('claim[autoAccidentState]')[0].value")) 
        
        # data["patient_claimCode"] = (driver.execute_script("return document.getElementsByName('code')[0].value")) 
        
        # data["insured_policy"] = (driver.execute_script("return document.getElementsByName('subscriber[groupId]')[0].value")) 
        # data["insured_dob"] = (driver.execute_script("return document.getElementsByName('subscriber[dob]')[0].value")) 
        # data["insured_planName"] = (driver.execute_script("return document.getElementsByName('subscriber[groupName]')[0].value")) 
        
        
        # data["dataOfIllness"] = (driver.execute_script("return document.getElementsByName('claim[additionalClaimInfo]')[0].value")) 
        # data["dataOfIllness_qual"] = (driver.execute_script("return document.getElementsByName('claim[additionalClaimInfoCode]')[0].options[document.getElementsByName('claim[additionalClaimInfoCode]')[0].selectedIndex].text "))
    
        # data["lastWorkData"] = (driver.execute_script("return document.getElementsByName('claim[lastWorkedDate]')[0].value")) 
        # data["workReturnDate"] = (driver.execute_script("return document.getElementsByName('claim[workReturnDate]')[0].value"))  
        

        # data["provider"] = (driver.execute_script("return document.getElementsByName('box17ProviderOption')[0].options[document.getElementsByName('box17ProviderOption')[0].selectedIndex].text")) 
        # data["provider_lastName"] = (driver.execute_script("return document.getElementsByName('box17Provider[lastName]')[0].value"))  
        # data["provider_firstName"] = (driver.execute_script("return document.getElementsByName('box17Provider[firstName]')[0].value")) 
        # data["provider_middleName"] = (driver.execute_script("return document.getElementsByName('box17Provider[middleName]')[0].value"))  

        # data["secondayIdType"] = (driver.execute_script("return document.getElementsByName('box17Provider[secondaryIdType]')[0].options[document.getElementsByName('box17Provider[secondaryIdType]')[0].selectedIndex].text"))     
        # data["secondaryId"] = (driver.execute_script("return document.getElementsByName('box17Provider[secondaryId]')[0].value"))        
        # data["npi"] = (driver.execute_script("return document.getElementsByName('box17Provider[npi]')[0].value"))         
        
        # data["hospitalizationDate_current_from"] = (driver.execute_script("return document.getElementsByName('claim[admissionDate]')[0].value")) 
        # data["hospitalizationDate_current_to"] = (driver.execute_script("return document.getElementsByName('claim[dischargeDate]')[0].value")) 
        
        # data["additionalClaimInfo"] = (driver.execute_script("return document.getElementsByName('claim[additionalClaimInfo]')[0].value"))  
        # data["additionalClaimInfoCode"] = (driver.execute_script("return document.getElementsByName('claim[additionalClaimInfoCode]')[0].options[document.getElementsByName('claim[additionalClaimInfoCode]')[0].selectedIndex].text"))   
    
        # data["supplementalClaim_typeCode"] = (driver.execute_script("return document.getElementsByName('claim[reportTypeCode]')[0].value"))  
        # data["supplementalClaim_transCode"] = (driver.execute_script("return document.getElementsByName('claim[reportTransmissionCode]')[0].value"))  
        # data["supplementalClaim_attachmentId"] = (driver.execute_script("return document.getElementsByName('claim[attachmentId]')[0].value"))    
        # data["outsideLabCharges"] = (driver.execute_script("return document.getElementsByName('claim[outsideLabCharges]')[0].value"))
        
        # data["icdInd"] = (driver.execute_script("return document.getElementsByName('claim[icdIndicator]')[0].value"))
        # data["icdA"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][0]')[0].value"))
        # data["icdB"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][1]')[0].value"))
        # data["icdC"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][2]')[0].value"))
        # data["icdD"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][3]')[0].value"))
        # data["icdE"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][4]')[0].value"))
        # data["icdF"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][5]')[0].value"))
        # data["icdG"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][6]')[0].value"))
        # data["icdH"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][7]')[0].value"))
        # data["icdI"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][8]')[0].value"))
        # data["icdJ"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][9]')[0].value"))
        # data["icdK"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][10]')[0].value"))
        # data["icdL"] = (driver.execute_script("return document.getElementsByName('claim[diagnosisCodes][11]')[0].value"))

        # data["resubmission_refNo"] = (driver.execute_script("return document.getElementsByName('claim[payerControlNumber]')[0].value"))
        # data["priorAuthNo"] = (driver.execute_script("return document.getElementsByName('claim[priorAuthorizationNumber]')[0].value"))
        # data["CLIANo"] = (driver.execute_script("return document.getElementsByName('claim[cliaNumber]')[0].value"))

        
        # data["billingProvider_taxId"] = (driver.execute_script("return document.getElementsByName('billingProvider[taxId]')[0].value"))
        # data["claim_totalCharge"] = (driver.execute_script("return document.getElementsByName('claim[totalCharge]')[0].value"))
        # data["claim_patientAmountPaid"] = (driver.execute_script("return document.getElementsByName('claim[patientAmountPaid]')[0].value"))
        # data["claim_claimSignatureDate"] = (driver.execute_script("return document.getElementsByName('claim[claimSignatureDate]')[0].value"))
        # data["serviceFacility_name"] = (driver.execute_script("return document.getElementsByName('serviceFacility[name]')[0].value"))
        # data["serviceFacility_streetLine1"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][streetLine1]')[0].value"))
        # data["serviceFacility_streetLine2"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][streetLine2]')[0].value"))
        # data["serviceFacility_city"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][city]')[0].value"))
        # data["serviceFacility_state"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][state]')[0].value"))
        # data["serviceFacility_zip"] = (driver.execute_script("return document.getElementsByName('serviceFacility[address][zip]')[0].value"))
        # data["serviceFacility_npi"] = (driver.execute_script("return document.getElementsByName('serviceFacility[npi]')[0].value"))
        
        
        # data["billingProvider_phoneNumber"] = (driver.execute_script("return document.getElementsByName('billingProvider[phoneNumber]')[0].value"))
        # try:
        #     data["billingProvider_lastName"] = (driver.execute_script("return document.getElementsByName('billingProvider[lastName]')[0].value"))
        #     data["billingProvider_firstName"] = (driver.execute_script("return document.getElementsByName('billingProvider[firstName]')[0].value"))
        #     data["billingProvider_middleName"] = (driver.execute_script("return document.getElementsByName('billingProvider[middleName]')[0].value"))
            
        # except:
        #     data["billingProvider_organization"] = (driver.execute_script("return document.getElementsByName('billingProvider[organizationName]')[0].value"))
        # data["billingProvider_streetLine1"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][streetLine1]')[0].value"))
        # data["billingProvider_streetLine2"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][streetLine2]')[0].value"))
        # data["billingProvider_city"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][city]')[0].value"))
        # data["billingProvider_state"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][state]')[0].value"))
        # data["billingProvider_zip"] = (driver.execute_script("return document.getElementsByName('billingProvider[address][zip]')[0].value"))
        # data["billingProvider_npi"] = (driver.execute_script("return document.getElementsByName('billingProvider[npi]')[0].value"))
        # data["billingProvider_taxonomyCode"] = (driver.execute_script("return document.getElementsByName('billingProvider[taxonomyCode]')[0].value"))

    ########################################################################

        # data["patient_gender"] = "" 
        # if (driver.execute_script("return document.getElementsByName('dependent[gender]')[0].checked")):
        #     data["patient_gender"] = "m"
        # if (driver.execute_script("return document.getElementsByName('dependent[gender]')[1].checked")):
        #     data["patient_gender"] = "f"

        # data["patient_employment"] = "" 
        # if (driver.execute_script("return document.getElementsByName('claim[relatedToEmployment]')[0].checked")):
        #     data["patient_employment"] = "yes"
        # if (driver.execute_script("return document.getElementsByName('claim[relatedToEmployment]')[1].checked")):
        #     data["patient_employment"] = "no"
            
        #new addition
        # data["patient_relationship_to_insecured"] = "" 
        # if (driver.execute_script("return document.getElementsByName('dependent[relationship]')[0].checked")):
        #     data["patient_relationship_to_insecured"] = "self"
        # if (driver.execute_script("return document.getElementsByName('dependent[relationship]')[1].checked")):
        #     data["patient_relationship_to_insecured"] = "spouse"
        # if (driver.execute_script("return document.getElementsByName('dependent[relationship]')[2].checked")):
        #     data["patient_relationship_to_insecured"] = "child"
        # if (driver.execute_script("return document.getElementsByName('dependent[relationship]')[3].checked")):
        #     data["patient_relationship_to_insecured"] = "other"        

        # data["auto_accident"] = "" 
        # if (driver.execute_script("return document.getElementsByName('claim[autoAccident]')[0].checked")):
        #     data["auto_accident"] = "yes"
        # if (driver.execute_script("return document.getElementsByName('claim[autoAccident]')[1].checked")):
        #     data["auto_accident"] = "no"


        # data["other_accident"] = "" 
        # if (driver.execute_script("return document.getElementsByName('claim[otherAccident]')[0].checked")):
        #     data["other_accident"] = "yes"
        # if (driver.execute_script("return document.getElementsByName('claim[otherAccident]')[1].checked")):
        #     data["other_accident"] = "no"


        # data["insured_gender"] = "" 
        # if (driver.execute_script("return document.getElementsByName('subscriber[gender]')[0].checked")):
        #     data["insured_gender"] = "m"
        # if (driver.execute_script("return document.getElementsByName('subscriber[gender]')[1].checked")):
        #     data["insured_gender"] = "f"

        # data["anyother_healthPlan"] = "" 
        # if (driver.execute_script("return document.getElementsByName('otherPayer')[0].checked")):
        #     data["anyother_healthPlan"] = "yes"
        # if (driver.execute_script("return document.getElementsByName('otherPayer')[1].checked")):
        #     data["anyother_healthPlan"] = "no"

        # data["claim_directPaymentAuthorized"] = ""
        # if (driver.execute_script("return document.getElementsByName('claim[directPaymentAuthorized]')[0].checked")):
        #     data["claim_directPaymentAuthorized"] = "yes"    
            
            
        # data["claim_outsideLab"] = "" 
        # if (driver.execute_script("return document.getElementsByName('claim[outsideLab]')[0].checked")):
        #     data["claim_outsideLab"] = "yes"
        # if (driver.execute_script("return document.getElementsByName('claim[outsideLab]')[1].checked")):
        #     data["claim_outsideLab"] = "no"
            
        # data["claim_frequency"] = "" 
        # if (driver.execute_script("return document.getElementsByName('claim[frequency]')[0].checked")):
        #     data["claim_frequency"] = "original"
        # if (driver.execute_script("return document.getElementsByName('claim[frequency]')[1].checked")):
        #     data["claim_frequency"] = "resubmission"
        # if (driver.execute_script("return document.getElementsByName('claim[frequency]')[2].checked")):
        #     data["claim_frequency"] = "cancel"


        # data["billingProvider_taxIdType"] = "" 
        # if (driver.execute_script("return document.getElementsByName('billingProvider[taxIdType]')[0].checked")):
        #     data["billingProvider_taxIdType"] = "SSN"
        # if (driver.execute_script("return document.getElementsByName('billingProvider[taxIdType]')[1].checked")):
        #     data["billingProvider_taxIdType"] = "EIN"
            
        # data["claim_acceptAssignmentCode"] = "" 
        # if (driver.execute_script("return document.getElementsByName('claim[acceptAssignmentCode]')[0].checked")):
        #     data["claim_acceptAssignmentCode"] = "yes"
        # if (driver.execute_script("return document.getElementsByName('claim[acceptAssignmentCode]')[1].checked")):
        #     data["claim_acceptAssignmentCode"] = "no"
            
        # data["billingProvider_entity"] = "" 
        # if (driver.execute_script("return document.getElementsByName('billingProvider[entity]')[0].checked")):
        #     data["billingProvider_entity"] = "individual"
        # if (driver.execute_script("return document.getElementsByName('billingProvider[entity]')[1].checked")):
        #     data["billingProvider_entity"] = "organization"
            

        for i in range(0,6):
            #-----
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
            print("done56")
            #-----

            # key = "claimserviceLines_" + str(i) +"_procedureCode" 	
            # name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][procedureCode]')[0].value"
            # data[key] = (driver.execute_script(name))
        
        
            # key = "claimserviceLines_" + str(i) +"_description" 	
            # name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][description]')[0].value"
            # data[key] = (driver.execute_script(name))      
            
            # lit_let = []
            # for ss in range(0,9):
                
            #     name = "return document.getElementsByClassName('dc-pointers-table')["+str(i)+"].getElementsByTagName('input')["+str(ss)+"].checked"
            #     name = (driver.execute_script(name))  

            #     if name == True:

            #         letter = get_letter[ss]
            #         lit_let.append(letter)
        
            # key = "claim_serviceLines_"+str(i)+ "_Diagnose_pointer"  
            # data[key] = lit_let
            # --------
            for x in range(0,4):
                key = "claim_serviceLines_" + str(i) +"_procedureModifiers_"+str(x) 	
                name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][procedureModifiers]["+str(x)+"]')[0].value"
                data[key] = (driver.execute_script(name))
                print("done78")
            # --------

            # key = "claimserviceLines_" + str(i) +"_chargeAmount" 	
            # name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][chargeAmount]')[0].value"     
            # data[key] = (driver.execute_script(name))

            # key = "claimserviceLines_" + str(i) +"_units" 	
            # name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][units]')[0].value"    
            # data[key] = (driver.execute_script(name))
        
            # key = "claimserviceLines_" + str(i) +"_epsdtIndicator" 	
            # name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][epsdtIndicator]')[0].value"
            # data[key] = (driver.execute_script(name))

            # key = "claimserviceLines_" + str(i) +"_renderingProviderlastName" 	
            # name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][renderingProvider][lastName]')[0].value"
            # data[key] = (driver.execute_script(name))

            # key = "claimserviceLines_" + str(i) +"_renderingProviderfirstName" 	
            # name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][renderingProvider][firstName]')[0].value"
            # data[key] = (driver.execute_script(name))

            # key = "claimserviceLines_" + str(i) +"_renderingProvidernpi" 	
            # name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][renderingProvider][npi]')[0].value"
            # data[key] = (driver.execute_script(name))

        return data
    except Exception as e:
        raise Exception(e)
    finally:
        cleanup_driver(driver)


# print(get_insurance_client_data("https://secure.simplepractice.com/clients/1ca2a91b31c4cf5c/insurance_claims/216832096","info+1@gina4med.com","Rakovski@345","AW7WGIL4BFQO6B3K2TGDKCMXEJ7EHLI2NV7B4RP7IJBBTH5IDQKA"))

def submit_claim_data(url,user,password_our,secret_key,modifier,is_submit):
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
                element.clear()
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
