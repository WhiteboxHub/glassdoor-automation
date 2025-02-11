# import yaml, pdb
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from glassdooreasyapply import GlassDoorEasyApply
# from validate_email import validate_email
# # i added this below three lines 
# from selenium.webdriver.common.by import By  
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# def init_browser():
#     browser_options = Options()
#     options = ['--disable-blink-features', '--no-sandbox', '--start-maximized', '--disable-extensions',
#                '--ignore-certificate-errors', '--disable-blink-features=AutomationControlled']

#     for option in options:
#         browser_options.add_argument(option)

#     # driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=browser_options)
#     driver = webdriver.Chrome(service=webdriver.ChromeService(ChromeDriverManager().install()), options=browser_options)



#     driver.set_window_position(0, 0)
#     driver.maximize_window()

#     return driver


# def validate_yaml():
#     with open("config.yaml", 'r') as stream:
#         try:
#             parameters = yaml.safe_load(stream)
#         except yaml.YAMLError as exc:
#             raise exc

#     mandatory_params = ['email', 'password', 'disableAntiLock', 'remote', 'experienceLevel', 'jobTypes', 'date',
#                         'positions', 'locations', 'distance', 'outputFileDirectory', 'checkboxes', 'universityGpa',
#                         'languages', 'industry', 'technology', 'personalInfo', 'eeo', 'uploads']

#     for mandatory_param in mandatory_params:
#         if mandatory_param not in parameters:
#             raise Exception(mandatory_param + ' is not inside the yml file!')

#     assert validate_email(parameters['email'])
#     assert len(str(parameters['password'])) > 0

#     assert isinstance(parameters['disableAntiLock'], bool)

#     assert isinstance(parameters['remote'], bool)

#     assert len(parameters['experienceLevel']) > 0
#     experience_level = parameters.get('experienceLevel', [])
#     at_least_one_experience = False
#     for key in experience_level.keys():
#         if experience_level[key]:
#             at_least_one_experience = True
#     assert at_least_one_experience

#     assert len(parameters['jobTypes']) > 0
#     job_types = parameters.get('jobTypes', [])
#     at_least_one_job_type = False
#     for key in job_types.keys():
#         if job_types[key]:
#             at_least_one_job_type = True
#     assert at_least_one_job_type

#     assert len(parameters['date']) > 0
#     date = parameters.get('date', [])
#     at_least_one_date = False
#     for key in date.keys():
#         if date[key]:
#             at_least_one_date = True
#     assert at_least_one_date

#     approved_distances = {0, 5, 10, 25, 50, 100}
#     assert parameters['distance'] in approved_distances

#     assert len(parameters['positions']) > 0
#     assert len(parameters['locations']) > 0

#     assert len(parameters['uploads']) >= 1 and 'resume' in parameters['uploads']

#     assert len(parameters['checkboxes']) > 0

#     checkboxes = parameters.get('checkboxes', [])
#     assert isinstance(checkboxes['driversLicence'], bool)
#     assert isinstance(checkboxes['requireVisa'], bool)
#     assert isinstance(checkboxes['legallyAuthorized'], bool)
#     assert isinstance(checkboxes['urgentFill'], bool)
#     assert isinstance(checkboxes['commute'], bool)
#     assert isinstance(checkboxes['backgroundCheck'], bool)
#     assert 'degreeCompleted' in checkboxes

#     assert isinstance(parameters['universityGpa'], (int, float))

#     languages = parameters.get('languages', [])
#     language_types = {'none', 'conversational', 'professional', 'native or bilingual'}
#     for language in languages:
#         assert languages[language].lower() in language_types

#     industry = parameters.get('industry', [])

#     for skill in industry:
#         assert isinstance(industry[skill], int)
#     assert 'default' in industry

#     technology = parameters.get('technology', [])

#     for tech in technology:
#         assert isinstance(technology[tech], int)
#     assert 'default' in technology

#     assert len(parameters['personalInfo'])
#     personal_info = parameters.get('personalInfo', [])
#     for info in personal_info:
#         assert personal_info[info] != ''

#     assert len(parameters['eeo'])
#     eeo = parameters.get('eeo', [])
#     for survey_question in eeo:
#         assert eeo[survey_question] != ''

#     return parameters


# if __name__ == '__main__':
#     parameters = validate_yaml()
#     browser = init_browser()

#     bot = GlassDoorEasyApply(parameters, browser)
#     # i add below this lines 
# class GlassDoorEasyApply:
#     def __init__(self, parameters, browser):
#         self.parameters = parameters
#         self.browser = browser

