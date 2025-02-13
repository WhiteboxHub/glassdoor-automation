import time
import random
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class GlassDoorEasyApply:
    def __init__(self, parameters, driver):
        self.browser = driver
        self.email = parameters['email']
        self.password = parameters['password']
        self.disable_lock = parameters['disableAntiLock']
        self.company_blacklist = parameters.get('companyBlacklist', []) or []
        self.title_blacklist = parameters.get('titleBlacklist', []) or []
        self.positions = parameters.get('positions', [])
        self.locations = parameters.get('locations', [])
        self.base_search_url = self.get_base_search_url(parameters)
        self.seen_jobs = []
        self.file_name = "output"
        self.output_file_directory = parameters['outputFileDirectory']
        self.resume_dir = parameters['uploads']['resume']
        self.photo_dir = parameters['uploads']['photo']
        self.cover_letter_dir = parameters['uploads'].get('coverLetter', '')
        self.checkboxes = parameters.get('checkboxes', [])
        self.university_gpa = parameters['universityGpa']
        self.languages = parameters.get('languages', [])
        self.industry = parameters.get('industry', [])
        self.technology = parameters.get('technology', [])
        self.personal_info = parameters.get('personalInfo', [])
        self.eeo = parameters.get('eeo', [])
        self.technology_default = self.technology.get('default', '')
        self.industry_default = self.industry.get('default', '')

    def get_base_search_url(self, parameters):
        # Construct the base search URL based on parameters
        base_url = "https://www.glassdoor.com/Job/jobs.htm"
        query_params = []
        if self.positions:
            query_params.append(f"keyword={'%20'.join(self.positions)}")
        if self.locations:
            query_params.append(f"locId={self.locations[0]}")
        if query_params:
            base_url += "?" + "&".join(query_params)
        return base_url


    def login(self):
        wait = WebDriverWait(self.browser, 20)
        try:
            self.browser.get("https://www.glassdoor.com/index.htm")
            time.sleep(random.uniform(2, 4))

            # Step 1: Locate and fill in the email field
            email_input = wait.until(EC.presence_of_element_located((By.ID, "inlineUserEmail")))
            email_input.clear()  # Clear any pre-existing text
            email_input.send_keys(self.email)
            print("✅ Email entered.")

            # Step 2: Click 'Continue with Email' button
            continue_button = wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "button[data-test='email-form-button']")))
            self.browser.execute_script("arguments[0].scrollIntoView();", continue_button)
            ActionChains(self.browser).move_to_element(continue_button).click().perform()
            print("✅ 'Continue with Email' button clicked.")

            # Step 3: Locate and fill in the password field
            password_input = wait.until(EC.presence_of_element_located((By.ID, "inlineUserPassword")))
            password_input.clear()  # Clear any pre-existing text
            password_input.send_keys(self.password)  # Make sure self.password is set to your actual password
            print("✅ Password entered.")


            # Step 4: Locate the **correct** Sign In button using XPath
            sign_in_button = wait.until(EC.element_to_be_clickable(
                 (By.XPATH, "//button[@class='Button Button' and contains(., 'Sign in')]")))
            self.browser.execute_script("arguments[0].scrollIntoView();", sign_in_button)
            ActionChains(self.browser).move_to_element(sign_in_button).click().perform()
            print("✅ Correct 'Sign In' button clicked.")

            # # Step 5: Wait for the Glassdoor homepage to load
            time.sleep(random.uniform(5, 7))

            # Step 6: Locate and click the "Jobs" button
            jobs_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//a[@href='/Job/index.htm']")))  # XPath for "Jobs" link
            self.browser.execute_script("arguments[0].scrollIntoView();", jobs_button)
            ActionChains(self.browser).move_to_element(jobs_button).click().perform()
            print("✅ 'Jobs' button clicked. Navigating to the job search page.")


            # Wait a little to see if login proceeds
            time.sleep(random.uniform(2, 4))

        except TimeoutException:
            print("❌ TimeoutException: Element not found within the wait time.")
        except NoSuchElementException:
            print("❌ NoSuchElementException: Element not found on the page.")
        except Exception as e:
            print("❌ Error during login:", e)


    def close_popups(self):
        """Close any blocking popups or overlays"""
        wait = WebDriverWait(self.browser, 5)

        popup_classes = [
            "modal_ModalOverlay__DXtn2",  # Main modal overlay
            "overlay_class_1",  # Replace with other known popup classes
            "overlay_class_2"
        ]

        for popup_class in popup_classes:
            try:
                popups = self.browser.find_elements(By.CLASS_NAME, popup_class)
                for popup in popups:
                    print(f"⚠️ Popup detected ({popup_class})! Closing it...")
                    self.browser.execute_script("arguments[0].click();", popup)
                    time.sleep(2)
            except:
                pass

        print("✅ No popups detected.")

    def retry_click(self, element, max_attempts=3):
        """Try clicking an element multiple times before giving up"""
        for attempt in range(max_attempts):
            try:
                element.click()
                return True  # Click successful
            except Exception as e:
                print(f"⚠️ Attempt {attempt+1} failed. Retrying...")
                time.sleep(1)  # Short delay before retrying
        return False  # Click failed after retries

    def search_job(self):
        wait = WebDriverWait(self.browser, 20)
        try:
            # Step 1: Click on the "Jobs" button
            jobs_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/Job/index.htm']")))
            jobs_button.click()
            print("✅ Clicked on 'Jobs' button.")
            time.sleep(3)  # Allow time for navigation

            # Step 2: Locate and enter job title
            job_input_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Find your perfect job']")))
            self.browser.execute_script("arguments[0].scrollIntoView();", job_input_field)
            time.sleep(1)

            # Try using ActionChains for clicking
            actions = ActionChains(self.browser)
            actions.move_to_element(job_input_field).click().perform()

            job_input_field.send_keys("Software Engineer")
            print("✅ Job title entered: 'Software Engineer'.")
            time.sleep(2)

            # Step 3: Enter location and press Enter
            location_input = wait.until(EC.element_to_be_clickable((By.ID, "searchBar-location")))
            location_input.click()
            time.sleep(1)
            location_input.send_keys("New York")
            time.sleep(1)
            location_input.send_keys(Keys.RETURN)  # Press Enter to update results
            time.sleep(3)  # Wait for the page to update

            # Step 4: Re-locate the location input to avoid stale reference error
            location_input = wait.until(EC.presence_of_element_located((By.ID, "searchBar-location")))
            entered_location = location_input.get_attribute("value")
            print(f"✅ Location confirmed: {entered_location}")

        except TimeoutException:
            print("❌ TimeoutException: Element not found within the wait time.")
        except NoSuchElementException:
            print("❌ NoSuchElementException: Element not found on the page.")
        except Exception as e:
            print("❌ Error during job search:", e)

    def click_easy_apply_filter(self):
        """Click 'Easy Apply Only' filter"""
        wait = WebDriverWait(self.browser, 15)
        self.close_popups()  # Close popups before clicking

        try:
            easy_apply_filter = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test='applicationType']")))
            self.browser.execute_script("arguments[0].scrollIntoView();", easy_apply_filter)
            time.sleep(1)

            if not self.retry_click(easy_apply_filter):
                print("❌ Failed to click 'Easy Apply Only' filter after retries.")

            print("✅ 'Easy Apply Only' filter clicked successfully.")
            time.sleep(2)

            print('----------------------------------------------------------------')

        except Exception as e:
            print(f"❌ Error clicking 'Easy Apply Only' filter: {e}")

    

    def select_first_job(self):
        """Click the first job listing with retries"""
        wait = WebDriverWait(self.browser, 15)
        self.close_popups()  # Close popups before clicking

        max_retries = 3
        for attempt in range(max_retries):
            try:
                job_listings = wait.until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "JobCard_trackingLink__HMyun"))
                )

                if not job_listings:
                    print("❌ No job listings found.")
                    return False

                first_job = job_listings[0]
                self.browser.execute_script("arguments[0].scrollIntoView();", first_job)
                time.sleep(1)

                try:
                    first_job.click()
                except:
                    print("⚠️ Normal click failed. Trying JavaScript click.")
                    self.browser.execute_script("arguments[0].click();", first_job)

                print("✅ Clicked on the first job listing.")
                time.sleep(3)
                return True  # Success, exit function

            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed. Retrying... ({e})")
                time.sleep(2)  # Wait before retrying

        print("❌ Failed to click the first job listing after retries.")
        return False  # Return False if all retries fail


    def easy_apply_job(self):
        """Click 'Easy Apply' button on the job listing"""
        wait = WebDriverWait(self.browser, 15)
        self.close_popups()  # Close popups before clicking

        try:
            easy_apply_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test='easyApply']")))
            self.browser.execute_script("arguments[0].scrollIntoView();", easy_apply_button)
            time.sleep(1)

            if not self.retry_click(easy_apply_button):
                print("❌ Failed to click 'Easy Apply' button after retries.")

            print("✅ 'Easy Apply' button clicked successfully.")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Error clicking 'Easy Apply' button: {e}")

    def apply_to_jobs(self):
        """Run the full Easy Apply process"""
        print("🚀 Starting job application process...")

        # Step 1: Search for jobs
        self.search_job()

        # Step 2: Apply Easy Apply filter
        self.click_easy_apply_filter()

        # Step 3: Click the first job listing
        job_selected = self.select_first_job()

        if job_selected:
            # Step 4: Click 'Easy Apply'
            self.easy_apply_job()
        time.sleep(10)
        print("✅ Job application process completed.")


    

    def select_resume_and_continue(self):
        """Select the uploaded resume and proceed to the next step."""
        try:
            print("✅ Waiting for the resume selection page...")

            wait = WebDriverWait(self.browser, 15)

            # ✅ Wait for resume selection to load
            resume_radio_xpath = "//input[@type='radio' and @name='resumeType']"
            wait.until(EC.presence_of_element_located((By.XPATH, resume_radio_xpath)))
            print("✅ Resume selection page detected.")

            # ✅ Check if resume is already selected
            resume_radio_button = self.browser.find_element(By.XPATH, resume_radio_xpath)
            if not resume_radio_button.is_selected():
                print("⚠️ Resume not selected, selecting it now...")
                resume_label_xpath = "//label[contains(@data-testid, 'FileResumeCard-label')]"
                resume_label = wait.until(EC.element_to_be_clickable((By.XPATH, resume_label_xpath)))

                # Scroll to resume and click
                self.browser.execute_script("arguments[0].scrollIntoView();", resume_label)
                time.sleep(1)
                resume_label.click()
                print("✅ Resume selected.")

            time.sleep(5)  # Ensure selection is processed

            # ✅ Click the SVG button (checkmark)
            try:
                print("✅ Waiting for SVG button (checkmark)...")
                svg_button_xpath = "//svg[contains(@class, 'css-s92xw2')]"
                svg_button = wait.until(EC.element_to_be_clickable((By.XPATH, svg_button_xpath)))

                # Scroll into view
                self.browser.execute_script("arguments[0].scrollIntoView();", svg_button)
                time.sleep(1)

                try:
                    svg_button.click()
                    print("✅ SVG button clicked successfully.")
                except:
                    print("⚠️ Normal click failed. Trying JavaScript click...")
                    self.browser.execute_script("arguments[0].click();", svg_button)

            except TimeoutException:
                print("❌ TimeoutException: SVG button not found.")
            except Exception as e:
                print(f"❌ Error clicking SVG button: {e}")

            time.sleep(5)  # Ensure SVG click is processed

            # ✅ Click "Continue" button
            continue_button_xpath = "//button[contains(text(), 'Continue')]"
            continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, continue_button_xpath)))

            try:
                continue_button.click()
                print("✅ Clicked 'Continue' after selecting resume and clicking SVG.")
            except:
                print("⚠️ Normal click failed. Trying JavaScript click...")
                self.browser.execute_script("arguments[0].click();", continue_button)

            time.sleep(3)

        except TimeoutException:
            print("❌ TimeoutException: Resume selection page did not load in time.")
        except Exception as e:
            print(f"❌ Error selecting resume: {e}")


    

    def enter_mobile_number(self, mobile_number):
        """Enter mobile number after clicking 'Continue'."""
        try:
            print("🚀 Entering mobile number...")

            mobile_input_xpath = "//input[@type='tel']"

            # Wait for the mobile input field
            mobile_input = WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located((By.XPATH, mobile_input_xpath))
            )

            # Click the input field to activate it
            self.browser.execute_script("arguments[0].scrollIntoView();", mobile_input)
            mobile_input.click()
            time.sleep(1)

            # Enter mobile number
            mobile_input.clear()
            mobile_input.send_keys(mobile_number)
            print(f"✅ Mobile number entered: {mobile_number}")

            # ✅ Click "Continue" button
            continue_button_xpath = "//button[contains(text(), 'Continue')]"
            continue_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, continue_button_xpath))
            )
            try:
                continue_button.click()
            except Exception:
                print("⚠️ Normal click failed. Trying JavaScript click...")
                self.browser.execute_script("arguments[0].click();", continue_button)

            print("✅ Clicked on 'Continue' after entering mobile number.")

        except Exception as e:
            print(f"❌ Failed to enter mobile number: {e}")

    def select_yes_no_options(self):
        """Automatically select 'Yes' or 'No' options."""
        try:
            print("🚀 Selecting 'Yes' or 'No' options...")

            yes_no_buttons_xpath = "//button[contains(text(), 'Yes') or contains(text(), 'No')]"

            # Wait for the Yes/No buttons
            yes_no_buttons = WebDriverWait(self.browser, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, yes_no_buttons_xpath))
            )

            for button in yes_no_buttons:
                self.browser.execute_script("arguments[0].scrollIntoView();", button)
                time.sleep(1)
                self.browser.execute_script("arguments[0].click();", button)  # JS Click
                print(f"✅ Clicked on '{button.text}' button.")

            # ✅ Click "Continue" button after selecting options
            continue_button_xpath = "//button[contains(text(), 'Continue')]"
            continue_button = WebDriverWait(self.browser, 10).until(
                EC.element_to_be_clickable((By.XPATH, continue_button_xpath))
            )
            try:
                continue_button.click()
            except Exception:
                print("⚠️ Normal click failed. Trying JavaScript click...")
                self.browser.execute_script("arguments[0].click();", continue_button)

            print("✅ Clicked on 'Continue' after selecting options.")

        except Exception as e:
            print(f"❌ Failed to select 'Yes' or 'No' options: {e}")


            


    def security_check(self):
        """Handles potential CAPTCHA or additional verification steps"""
        try:
            wait = WebDriverWait(self.browser, 5)
            captcha_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="recaptcha challenge"]')))
            if captcha_box:
                print("CAPTCHA detected. Please solve it manually.")
                input("Press Enter after solving CAPTCHA...")

        except Exception:
            print("No CAPTCHA detected. Continuing...")

    def start_applying(self):
        """Function placeholder for job application automation"""
        print("Starting job application process... (To be implemented)")

