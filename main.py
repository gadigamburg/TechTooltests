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


import dasboard_tests

from login_tests import LoginTests
from dasboard_tests import DashboardTests

###  Global content for all project ######
#path of Chromedriver
dir=os.getcwd()
chrome_driver_path=dir + "\chromedriver.exe"

config_parser=SafeConfigParser()
config_parser.read('config.properties')
device_ip=config_parser.get('unit_parameters','ip')

###########################################



loginTests=unittest.TestLoader().loadTestsFromTestCase(LoginTests)
dashboardTests=unittest.TestLoader().loadTestsFromTestCase(DashboardTests)

#driver.quit()
#smoke_test=unittest.TestSuite([loginTests,dashboardTests])
smoke_test=unittest.TestSuite([loginTests])

unittest.TextTestRunner(verbosity=2).run(smoke_test)

# if __name__=='__main__':
#     unittest.main(verbosity=2)

