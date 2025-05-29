


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

def login_health_app(url, username, password, secret_key):
    """Optimized login function for Health App with reduced execution time."""
    
    # Initialize driver outside try block for proper cleanup
    driver = None
    
    try:
        # Precompute OTP before starting browser to save time
        otp_code = get_otp(secret_key)
        letters = ['a', 'b', 'c', 'd', 'e', 'f']  # Moved outside to avoid recreation
        
        # Chrome options with essential settings only
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
        
        # Only critical experimental options
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.notifications": 2
        })
        
        service = webdriver.ChromeService(
            executable_path=os.environ.get("CHROMEDRIVER_PATH")
        )
        driver = webdriver.Chrome(service=service, options=options)

        driver.set_page_load_timeout(60)  # Reduced from 30
        
        # 1. Optimized page load and element interaction
        driver.get(url)
        
        # Use JavaScript direct injection for faster form filling
        driver.execute_script(f"""
            document.getElementById('user_email').value = '{username}';
            document.getElementById('user_password').value = '{password}';
            document.getElementById('submitBtn').click();
        """)
        
        # 2. Optimized OTP handling
        # Wait for any OTP field to appear (reduces wait time)
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[id^="code_"]'))
        )
        
        # Batch OTP field filling using JavaScript
        for i in range(6):
            field = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, f"code_{letters[i]}")))
            field.clear()
            field.send_keys(otp_code[i])
        
        # Wait for submit button to be clickable
        submit_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, 'commit')))
        
        # Click using JavaScript for reliability
        driver.execute_script("arguments[0].click();", submit_btn)
        return driver

    except Exception as e:
        logging.error(f"Login failed: {str(e)}", exc_info=True)
        if driver:
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
    driver = None
    
    JS_EXTRACTOR = """
        function getSelectedText(select) {
            if (!select) return "";
            return select.options[select.selectedIndex]?.text || "";
        }

        const data = {
            payer_id: document.querySelector("[name='payer[id]']")?.value || "",
            payer_name: document.querySelector("[name='payer[name]']")?.value || "",
            patient_lastName: document.querySelector("[name='dependent[lastName]']")?.value || "",
            patient_firstName: document.querySelector("[name='dependent[firstName]']")?.value || "",
            serviceLines: []
        };

        // More reliable service line detection
        let i = 0;
        while (i < 6) {
            // Find the service date from element using precise selector
            const dateFromSelector = `input[name='claim[serviceLines][${i}][serviceDateFrom]']`;
            const fromEl = document.querySelector(dateFromSelector);
            
            // If element doesn't exist or has no value, stop processing
            if (!fromEl || !fromEl.value) {
                i++;
                continue;
            }

            // Build service line data with fallbacks
            const line = {
                serviceDateFrom: fromEl.value,
                serviceDateTo: document.querySelector(`input[name='claim[serviceLines][${i}][serviceDateTo]']`)?.value || "",
                placeOfService: getSelectedText(document.querySelector(`select[name='claim[serviceLines][${i}][placeOfService]']`)),
                modifiers: []
            };

            // Process modifiers with precise selectors
            for (let x = 0; x < 4; x++) {
                const modSelector = `input[name='claim[serviceLines][${i}][procedureModifiers][${x}]']`;
                line.modifiers.push(document.querySelector(modSelector)?.value || "");
            }

            data.serviceLines.push(line);
            i++;
        }

        return data;
    """
    for attempt in range(2):
        try:
            driver = login_health_app(url, user, password_our, secret_key)
            
            time.sleep(5)
            
            # Execute mega-extractor script
            raw_data = driver.execute_script(JS_EXTRACTOR)
            print(raw_data)
            # Validate we got critical data
            if not raw_data or not raw_data.get('payer_id'):
                raise ValueError("Essential data missing")
            
            # Transform data structure
            data = {
                "payer_id": raw_data['payer_id'],
                "payer_name": raw_data['payer_name'],
                "patient_lastName": raw_data['patient_lastName'],
                "patient_firstName": raw_data['patient_firstName']
            }
            
            # Process service lines
            for i, line in enumerate(raw_data['serviceLines']):
                prefix = f"claim_serviceLines_{i}"
                data.update({
                    f"{prefix}_serviceDateFrom": line['serviceDateFrom'],
                    f"{prefix}_serviceDateTo": line['serviceDateTo'],
                    f"{prefix}_placeOfService": line['placeOfService'],
                    **{
                        f"{prefix}_procedureModifiers_{x}": mod
                        for x, mod in enumerate(line['modifiers'])
                    }
                })
            
            return data
        except Exception as e:
            cleanup_driver(driver)
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
