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
logging.basicConfig(level=logging.INFO, filename='TestAdminTool.log', filemode='a' ,format='%(asctime)s %(levelname)s - %(message)s')

###########################################

class  DashboardTests(unittest.TestCase):
    @classmethod
#   def setUp(self):
    def setUpClass(self):
    # Create a new Chrome session
       self.driver=webdriver.Chrome(chrome_driver_path)
       self.driver.implicitly_wait(30)
       self.driver.maximize_window()
        ###################################
       self.admintool_url=str("http://"+device_ip+":9000")
        # navigate to the application page
       self.driver.get(self.admintool_url)
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


    def test_A_serial_number(self):
        T=ConnectionToDUT()
        out, err, sh, client = T.RunRemoteCommands("cat /usr/local/board/medical_file.txt | grep assembly.cat | awk -F'=' '{print $2}' | awk -F',' '{print $1}'")
        T.CloseSSHConnection(sh, client)
        T = ConnectionToDUT()
        out2, err2, sh2, client2 = T.RunRemoteCommands("cat /usr/local/board/medical_file.txt | grep assembly.sn | awk -F'=' '{print $2}' | awk -F',' '{print $1}'")
        T.CloseSSHConnection(sh2, client2)
        self.dashboard_url = self.admintool_url + "/#/pages/dashboard"
        logging.info('check if we located at dashboard')
        logging.info(self.dashboard_url)
        try:
            myElem = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ng-star-inserted')))
            user = "rammshtein"
            try:
                self.assertTrue(user in self.driver.page_source)
                logging.info('check if log-in as rammshtein')
                time.sleep(2)
            except Exception as e:
                logging.error("The log-in as rammshtein is ---  FAIL ")
                logging.error(e)
                raise e
        except Exception as e:
            logging.error("Loading took too much time ---  FAIL ")
            logging.error(e)
            raise e
        logging.info('start check serial number')
        self.sn = self.driver.find_element_by_xpath("//input[@id='serialNumber']")
        self.sn_dashboard=self.sn.get_attribute('value').strip()
        logging.info("The Serial number that AdminTool found is : {s}".format(s=self.sn.get_attribute('value')))
        self.real_serial_number=out.strip() + out2.strip()
        logging.info("The real Serial number on device is : {s}".format(s=self.real_serial_number))
        try:
            self.assertEqual(self.sn_dashboard,self.real_serial_number)
            logging.info("The Serial Number is as expected !! ---  PASS")
        except Exception as e:
            logging.error("The found Serial number is not as expected ---  FAIL ")
            logging.error(e)
            raise e

    def test_B_hostname(self):
        T = ConnectionToDUT()
        out, err, sh, client = T.RunRemoteCommands("echo $HOSTNAME")
        T.CloseSSHConnection(sh, client)

        ## get username field textbox
        logging.info('start check hostname number')
        self.host=self.driver.find_element_by_xpath("//input[@id='hostName']")
        self.host_dashboard=self.host.get_attribute('value').strip()
        logging.info("The value of Hostname that appear on Dashboard is : {s}".format(s=self.host_dashboard))

        #self.real_hostname = out.strip()
        self.real_hostname = out.strip()
        logging.info("The real Hostname on device is : {s}".format(s=self.real_hostname))
        try:
            self.assertEqual(self.host_dashboard, self.real_hostname)
            logging.info("The Hostname is as expected !! ---  PASS")
        #except Exception as e:
        except AssertionError as e:
            logging.error("The found Hostname is not as expected ---  FAIL ")
            logging.error(e)
            raise e

    def test_C_MAC(self):
        T = ConnectionToDUT()
        self.dev_type = config_parser.get('unit_parameters', 'device_type')
        if self.dev_type.upper() == "SOM":
            out, err, sh, client = T.RunRemoteCommands("ifconfig | grep 'HWaddr' | awk -F'HWaddr ' '{print $2}'")
        if self.dev_type.upper() == "PC":
            out, err, sh, client = T.RunRemoteCommands("ifconfig | grep ether | awk -F'ether ' '{print $2}' | awk -F' ' '{print $1}'")
        if self.dev_type.upper() == "ANT":
            out, err, sh, client = T.RunRemoteCommands("ifconfig | grep 'HWaddr' | awk -F'HWaddr ' '{print $2}'")
        T.CloseSSHConnection(sh, client)

        logging.info('start check MAC address value')
        self.mac=self.driver.find_element_by_xpath("//input[@id='macAddress']")
        self.mac_dashboard=self.mac.get_attribute('value').strip()
        logging.info("The value of MAC address that appear on Dashboard is : {s}".format(s=self.mac_dashboard))

        #self.real_hostname = out.strip()
        self.real_mac = out.strip()
        logging.info("The real MAC address on device is : {s}".format(s=self.real_mac))
        try:
            self.assertEqual(self.mac_dashboard, self.real_mac)
            logging.info("The MAC address is as expected !! ---  PASS")
        #except Exception as e:
        except AssertionError as e:
            logging.error("The found MAC address is not as expected ---  FAIL ")
            logging.error(e)
            raise e

    def test_D_farmID(self):
        T = ConnectionToDUT()
        self.dev_type = config_parser.get('unit_parameters', 'device_type')
