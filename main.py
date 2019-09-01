from selenium import webdriver
import os,sys
from ConfigParser import SafeConfigParser

###  Global content for all project ######
#path of Chromedriver
dir=os.getcwd()
chrome_driver_path=dir + "\chromedriver.exe"
ip=str(sys.argv[1])
device_ip=ip
config_parser=SafeConfigParser()
config_parser.read('config.properties')
###########################################


# Create a new Chrome session
driver=webdriver.Chrome(chrome_driver_path)
driver.implicitly_wait(30)
driver.maximize_window()
###################################


###  Star Log In Test Case 1
### with correct details
admintool_url=str("http://"+device_ip+":9000")
# navigate to the application page
driver.get(admintool_url)


## get username field textbox
username_field=driver.find_element_by_id("input-username")
username_field.clear()

## enter username to field
admin_user=config_parser.get('username_passwords','general_user_admin')
username_field.send_keys(admin_user)


## enter password  text field
password_field=driver.find_element_by_id("input-password")
password_field.clear()

## enter password to field
password_admin_user=config_parser.get('username_passwords','general_password_admin')
password_field.send_keys(password_admin_user)
driver.implicitly_wait(5)
### Pres on 'Log in' ###
#log_in_btn=driver.find_element_by_class_name("btn-success btn-full-width")
log_in_btn=driver.find_element_by_xpath("//*[contains(text(),'Log In')]")
log_in_btn.submit()

#####################################



#driver.quit()




