# AdminTool tests

The focal point of this project is contain automation tests for AdminTool on Collector/Standalone Server.

It wroten on pure Python 2.7 by using Selenium that work with Webdriver and tests are writen using integration framework of unittest

The HTML report is generated by HTMLTestRunner.


The list of tests :

Login tests :

1) Test of login with admin user
2)Test of Login with regular user
3)Test of login with LeLy user
4)Test of login with fake user
5)Test of appeareance alert message of "password required"
6)Test of appeareance alert message of "username is required"
7)Test of appeareance message that password too short/long
8)Test of logout button functionality from Dashboard

Dashboard tests :

1) Check if tool show correct Serial number to DUT device