#        if self.dev_type.upper() == "SOM":
        out, err, sh, client = T.RunRemoteCommands("mysql -uroot -pscrscr scr -e 'select pvalue from scrproperties where id=16;' | tail -n 1")
        T.CloseSSHConnection(sh, client)

        logging.info('start check farmID value')
        self.farmid=self.driver.find_element_by_xpath("//input[@id='farmId']")
        self.farmid_dashboard=self.farmid.get_attribute('value').strip()
        logging.info("The value of farmid that appear on Dashboard is : {s}".format(s=self.farmid_dashboard))

        #self.real_hostname = out.strip()
        self.real_farmid = out.strip()
        if self.farmid_dashboard == "No Farm ID" :
            self.farmid_dashboard="NULL"
            logging.info("The value 'No Farm ID == NULL'")
        logging.info("The real farmid on device is : {s}".format(s=self.real_farmid))
        try:
            self.assertEqual(self.farmid_dashboard, self.real_farmid)
            logging.info("The farmId is as expected !! ---  PASS")
        #except Exception as e:
        except AssertionError as e:
            logging.error("The found farmId is not as expected ---  FAIL ")
            logging.error(e)
            raise e
    def test_E_imageVersion(self):
        T = ConnectionToDUT()
        self.dev_type = config_parser.get('unit_parameters', 'device_type')
        #        if self.dev_type.upper() == "SOM":
        out, err, sh, client = T.RunRemoteCommands("cat /root/image_version.txt")
        T.CloseSSHConnection(sh, client)

        logging.info('start check image version value')
        self.imageVer = self.driver.find_element_by_xpath("//input[@id='imageVersion']")
        self.imageVer_dashboard = self.imageVer.get_attribute('value').strip()
        logging.info("The image version value that appear on Dashboard is : {s}".format(s=self.imageVer_dashboard))

        # self.real_hostname = out.strip()
        self.real_imageVer = out.strip()
        logging.info("The real image version on device is : {s}".format(s=self.real_imageVer))
        try:
            self.assertEqual(self.imageVer_dashboard, self.real_imageVer)
            logging.info("The real image version is as expected !! ---  PASS")
        # except Exception as e:
        except AssertionError as e:
            logging.error("The found real image version is not as expected ---  FAIL ")
            logging.error(e)
            raise e
    def test_F_FSVersion(self):
        self.dev_type = config_parser.get('unit_parameters', 'device_type')
        if self.dev_type=="ANT":
            raise unittest.SkipTest(logging.warning("No FS version on Antenna, skip test of checking FS version"))
        T = ConnectionToDUT()
