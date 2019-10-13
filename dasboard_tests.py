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

## Imort Remote connection (SSH) modules
from SSHConnection import ConnectionToDUT

###  Global content for all project ######
#path of Chromedriver
dir=os.getcwd()
chrome_driver_path=dir + "\chromedriver.exe"

config_parser=SafeConfigParser()
config_parser.read('config.properties')
device_ip=config_parser.get('unit_parameters','ip')

### Config logging  ####
logging.basicConfig(level=logging.INFO, filename='TestAdminTool.log', filemode='w' ,format='%(asctime)s %(levelname)s - %(message)s')

###########################################

class  DashboardTests(unittest.TestCase):
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

    def test_correct_serial_number(self):
        T=ConnectionToDUT()
        out, err, sh, client = T.RunRemoteCommands("cat /usr/local/board/medical_file.txt | grep assembly.cat | awk -F'=' '{print $2}' | awk -F',' '{print $1}'")
        T.CloseSSHConnection(sh, client)
        T = ConnectionToDUT()
        out2, err2, sh2, client2 = T.RunRemoteCommands("cat /usr/local/board/medical_file.txt | grep assembly.sn | awk -F'=' '{print $2}' | awk -F',' '{print $1}'")
        T.CloseSSHConnection(sh2, client2)

        ## get username field textbox
        logging.info('start check serial number')
        self.username_field = self.driver.find_element_by_id("username-input")
        self.username_field.clear()
        ## enter username to field
        self.admin_user = config_parser.get('username_passwords', 'general_user_admin')
        self.username_field.send_keys(self.admin_user)

        ## enter password  text field
        self.password_field = self.driver.find_element_by_id("password-input")
        self.password_field.clear()

        ## enter password to field
        self.password_admin_user = config_parser.get('username_passwords', 'general_password_admin')
        self.password_field.send_keys(self.password_admin_user)
        ### Pres on 'Log in' ###
        self.log_in_btn = self.driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
        self.log_in_btn.submit()
        self.dashboard_url = self.admintool_url + "/#/pages/dashboard"
        logging.info('check if we located at dashboard')
        logging.info(self.dashboard_url)
        try:
            myElem = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
            user = "rammshtein"
            try:
                self.assertTrue(user in self.driver.page_source)
                logging.info('check if log-in as rammshtein')
                time.sleep(2)
                #print "syccessfully log-in as rammshtein"
            except AssertionError:
                print "not log-in as rammshtein"
        except TimeoutException:
            print "Loading took too much time!"
        self.general_sn = self.driver.find_element_by_xpath("//div[@class='title' and text()='Serial Number']")
        self.sn=self.general_sn.find_element_by_xpath("//div[@class='status']").text
        logging.info("The Serial number that AdminTool found is : {s}".format(s=self.sn))

        # out, err, sh, client = ConnectionToDUT.RunRemoteCommands('ls')
        # logging.info(out)
        # time.sleep(10)
        # ConnectionToDUT.CloseSSHConnection(sh, client)


        #self.real_serial_number= config_parser.get('unit_parameters', 'serial_number')
        self.real_serial_number=out.strip() + out2.strip() + '1'
        logging.info("The real Serial number on device is : {s}".format(s=self.real_serial_number))
        try:
            self.assertEqual(self.sn,self.real_serial_number)
            logging.info("The Serial Number is as expected !! ---  PASS")
        except Exception as e:
            logging.error("The found Serial number is not as expected ---  FAIL ")
            logging.error(e)
            raise e



    @classmethod
    def tearDown(self):
        # close the browser window
        self.driver.quit()

    def tearDown(self):
        # close the browser window
        self.driver.quit()
#####################################