#     def login(self):
#         wait = WebDriverWait(self.browser, 10)  # Wait up to 10 seconds
#         try:
#             login_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#SiteNav button")))
#             login_button.click()
#             print("Login button clicked.")
#         except Exception as e:
#             print("Error:", e)
#     # bot.login()
#     # bot.security_check()
#     # bot.start_applying()
#     print("Start")
#     bot.login() 
#     print("End")







import yaml
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from glassdooreasyapply import GlassDoorEasyApply
from validate_email import validate_email


def init_browser():
    browser_options = Options()
    options = [
        '--disable-blink-features',
        '--no-sandbox',
        '--start-maximized',
        '--disable-extensions',
        '--ignore-certificate-errors',
        '--disable-blink-features=AutomationControlled'
    ]

    for option in options:
        browser_options.add_argument(option)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=browser_options)
    driver.set_window_position(0, 0)
    driver.maximize_window()
    return driver


def validate_yaml():
    with open("config.yaml", 'r') as stream:
        try:
            parameters = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc

    mandatory_params = [
        'email', 'password', 'disableAntiLock', 'remote', 'experienceLevel',
        'jobTypes', 'date', 'positions', 'locations', 'distance',
        'outputFileDirectory', 'checkboxes', 'universityGpa', 'languages',
        'industry', 'technology', 'personalInfo', 'eeo', 'uploads'
    ]

    for mandatory_param in mandatory_params:
        if mandatory_param not in parameters:
            raise Exception(mandatory_param + ' is not inside the yml file!')

    assert validate_email(parameters['email'])
    assert len(str(parameters['password'])) > 0
    assert isinstance(parameters['disableAntiLock'], bool)
    assert isinstance(parameters['remote'], bool)
    assert len(parameters['experienceLevel']) > 0
    assert any(parameters['experienceLevel'].values())
    assert len(parameters['jobTypes']) > 0
    assert any(parameters['jobTypes'].values())
    assert len(parameters['date']) > 0
    assert any(parameters['date'].values())

    approved_distances = {0, 5, 10, 25, 50, 100}
    assert parameters['distance'] in approved_distances
    assert len(parameters['positions']) > 0
    assert len(parameters['locations']) > 0
    assert len(parameters['uploads']) >= 1 and 'resume' in parameters['uploads']
    assert len(parameters['checkboxes']) > 0

    checkboxes = parameters.get('checkboxes', {})
    assert isinstance(checkboxes.get('driversLicence', False), bool)
    assert isinstance(checkboxes.get('requireVisa', False), bool)
    assert isinstance(checkboxes.get('legallyAuthorized', False), bool)
    assert isinstance(checkboxes.get('urgentFill', False), bool)
    assert isinstance(checkboxes.get('commute', False), bool)
    assert isinstance(checkboxes.get('backgroundCheck', False), bool)
    assert 'degreeCompleted' in checkboxes

    assert isinstance(parameters['universityGpa'], (int, float))

    languages = parameters.get('languages', {})
    language_types = {'none', 'conversational', 'professional', 'native or bilingual'}
    for language in languages:
        assert languages[language].lower() in language_types

    industry = parameters.get('industry', {})
    for skill in industry:
        assert isinstance(industry[skill], int)
    assert 'default' in industry

    technology = parameters.get('technology', {})
    for tech in technology:
        assert isinstance(technology[tech], int)
    assert 'default' in technology

    assert len(parameters['personalInfo'])
    for info in parameters['personalInfo']:
        assert parameters['personalInfo'][info] != ''

    assert len(parameters['eeo'])
    for survey_question in parameters['eeo']:
        assert parameters['eeo'][survey_question] != ''

    return parameters


# if __name__ == '__main__':
#     parameters = validate_yaml()
#     browser = init_browser()
#     bot = GlassDoorEasyApply(parameters, browser)
    
#     print("Start")
#     # print(dir(bot))
#     bot.login()
#     time.sleep(3)  # Ensure the page loads
#     bot.search_job()
#     time.sleep(3)  # Ensure the page loads
#     bot.click_easy_apply_filter()
#     time.sleep(3)  # Ensure the page loads
#     bot.select_first_job()
#     time.sleep(3)  # Ensure the page loads
#     bot.easy_apply_job()
#     time.sleep(3)  # Ensure the page loads
#     bot.apply_to_jobs()

#     print("End")



if __name__ == '__main__':
    try:
        parameters = validate_yaml()
        browser = init_browser()
        bot = GlassDoorEasyApply(parameters, browser)
        
        print("🚀 Start")
        bot.login()
        time.sleep(3)  # Ensure the page loads

        bot.apply_to_jobs()  # Single call handles everything
        
        print("✅ End")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        print("🛑 Closing browser...")
        browser.quit()