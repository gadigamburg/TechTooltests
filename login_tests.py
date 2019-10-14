from selenium import webdriver
import os,sys
from ConfigParser import SafeConfigParser
import unittest
import time
import logging
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

###  Global content for all project ######
#path of Chromedriver
dir=os.getcwd()
chrome_driver_path=dir + "\chromedriver.exe"

config_parser=SafeConfigParser()
config_parser.read('config.properties')
device_ip=config_parser.get('unit_parameters','ip')

### Config logging  ####
logging.basicConfig(level=logging.INFO, filename='TestAdminTool.log', filemode='a' ,format='%(asctime)s %(levelname)s - %(message)s')


###########################################
logging.info('############################')
class  LoginTests(unittest.TestCase):
    @classmethod
    def setUp(self):
    # Create a new Chrome session
       self.driver=webdriver.Chrome(chrome_driver_path)
       self.driver.implicitly_wait(30)
       self.driver.maximize_window()
        ###################################
       self.admintool_url=str("http://"+device_ip+":9000")
        # navigate to the application page
       self.driver.get(self.admintool_url)
    # def test_correct_login_admin(self):
    #     ## get username field textbox
    #     logging.info('Start Login as admin user...')
    #     self.username_field=self.driver.find_element_by_id("username-input")
    #     self.username_field.clear()
    #     ## enter username to field
    #     self.admin_user=config_parser.get('username_passwords','general_user_admin')
    #     self.username_field.send_keys(self.admin_user)
    #     ## enter password  text field
    #     self.password_field=self.driver.find_element_by_id("password-input")
    #     self.password_field.clear()
    #     ## enter password to field
    #     self.password_admin_user=config_parser.get('username_passwords','general_password_admin')
    #     self.password_field.send_keys(self.password_admin_user)
    #     ### Pres on 'Log in' ###
    #     self.log_in_btn=self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
    #     self.log_in_btn.submit()
    #     self.dashboard_url = self.admintool_url + "/#/pages/dashboard"
    #     try:
    #         myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
    #         user = "rammshtein"
    #         try:
    #             self.assertTrue(user in self.driver.page_source)
    #             logging.info('Successefully get to Dashboard page as admin user.Test is PASS')
    #         except AssertionError:
    #             self.fail("not log-in as rammshtein")
    #             logging.error('Failed log in as admin user. Test is FAIL')
    #     except TimeoutException:
    #         self.fail("Loading took too much time!")
    #         logging.error('Loading and switch to Dashboard as Admin useer took too much time. Test is FAIL')
    # def test_correct_login_user(self):
    #     logging.info('Start Login as regular user...')
    #     #open new tab
    #     self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    #     self.driver.get(self.admintool_url)
    #     ## get username field textbox
    #     self.username_field=self.driver.find_element_by_id("username-input")
    #     self.username_field.clear()
    #     ## enter username to field
    #     self.user=config_parser.get('username_passwords','general_user')
    #     self.username_field.send_keys(self.user)
    #     ## enter password  text field
    #     self.password_field=self.driver.find_element_by_id("password-input")
    #     self.password_field.clear()
    #     ## enter password to field
    #     self.password_user=config_parser.get('username_passwords','general_password')
    #     self.password_field.send_keys(self.password_user)
    #     ### Pres on 'Log in' ###)
    #     self.log_in_btn=self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
    #     self.log_in_btn.submit()
    #     self.dashboard_url = self.admintool_url + "/#/pages/dashboard"
    #     try:
    #         myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
    #         user = "user"
    #         try:
    #             self.assertTrue(user in self.driver.page_source)
    #             logging.info('Successefully get to Dashboard page as regular user. Test is PASS')
    #         except AssertionError:
    #             self.fail("not log-in as user")
    #             logging.error('Failed log in as regular user. Test is FAIL')
    #     except TimeoutException:
    #         self.fail("Loading took too much time!")
    #         logging.error('Loading and switch to Dashboard as Regular useer took too much time. Test is FAIL')
    # def test_correct_login_lely(self):
    #     logging.info('Start Login as LeLy user...')
    #     #open new tab
    #     self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    #     self.driver.get(self.admintool_url)
    #     ## get username field textbox
    #     self.username_field=self.driver.find_element_by_id("username-input")
    #     self.username_field.clear()
    #     ## enter username to field
    #     self.user=config_parser.get('username_passwords','general_lely_user')
    #     self.username_field.send_keys(self.user)
    #     ## enter password  text field
    #     self.password_field=self.driver.find_element_by_id("password-input")
    #     self.password_field.clear()
    #     ## enter password to field
    #     self.password_user=config_parser.get('username_passwords','general_lely_password')
    #     self.password_field.send_keys(self.password_user)
    #     ### Pres on 'Log in' ###
    #     #self.log_in_btn=self.driver.find_element_by_class_name("btn-success btn-full-width")
    #     self.log_in_btn=self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
    #     self.log_in_btn.submit()
    #     self.dashboard_url = self.admintool_url + "/#/pages/dashboard"
    #     try:
    #         myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
    #         user = "user"
    #         try:
    #             self.assertTrue(user in self.driver.page_source)
    #             logging.info('Successefully get to Dashboard page as LeLy user.Test is PASS')
    #         except AssertionError:
    #             self.fail("not log-in as user")
    #             logging.error('Failed log in as LeLy user. Test is FAIL')
    #     except TimeoutException:
    #         self.fail("Loading took too much time!")
    #         logging.error('Loading and switch to Dashboard as LeLy user took too much time. Test is FAIL')
    # def test_wrong_login_user(self):
    #     logging.info('Start Login as wrong/not exist user...')
    #     # open new tab
    #     self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    #     self.driver.get(self.admintool_url)
    #     ## get username field textbox
    #     self.username_field = self.driver.find_element_by_id("username-input")
    #     self.username_field.clear()
    #     ## enter username to field
    #     self.user = config_parser.get('username_passwords', 'fake_user')
    #     #self.username_field.send_keys(self.user)
    #     self.username_field.send_keys("test")
    #     ## enter password  text field
    #     self.password_field = self.driver.find_element_by_id("password-input")
    #     self.password_field.clear()
    #     ## enter password to field
    #     self.password_user = config_parser.get('username_passwords', 'fake_password')
    #     self.password_field.send_keys(self.password_user)
    #     ### Pres on 'Log in' ###
    #     self.log_in_btn = self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
    #     self.log_in_btn.submit()
    #     try:
    #         myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'alert-message')))
    #         # print "Get to Dashboard"
    #         self.driver.implicitly_wait(5)
    #         alert_content = "Error while authorizing user"
    #         try:
    #             self.assertTrue(alert_content in self.driver.page_source)
    #             logging.info('Recognize authorized alert pop-up message, test is PASS')
    #         except AssertionError:
    #             self.fail("not alert message appear")
    #             logging.error('No pop-up alert message appear, test is FAIL')
    #     except TimeoutException:
    #          self.fail("Get an alert message too much time!")
    #          logging.error('Get an alert message of authorization took too much time, Test is FAIL')
    # def test_logout(self):
    #     logging.info('Start test of log out from admin tool...')
    #     ## get username field textbox
    #     self.username_field = self.driver.find_element_by_id("username-input")
    #     self.username_field.clear()
    #     ## enter username to field
    #     self.admin_user = config_parser.get('username_passwords', 'general_user_admin')
    #     self.username_field.send_keys(self.admin_user)
    #     ## enter password  text field
    #     self.password_field = self.driver.find_element_by_id("password-input")
    #     self.password_field.clear()
    #     ## enter password to field
    #     self.password_admin_user = config_parser.get('username_passwords', 'general_password_admin')
    #     self.password_field.send_keys(self.password_admin_user)
    #     ### Pres on 'Log in' ###
    #     self.log_in_btn = self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
    #     self.log_in_btn.submit()
    #     self.dashboard_url = self.admintool_url + "/#/pages/dashboard"
    #     try:
    #         myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
    #         # print "Get to Dashboard"
    #         user = "rammshtein"
    #         try:
    #             self.assertTrue(user in self.driver.page_source)
    #             logging.info('Successfully get to Dashboard as Admin user, test is PASS')
    #         except AssertionError:
    #             self.fail("not log-in as rammshtein")
    #             logging.error("Failed get to dashboard as Admin user, test is FAIL")
    #     except TimeoutException:
    #         self.fail("Loading took too much time!")
    #         logging.error("Loading to Dashboard took too much time, test is FAIL")
    #     ## Finish login process and located at Dashboard page
    #     ## Start Log out process
    #     try:
    #        logout_href="#/auth/logout"
    #        logout_btn=self.driver.find_element_by_xpath('//a[@href="'+logout_href+'"]')
    #        logging.info("Log-out button is found ")
    #     except NoSuchElementException:
    #         self.fail("Didn't found Log out button")
    #         logging.error("Failed find log-out button , test is FAIL")
    #     logout_btn.click()
    #     try:
    #         myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'username-input')))
    #         logging.info("Successfully return to login page, test is PASS")
    #     except NoSuchElementException:
    #         self.fail("Didn't return to Login page")
    #         logging.error("Don't return to Login page , test is FAIL ")
    def test_user_password_is_required(self):
        logging.info('Start test of appearence message that password is required...')
        ## get username field textbox
        self.username_field = self.driver.find_element_by_id("username-input")
        self.username_field.clear()
        ## enter username to field
        self.admin_user = config_parser.get('username_passwords', 'general_user_admin')
        self.username_field.send_keys(self.admin_user)
        ## Clear username text box again, for appearence if alert messsage
        self.username_field.clear()
        ## focus on password field box
        self.password_field = self.driver.find_element_by_id("password-input")
        self.password_field.clear()
        ## Now should appear a message of 'username is required'
        try:
            myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'error-message')))
            logging.info(myElem.text)
                # try:
                #     self.assertTrue(user in self.driver.page_source)
                #     logging.info('Successfully get to Dashboard as Admin user, test is PASS')
                # except AssertionError:
                #     self.fail("not log-in as rammshtein")
                #     logging.error("Failed get to dashboard as Admin user, test is FAIL")
        except TimeoutException:
            self.fail("Loading took too much time!")
            logging.error("Loading to Dashboard took too much time, test is FAIL")

        # self.password_field = self.driver.find_element_by_id("password-input")
        # self.password_field.clear()
        # ## enter password to field
        # self.password_admin_user = config_parser.get('username_passwords', 'general_password_admin')
        # self.password_field.send_keys(self.password_admin_user)
        # try:
        # myElem = WebDriverWait(self.driver, 10).until(
        # EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
        #         # print "Get to Dashboard"
        #         user = "rammshtein"
        #         try:
        #             self.assertTrue(user in self.driver.page_source)
        #             logging.info('Successfully get to Dashboard as Admin user, test is PASS')
        #         except AssertionError:
        #             self.fail("not log-in as rammshtein")
        #             logging.error("Failed get to dashboard as Admin user, test is FAIL")
        #     except TimeoutException:
        #         self.fail("Loading took too much time!")
        #         logging.error("Loading to Dashboard took too much time, test is FAIL")

    @classmethod
    def tearDown(self):
        logging.info("###############################")
        # close the browser window
        self.driver.quit()
#####################################