# Example usage
if __name__ == "__main__":
    parameters = {
        'email': 'your_email@example.com',
        'password': 'your_password',
        'disableAntiLock': True,
        'companyBlacklist': [],
        'titleBlacklist': [],
        'positions': ['Software Engineer'],
        'locations': ['1147221'],  # Example location ID for San Francisco
        'outputFileDirectory': '/path/to/output',
        'uploads': {
            'resume': '/path/to/resume.pdf',
            'photo': '/path/to/photo.jpg',
            'coverLetter': '/path/to/cover_letter.pdf'
        },
        'universityGpa': '3.5',
        'languages': ['English', 'Spanish'],
        'industry': {'default': 'Technology'},
        'technology': {'default': 'Python'},
        'personalInfo': {},
        'eeo': {}
    }

    # Initialize the WebDriver (make sure to specify the correct path to chromedriver)
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

    # Create an instance of GlassDoorEasyApply and log in
    glassdoor_bot = GlassDoorEasyApply(parameters, driver)
    glassdoor_bot.login()
    glassdoor_bot.security_check()
    glassdoor_bot.start_applying()

    # Close the browser
    driver.quit()



# --------------------------------------------------------------------------------------------------
    def check_notif_modal(self):
        try:
            self.browser.find_element_by_class_name("modal_main")
            self.browser.find_element_by_class_name("modal_closeIcon").click()
        except:
            pass
        
    def get_base_with_location(self, location, position):
        self.browser.find_element_by_id("sc.keyword").send_keys(position)
        loc = self.browser.find_element_by_id("sc.location")
        loc.send_keys(Keys.CONTROL + 'a')
        time.sleep(2)
        loc.send_keys(Keys.DELETE)
        time.sleep(3)
        loc = self.browser.find_element_by_id("sc.location")
        loc.send_keys(location)
        time.sleep(1)
        loc.send_keys(Keys.ARROW_DOWN)
        time.sleep(1)
        loc.send_keys(Keys.RETURN)
        time.sleep(2)
        self.browser.find_element_by_xpath('//*[@id="Discover"]/div/div/div[1]/div[1]/div[3]/a/strong').click()
        self.check_notif_modal()
        current_url = self.browser.current_url
        base_url = current_url.split('.htm')[0]
        return base_url + ".htm"
        
    def start_applying(self):
        searches = list(product(self.positions, self.locations))
        random.shuffle(searches)

        page_sleep = 0
        minimum_time = 30*1
        minimum_page_time = time.time() + minimum_time

        for (position, location) in searches:

            print("Starting the search for " + position + " in " + location + ".")
            base_url = self.get_base_with_location(location, position)
            job_page_number = -1


            try:
                while True:
                    page_sleep += 1
                    job_page_number += 1
                    print("Going to job page " + str(job_page_number))
                    self.next_job_page(base_url, job_page_number)
                    time.sleep(random.uniform(1.5, 3.5))
                    print("Starting the application process for this page...")
                    self.apply_jobs(location)
                    print("Applying to jobs on this page has been completed!")

                    time_left = minimum_page_time - time.time()
                    if time_left > 0:
                        print("Sleeping for " + str(time_left) + " seconds.")
                        time.sleep(time_left)
                        minimum_page_time = time.time() + minimum_time
                    if page_sleep % 5 == 0:
                        sleep_time = random.randint(50, 100)
                        print("Sleeping for " + str(sleep_time/60) + " minutes.")
                        time.sleep(sleep_time)
                        page_sleep += 1
            except:
                traceback.print_exc()
                pass

            time_left = minimum_page_time - time.time()
            if time_left > 0:
                print("Sleeping for " + str(time_left) + " seconds.")
                time.sleep(time_left)
                minimum_page_time = time.time() + minimum_time
            if page_sleep % 5 == 0:
                sleep_time = random.randint(100, 300)
                print("Sleeping for " + str(sleep_time/60) + " minutes.")
                time.sleep(sleep_time)
                page_sleep += 1


    def apply_jobs(self, location):
        no_jobs_text = ""
        try:
            no_jobs_element = self.browser.find_element_by_class_name('scaffold-layout__list-detail')
            no_jobs_text = no_jobs_element.text
        except:
            pass
        if 'No matching jobs found' in no_jobs_text:
            raise Exception("No more jobs on this page")

        if 'unfortunately, things aren' in self.browser.page_source.lower():
            raise Exception("No more jobs on this page")
        try:
            job_results = self.browser.find_element_by_id("MainCol")
            self.scroll_slow(job_results)
            self.scroll_slow(job_results, step=250, reverse=True)
