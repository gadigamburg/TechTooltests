from selenium import webdriver
import os,sys
from ConfigParser import SafeConfigParser
import unittest
import time


###  Global content for all project ######
#path of Chromedriver
dir=os.getcwd()
chrome_driver_path=dir + "\chromedriver.exe"

config_parser=SafeConfigParser()
config_parser.read('config.properties')
device_ip=config_parser.get('unit_parameters','ip')

###########################################

class  LoginTests(unittest.TestCase):
    def setUp(self):
    # Create a new Chrome session
       self.driver=webdriver.Chrome(chrome_driver_path)
       self.driver.implicitly_wait(30)
       self.driver.maximize_window()
        ###################################
       self.admintool_url=str("http://"+device_ip+":9000")
        # navigate to the application page
       self.driver.get(self.admintool_url)

    def test_correct_login(self):
        ## get username field textbox
        self.username_field=self.driver.find_element_by_id("input-username")
        self.username_field.clear()
        ## enter username to field
        self.admin_user=config_parser.get('username_passwords','general_user_admin')
        self.username_field.send_keys(self.admin_user)

        ## enter password  text field
        self.password_field=self.driver.find_element_by_id("input-password")
        self.password_field.clear()

        ## enter password to field
        self.password_admin_user=config_parser.get('username_passwords','general_password_admin')
        self.password_field.send_keys(self.password_admin_user)
        ### Pres on 'Log in' ###
        #self.log_in_btn=self.driver.find_element_by_class_name("btn-success btn-full-width")
        self.log_in_btn=self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
        self.log_in_btn.submit()
        time.sleep(10)
    def tearDown(self):
        # close the browser window
        self.driver.quit()
#####################################



#driver.quit()


if __name__=='__main__':
    unittest.main(verbosity=2)

