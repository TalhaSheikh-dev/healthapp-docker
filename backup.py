improve this one aswell

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
        data["patient_lastName"] = (driver.execute_script("return document.getElementsByName('dependent[lastName]')[0].value"))
        print("done3")
        data["patient_firstName"] = (driver.execute_script("return document.getElementsByName('dependent[firstName]')[0].value"))
        print("done4")    

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
            for x in range(0,4):
                key = "claim_serviceLines_" + str(i) +"_procedureModifiers_"+str(x) 	
                name = "return document.getElementsByName('claim[serviceLines]["+str(i)+"][procedureModifiers]["+str(x)+"]')[0].value"
                data[key] = (driver.execute_script(name))
                print("done78")

        return data
    except Exception as e:
        raise Exception(e)
    finally:
        cleanup_driver(driver)