#        self.dev_type.upper() == "SOM":
        out, err, sh, client = T.RunRemoteCommands("cat /mnt/usb/fsversion/version")
        T.CloseSSHConnection(sh, client)
        logging.info('start check FS version value')
        self.FSVer = self.driver.find_element_by_xpath("//input[@id='farmServerVersion']")
        self.FSVer_dashboard = self.FSVer.get_attribute('value').strip()
        logging.info("The Farm Server version value that appear on Dashboard is : {s}".format(s=self.FSVer_dashboard))
        self.real_FSVer = out.strip()
        logging.info("The real FS  version on device is : {s}".format(s=self.real_FSVer))
        try:
            self.assertEqual(self.FSVer_dashboard, self.real_FSVer)
            logging.info("The real FS version is as expected !! ---  PASS")
        # except Exception as e:
        except AssertionError as e:
            logging.error("The real FS version is not as expected ---  FAIL ")
            logging.error(e)
            raise e

    def test_G_EmbVersion(self):
        self.dev_type = config_parser.get('unit_parameters', 'device_type')
        if self.dev_type == "PC":
            raise unittest.SkipTest(logging.warning("No Embedded version on PC, skip test of checking Embedded version"))
        T = ConnectionToDUT()
        #        self.dev_type.upper() == "SOM":
        out, err, sh, client = T.RunRemoteCommands("cat /usr/local/pref/versions/package_versions.txt  | grep 'Package' | awk -F'Package ' '{print $2}'")
        T.CloseSSHConnection(sh, client)
        logging.info('start check Embedded version value')
        self.EmbVer = self.driver.find_element_by_xpath("//input[@id='embeddedSWVersion']")
        self.EmbVer_dashboard = self.EmbVer.get_attribute('value').strip()
        logging.info("The Embedded version value that appear on Dashboard is : {s}".format(s=self.EmbVer_dashboard))
        self.real_EmbVer = out.strip()
        logging.info("The real Emb version on device is : {s}".format(s=self.real_EmbVer))
        try:
            self.assertEqual(self.EmbVer_dashboard, self.real_EmbVer)
            logging.info("The real Embedded version is as expected !! ---  PASS")
        # except Exception as e:
        except AssertionError as e:
            logging.error("The real Embedded version is not as expected ---  FAIL ")
            logging.error(e)
            raise e
    def test_H_NetworkConf(self):
        self.dev_type = config_parser.get('unit_parameters', 'device_type')
        T = ConnectionToDUT()
        out, err, sh, client = T.RunRemoteCommands("readlink -- '/etc/dhcpcd.conf'")
        T.CloseSSHConnection(sh, client)
        logging.info('start check network configuraion type')
        self.netMode = self.driver.find_element_by_xpath("//input[@id='networkMode']")
        self.netMode_dashboard = self.netMode.get_attribute('value').strip()
        logging.info("The Network mode configuraton that appear on Dashboard is : {s}".format(s=self.netMode_dashboard))
        self.netMode_real=out.strip()
        if ( self.netMode_real == "/etc/dhcpcd.conf.dhcp"):
            self.netMode_real="Dynamic IP (DHCP)"
        else:
            self.netMode_real = "Static Ip"
        logging.info("The real Network mode configuration on device is : {s}".format(s=self.netMode_real))
        try:
            self.assertEqual(self.netMode_dashboard, self.netMode_real)
            logging.info("The real Network Mode is as expected !! ---  PASS")
        # except Exception as e:
        except AssertionError as e:
            logging.error("The real Network Mode is not as expected ---  FAIL ")
            logging.error(e)
            raise e
    def test_K_DateTime(self):
        T = ConnectionToDUT()
        #"'%d/%m/%Y %H:%M'"
        out, err, sh, client = T.RunRemoteCommands("date +'%d/%m/%Y %H:%M'")
        T.CloseSSHConnection(sh, client)
        logging.info('start check device time on adminTool at UTC format')
        self.datetime = self.driver.find_element_by_xpath("//span[@class='font-weight-bolder ml-1 ng-star-inserted']")
        logging.info("The date time value that AdminTool show is : {s}".format(s=self.datetime.text))
        curr_sys_datetime=out.rstrip()+" UTC"
        logging.info("The value of date time we get from system is : {s}".format(s=curr_sys_datetime))
        try:
           self.assertEqual(self.datetime.text, curr_sys_datetime)
           logging.info("The value of AdminTool is equal to system date time value")
        except AssertionError as e:
            logging.error("The date time value that AdminTool show is not equal to real system clock !")
            logging.error(e)
            raise e

    def test_L_ShowDeviceType(self):
        T = ConnectionToDUT()
        # "'%d/%m/%Y %H:%M'"
        out, err, sh, client = T.RunRemoteCommands("date +'%d/%m/%Y %H:%M'")
        T.CloseSSHConnection(sh, client)
        logging.info('start check device time on adminTool at UTC format')
        self.datetime = self.driver.find_element_by_xpath("//span[@class='font-weight-bolder ml-1 ng-star-inserted']")
        logging.info("The date time value that AdminTool show is : {s}".format(s=self.datetime.text))
        curr_sys_datetime = out.rstrip() + " UTC"
        logging.info("The value of date time we get from system is : {s}".format(s=curr_sys_datetime))
        try:
            self.assertEqual(self.datetime.text, curr_sys_datetime)
            logging.info("The value of AdminTool is equal to system date time value")
        except AssertionError as e:
            logging.error("The date time value that AdminTool show is not equal to real system clock !")
            logging.error(e)
            raise e

    @classmethod
#    def tearDown(self):
    def tearDownClass(self):
        # close the browser window
        self.driver.quit()
#####################################

