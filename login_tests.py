from selenium import webdriver
import os,sys
from ConfigParser import SafeConfigParser
import unittest
import time
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

###########################################

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
    #     self.username_field=self.driver.find_element_by_id("input-username")
    #     self.username_field.clear()
    #     ## enter username to field
    #     self.admin_user=config_parser.get('username_passwords','general_user_admin')
    #     self.username_field.send_keys(self.admin_user)
    #
    #     ## enter password  text field
    #     self.password_field=self.driver.find_element_by_id("input-password")
    #     self.password_field.clear()
    #
    #     ## enter password to field
    #     self.password_admin_user=config_parser.get('username_passwords','general_password_admin')
    #     self.password_field.send_keys(self.password_admin_user)
    #     ### Pres on 'Log in' ###
    #     self.log_in_btn=self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
    #     self.log_in_btn.submit()
    #     self.dashboard_url = self.admintool_url + "/#/pages/dashboard"
    #     try:
    #         myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
    #         #print "Get to Dashboard"
    #         user = "rammshtein"
    #         try:
    #             self.assertTrue(user in self.driver.page_source)
    #             #print "syccessfully log-in as rammshtein"
    #         except AssertionError:
    #             self.fail("not log-in as rammshtein")
    #     except TimeoutException:
    #         self.fail("Loading took too much time!")


    # def test_correct_login_user(self):
    #     #open new tab
    #     self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
    #     self.driver.get(self.admintool_url)
    #     ## get username field textbox
    #     self.username_field=self.driver.find_element_by_id("input-username")
    #     self.username_field.clear()
    #     ## enter username to field
    #     self.user=config_parser.get('username_passwords','general_user')
    #     self.username_field.send_keys(self.user)
    #
    #     ## enter password  text field
    #     self.password_field=self.driver.find_element_by_id("input-password")
    #     self.password_field.clear()
    #
    #     ## enter password to field
    #     self.password_user=config_parser.get('username_passwords','general_password')
    #     self.password_field.send_keys(self.password_user)
    #     ### Pres on 'Log in' ###
    #     #self.log_in_btn=self.driver.find_element_by_class_name("btn-success btn-full-width")
    #     self.log_in_btn=self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
    #     self.log_in_btn.submit()
    #     self.dashboard_url = self.admintool_url + "/#/pages/dashboard"
    #     try:
    #         myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
    #         #print "Get to Dashboard"
    #         user = "user"
    #         try:
    #             self.assertTrue(user in self.driver.page_source)
    #             #print "syccessfully log-in as user"
    #         except AssertionError:
    #             self.fail("not log-in as user")
    #     except TimeoutException:
    #         self.fail("Loading took too much time!")

    def test_wrong_login_user(self):
        # open new tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
        self.driver.get(self.admintool_url)
        ## get username field textbox
        self.username_field = self.driver.find_element_by_id("input-username")
        self.username_field.clear()
        ## enter username to field
        self.user = config_parser.get('username_passwords', 'fake_user')
        self.username_field.send_keys(self.user)

        ## enter password  text field
        self.password_field = self.driver.find_element_by_id("input-password")
        self.password_field.clear()

        ## enter password to field
        self.password_user = config_parser.get('username_passwords', 'general_password')
        self.password_field.send_keys(self.password_user)
        ### Pres on 'Log in' ###
        self.log_in_btn = self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
        self.log_in_btn.submit()
        try:
            myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'alert-message')))
            # print "Get to Dashboard"
            self.driver.implicitly_wait(10)
            alert_content = "Error while authorizing user"
            try:
                self.assertTrue(alert_content in self.driver.page_source)
                #print "syccessfully log-in as user"
            except AssertionError:
                self.fail("not alert message appear")
        except TimeoutException:
             self.fail("Get an alert message too much time!")

    def test_logout(self):
        ## get username field textbox
        self.username_field = self.driver.find_element_by_id("input-username")
        self.username_field.clear()
        ## enter username to field
        self.admin_user = config_parser.get('username_passwords', 'general_user_admin')
        self.username_field.send_keys(self.admin_user)

        ## enter password  text field
        self.password_field = self.driver.find_element_by_id("input-password")
        self.password_field.clear()

        ## enter password to field
        self.password_admin_user = config_parser.get('username_passwords', 'general_password_admin')
        self.password_field.send_keys(self.password_admin_user)
        ### Pres on 'Log in' ###
        self.log_in_btn = self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
        self.log_in_btn.submit()
        self.dashboard_url = self.admintool_url + "/#/pages/dashboard"
        try:
            myElem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
            # print "Get to Dashboard"
            user = "rammshtein"
            try:
                self.assertTrue(user in self.driver.page_source)
                # print "syccessfully log-in as rammshtein"
            except AssertionError:
                self.fail("not log-in as rammshtein")
        except TimeoutException:
            self.fail("Loading took too much time!")
        ## Finish login process and located at Dashboard page
        ## Start Log out process
        try:
           logout_href="#/auth/logout"
           logout_btn=self.driver.find_element_by_xpath('//a[@href="'+logout_href+'"]')
        except NoSuchElementException:
            self.fail("Didn't found Log out button")
        logout_btn.click()
        try:
            myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'input-username')))
        except NoSuchElementException:
            self.fail("Didn't return to Login page")
    @classmethod
    def tearDown(self):
        # close the browser window
        self.driver.quit()
#####################################



# if __name__=='__main__':
#     unittest.main(verbosity=2)