# //*[@id="MainCol"]/div[1]/ul/li[1]
# //*[@id="MainCol"]/div[1]/ul/li[2]
            # job_list = self.browser.find_elements_by_class_name('scaffold-layout__list-container')[0].find_elements_by_class_name('jobs-search-results__list')
            job_list = self.browser.find_elements_by_xpath('//*[@id="MainCol"]/div[1]/ul/li')
        except:
            raise Exception("No more jobs on this page")

        if len(job_list) == 0:
            raise Exception("No more jobs on this page")

        for job_tile in job_list:
            job_title, company, job_location, apply_method, link = "", "", "", "", ""

            try:
                job_title = job_tile.find_element_by_class_name('eigr9kq1').find_element_by_tag_name('span').text
                link = job_tile.find_element_by_class_name('job-search-key-1rd3saf').get_attribute('href').split('?')[0]
            except:
                pass
            try:
                company = job_tile.find_element_by_class_name('e1n63ojh0').find_element_by_tag_name('span').text
            except:
                pass
            try:
                job_location = job_tile.find_element_by_class_name('e1rrn5ka').text
            except:
                pass
            try:
                apply_method = job_tile.find_element_by_class_name('job-card-container__apply-method').text
            except:
                pass

            contains_blacklisted_keywords = False
            job_title_parsed = job_title.lower().split(' ')

            for word in self.title_blacklist:
                if word.lower() in job_title_parsed:
                    contains_blacklisted_keywords = True
                    break

            if company.lower() not in [word.lower() for word in self.company_blacklist] and \
               contains_blacklisted_keywords is False and link not in self.seen_jobs:
                try:
                    job_el = job_tile.find_element_by_class_name('eigr9kq1')
                    job_el.click()

                    time.sleep(random.uniform(3, 5))

                    try:
                        done_applying = self.apply_to_job()
                        if done_applying:
                            print("Done applying to the job!")
                        else:
                            print('Already applied to the job!')
                        # self.browser.close()
                        # self.browser.switch_to.window(self.browser.window_handles[0])

                    except:
                        temp = self.file_name
                        self.file_name = "failed"
                        print("Failed to apply to job! Please submit a bug report with this link: " + link)
                        print("Writing to the failed csv file...")
                        try:
                            self.write_to_file(company, job_title, link, job_location, location)
                        except:
                            pass
                        self.file_name = temp

                    try:
                        self.write_to_file(company, job_title, link, job_location, location)
                    except Exception:
                        print("Could not write the job to the file! No special characters in the job title/company is allowed!")
                        traceback.print_exc()
                except:
                    traceback.print_exc()
                    print("Could not apply to the job!")
                    pass
            else:
                print("Job contains blacklisted keyword or company name!")
            self.seen_jobs += link

    def apply_to_job(self):
        easy_apply_button = None

        try:
            easy_apply_button = self.browser.find_element_by_class_name('e1mdf2m0')
        except:
            return False

        # try:
        #     job_description_area = self.browser.find_element_by_class_name("JDCol")
        #     self.scroll_slow(job_description_area, end=1200)
        #     self.scroll_slow(job_description_area, end=1200, step=400, reverse=True)
        # except:
        #     pass

        print("Applying to the job....")
        easy_apply_button.click()

        button_text = ""
        submit_application_text = 'Apply'
        while submit_application_text not in button_text.lower():
            retries = 3
            while retries > 0:
                try:
                    self.fill_up()
                    next_button = self.browser.find_element_by_class_name("icl-Button")
                    button_text = next_button.text.lower()
                    if submit_application_text in button_text:
                        try:
                            self.unhallow()
                        except:
                            print("Failed to unfollow company!")
                    time.sleep(random.uniform(1.5, 2.5))
                    next_button.click()
                    time.sleep(random.uniform(3.0, 5.0))

                    if 'please enter a valid answer' in self.browser.page_source.lower() or 'file is required' in self.browser.page_source.lower():
                        retries -= 1
                        print("Retrying application, attempts left: " + str(retries))
                    else:
                        break
                except:
                    traceback.print_exc()
                    raise Exception("Failed to apply to job!")
            if retries == 0:
                traceback.print_exc()
                self.browser.find_element_by_class_name('artdeco-modal__dismiss').click()
                time.sleep(random.uniform(3, 5))
                self.browser.find_elements_by_class_name('artdeco-modal__confirm-dialog-btn')[1].click()
                time.sleep(random.uniform(3, 5))
                raise Exception("Failed to apply to job!")

        closed_notification = False
        time.sleep(random.uniform(3, 5))
        try:
            self.browser.find_element_by_class_name('artdeco-modal__dismiss').click()
            closed_notification = True
        except:
            pass
        try:
            self.browser.find_element_by_class_name('artdeco-toast-item__dismiss').click()
            closed_notification = True
        except:
            pass
        time.sleep(random.uniform(3, 5))

        if closed_notification is False:
            raise Exception("Could not close the applied confirmation window!")

        return True

    def home_address(self, element):
        try:
            groups = element.find_elements_by_class_name('ia-UserFields')
            if len(groups) > 0:
                for group in groups:
                    lb = group.find_element_by_tag_name('label').find_element_by_tag_name('span').text.lower()
                    input_field = group.find_element_by_tag_name('input')
                    if 'street' in lb:
                        self.enter_text(input_field, self.personal_info['Street address'])
                    elif 'city' in lb:
                        self.enter_text(input_field, self.personal_info['City'])
                        time.sleep(5)
                        input_field.send_keys(Keys.DOWN)
                        time.sleep(1)
                        input_field.send_keys(Keys.RETURN)
                    elif 'zip' in lb or 'postal' in lb:
                        self.enter_text(input_field, self.personal_info['Zip'])
                    elif 'state' in lb or 'province' in lb:
                        self.enter_text(input_field, self.personal_info['State'])
                    else:
                        pass
        except:
            pass

    def get_answer(self, question):
        if self.checkboxes[question]:
            return 'yes'
        else:
            return 'no'

    def additional_questions(self):
        #pdb.set_trace()
        frm_el = self.browser.find_elements_by_class_name('icl-TextInput-wrapper')
        if len(frm_el) > 0:
            for el in frm_el:
                # Radio check
                try:
                    radios = el.find_element_by_class_name('jobs-easy-apply-form-element').find_elements_by_class_name('fb-radio')

                    radio_text = el.text.lower()
                    radio_options = [text.text.lower() for text in radios]
                    answer = "yes"

                    if 'driver\'s licence' in radio_text or 'driver\'s license' in radio_text:
                        answer = self.get_answer('driversLicence')
                    elif 'gender' in radio_text or 'veteran' in radio_text or 'race' in radio_text or 'disability' in radio_text or 'latino' in radio_text:
                        answer = ""
                        for option in radio_options:
                            if 'prefer' in option.lower() or 'decline' in option.lower() or 'don\'t' in option.lower() or 'specified' in option.lower() or 'none' in option.lower():
                                answer = option

                        if answer == "":
                            answer = radio_options[len(radio_options) - 1]
                    elif 'north korea' in radio_text:
                        answer = 'no'
                    elif 'sponsor' in radio_text:
                        answer = self.get_answer('requireVisa')
                    elif 'authorized' in radio_text or 'authorised' in radio_text or 'legally' in radio_text:
                        answer = self.get_answer('legallyAuthorized')
                    elif 'urgent' in radio_text:
                        answer = self.get_answer('urgentFill')
                    elif 'commuting' in radio_text:
                        answer = self.get_answer('commute')
                    elif 'background check' in radio_text:
                        answer = self.get_answer('backgroundCheck')
                    elif 'remote' in radio_text:
                        answer = self.get_answer('remote')
                    elif 'level of education' in radio_text:
                        for degree in self.checkboxes['degreeCompleted']:
                            if degree.lower() in radio_text:
                                answer = "yes"
                                break
                    elif 'level of education' in radio_text:
                        for degree in self.checkboxes['degreeCompleted']:
                            if degree.lower() in radio_text:
                                answer = "yes"
                                break
                    elif 'data retention' in radio_text:
                        answer = 'no'
                    elif 'drug' in radio_text:
                        answer = self.get_answer('drugTest')
                    else:
                        answer = radio_options[len(radio_options) - 1]

                    i = 0
                    to_select = None
                    for radio in radios:
                        if answer in radio.text.lower():
                            to_select = radios[i]
                        i += 1

                    if to_select is None:
                        to_select = radios[len(radios)-1]

                    self.radio_select(to_select, answer, len(radios) > 2)

                    if radios != []:
                        continue
                except:
                    pass
                # Questions check
                try:
                    question = el.find_element_by_class_name('jobs-easy-apply-form-element')
                    question_text = question.find_element_by_class_name('fb-form-element-label').text.lower()

                    txt_field_visible = False
                    try:
                        txt_field = question.find_element_by_class_name('fb-single-line-text__input')

                        txt_field_visible = True
                    except:
                        try:
                            txt_field = question.find_element_by_class_name('fb-textarea')

                            txt_field_visible = True
                        except:
                            pass

                    if txt_field_visible != True:
                        txt_field = question.find_element_by_class_name('multi-line-text__input')

                    text_field_type = txt_field.get_attribute('name').lower()
                    if 'numeric' in text_field_type:
                        text_field_type = 'numeric'
                    elif 'text' in text_field_type:
                        text_field_type = 'text'

                    to_enter = ''
                    if 'experience do you currently have' in question_text:
                        no_of_years = self.industry_default

                        for industry in self.industry:
                            if industry.lower() in question_text:
                                no_of_years = self.industry[industry]
                                break

                        to_enter = no_of_years
                    elif 'many years of work experience do you have using' in question_text:
                        no_of_years = self.technology_default

                        for technology in self.technology:
                            if technology.lower() in question_text:
                                no_of_years = self.technology[technology]

                        to_enter = no_of_years
                    elif 'grade point average' in question_text:
                        to_enter = self.university_gpa
                    elif 'first name' in question_text:
                        to_enter = self.personal_info['First Name']
                    elif 'last name' in question_text:
                        to_enter = self.personal_info['Last Name']
                    elif 'name' in question_text:
                        to_enter = self.personal_info['First Name'] + " " + self.personal_info['Last Name']
                    elif 'phone' in question_text:
                        to_enter = self.personal_info['Mobile Phone Number']
                    elif 'linkedin' in question_text:
                        to_enter = self.personal_info['Linkedin']
                    elif 'website' in question_text or 'github' in question_text or 'portfolio' in question_text:
                        to_enter = self.personal_info['Website']
                    elif 'summary' in question_text:
                        to_enter = self.personal_info['Summary']
                    elif 'headline' in question_text:
                        to_enter = self.personal_info['Headline']
                    elif 'education' in question_text:
                        to_enter = self.personal_info['University']
                    else:
                        if text_field_type == 'numeric':
                            to_enter = 0
                        else:
                            to_enter = " ‏‏‎ "

                    if text_field_type == 'numeric':
                        if not isinstance(to_enter, (int, float)):
                            to_enter = 0
                    elif to_enter == '':
                        to_enter = " ‏‏‎ "

                    self.enter_text(txt_field, to_enter)
                    continue
                except:
                    pass
                # Date Check
                try:
                    date_picker = el.find_element_by_class_name('artdeco-datepicker__input ')
                    date_picker.clear()
                    date_picker.send_keys(date.today().strftime("%m/%d/%y"))
                    time.sleep(3)
                    date_picker.send_keys(Keys.RETURN)
                    time.sleep(2)
                    continue
                except:
                    pass
                # Dropdown check
                try:
                    question = el.find_element_by_class_name('jobs-easy-apply-form-element')
                    question_text = question.find_element_by_class_name('fb-form-element-label').text.lower()

                    dropdown_field = question.find_element_by_class_name('fb-dropdown__select')

                    select = Select(dropdown_field)

                    options = [options.text for options in select.options]

                    if 'proficiency' in question_text:
                        proficiency = "Conversational"

                        for language in self.languages:
                            if language.lower() in question_text:
                                proficiency = self.languages[language]
                                break

                        self.select_dropdown(dropdown_field, proficiency)
                    elif 'country code' in question_text:
                        self.select_dropdown(dropdown_field, self.personal_info['Phone Country Code'])
                    elif 'north korea' in question_text:

                        choice = ""

                        for option in options:
                            if 'no' in option.lower():
                                choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    elif 'sponsor' in question_text:
                        answer = self.get_answer('requireVisa')

                        choice = ""

                        for option in options:
                            if answer == 'yes':
                                choice = option
                            else:
                                if 'no' in option.lower():
                                    choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    elif 'authorized' in question_text or 'authorised' in question_text:
                        answer = self.get_answer('legallyAuthorized')

                        choice = ""

                        for option in options:
                            if answer == 'yes':
                                # find some common words
                                choice = option
                            else:
                                if 'no' in option.lower():
                                    choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    elif 'citizenship' in question_text:
                        answer = self.get_answer('legallyAuthorized')

                        choice = ""

                        for option in options:
                            if answer == 'yes':
                                if 'no' in option.lower():
                                    choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    elif 'gender' in question_text or 'veteran' in question_text or 'race' in question_text or 'disability' in question_text or 'latino' in question_text:

                        choice = ""

                        for option in options:
                            if 'prefer' in option.lower() or 'decline' in option.lower() or 'don\'t' in option.lower() or 'specified' in option.lower() or 'none' in option.lower():
                                choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    else:
                        choice = ""

                        for option in options:
                            if 'yes' in option.lower():
                                choice = option

                        if choice == "":
                            choice = options[len(options) - 1]

                        self.select_dropdown(dropdown_field, choice)
                    continue
                except:
                    pass

                # Checkbox check for agreeing to terms and service
                try:
                    question = el.find_element_by_class_name('jobs-easy-apply-form-element')

                    clickable_checkbox = question.find_element_by_tag_name('label')

                    clickable_checkbox.click()
                except:
                    pass

    def unhallow(self):
        try:
            follow_checkbox = self.browser.find_element(By.XPATH, "//label[contains(.,\'to stay up to date with their page.\')]").click()
            follow_checkbox.click()
        except:
            pass

    def send_resume(self):
        try:
            file_upload_elements = (By.CSS_SELECTOR, "input[name='file']")
            if len(self.browser.find_elements(file_upload_elements[0], file_upload_elements[1])) > 0:
                input_buttons = self.browser.find_elements(file_upload_elements[0], file_upload_elements[1])
                for upload_button in input_buttons:
                    upload_type = upload_button.find_element(By.XPATH, "..").find_element(By.XPATH, "preceding-sibling::*")
                    if 'resume' in upload_type.text.lower():
                        upload_button.send_keys(self.resume_dir)
                    elif 'cover' in upload_type.text.lower():
                        if self.cover_letter_dir != '':
                            upload_button.send_keys(self.cover_letter_dir)
                        elif 'required' in upload_type.text.lower():
                            upload_button.send_keys(self.resume_dir)
                    elif 'photo' in upload_type.text.lower():
                        upload_button.send_keys(self.photo_dir)
        except:
            print("Failed to upload resume or cover letter!")
            pass


    def enter_text(self, element, text):
        element.clear()
        element.send_keys(text)

    def select_dropdown(self, element, text):
        select = Select(element)
        select.select_by_visible_text(text)

    # Radio Select
    def radio_select(self, element, label_text, clickLast=False):
        label = element.find_element_by_tag_name('label')
        if label_text in label.text.lower() or clickLast == True:
            label.click()
        else:
            pass

    # Contact info fill-up
    def contact_info(self):
        frm_el = self.browser.find_elements_by_class_name('jobs-easy-apply-form-section__grouping')
        if len(frm_el) > 0:
            for el in frm_el:
                text = el.text.lower()
                if 'email address' in text:
                    continue
                elif 'phone number' in text:
                    try:
                        country_code_picker = el.find_element_by_class_name('fb-dropdown__select')
                        self.select_dropdown(country_code_picker, self.personal_info['Phone Country Code'])
                    except:
                        print("Country code " + self.personal_info['Phone Country Code'] + " not found! Make sure it is exact.")
                    try:
                        phone_number_field = el.find_element_by_class_name('fb-single-line-text__input')
                        self.enter_text(phone_number_field, self.personal_info['Mobile Phone Number'])
                    except:
                        print("Could not input phone number.")

    def fill_up(self):
        try:
            time.sleep(2)
            # seems that this component may be hidden??? cannot find
            easy_apply_content = self.browser.find_element_by_xpath('//*[@id="ia-ApplyFormScreen"]/div[2]/form')
            b4 = easy_apply_content.find_element_by_class_name('ia-UserFields-fragment')
            pb4 = easy_apply_content.find_elements_by_class_name('ia-UserFields-fragment')
            if len(pb4) > 0:
                    try:
                        label = pb.find_element_by_tag_name('h3').text.lower()
                        try:
                            self.additional_questions()
                        except:
                            pass

                        try:
                            self.send_resume()
                        except:
                            pass

                        if 'Address' in label:
                            self.home_address(pb)
                        elif 'contact info' in label:
                            self.contact_info()
                    except:
                        pass
        except:
            pass
    
    def write_to_file(self, company, job_title, link, location, search_location):
        to_write = [company, job_title, link, location]
        file_path = self.output_file_directory + self.file_name + search_location + ".csv"

        with open(file_path, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(to_write)

    def scroll_slow(self, scrollable_element, start=0, end=3600, step=100, reverse=False):
        if reverse:
            start, end = end, start
            step = -step

        for i in range(start, end, step):
            self.browser.execute_script("arguments[0].scrollTo(0, {})".format(i), scrollable_element)
            time.sleep(random.uniform(1.0, 2.6))

    def avoid_lock(self):
        if self.disable_lock:
            return

        pyautogui.keyDown('ctrl')
        pyautogui.press('esc')
        pyautogui.keyUp('ctrl')
        time.sleep(1.0)
        pyautogui.press('esc')

    def get_base_search_url(self, parameters):
        remote_url = ""

        if parameters['remote']:
            remote_url = "?remoteWorkType=1"

        distance_url = "?radius=" + str(parameters['distance'])

        # job_types_url = "?jobType="
        # job_types = parameters.get('jobTypes', [])
        # for key in job_types:
        #     if job_types[key]:
        #         job_types_url += "%2C" + key.lower()

        date_url = ""
        if parameters['date']["Age"]:
            date_url = "&fromAge=" + str(parameters['date']['Age'])

        easy_apply_url = "&applicationType=1"

        extra_search_terms = [distance_url, remote_url]
        extra_search_terms_str = '&'.join(term for term in extra_search_terms if len(term) > 0) + easy_apply_url + date_url

        return extra_search_terms_str

    def next_job_page(self, base_url, job_page):
        self.browser.get(base_url + self.base_search_url)

        self.avoid_lock()

