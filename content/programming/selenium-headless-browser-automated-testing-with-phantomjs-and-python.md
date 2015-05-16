Title: Selenium headless browser automated testing with PhantomJS and Python
Date: 2013-09-17 21:04
Slug: content/selenium-headless-browser-automated-testing-with-phantomjs-and-python

[TOC]

### Overview

selenium: an automation framework for interactions with websites (like a programmatic browser) <http://docs.seleniumhq.org/docs/02_selenium_ide.jsp#introduction>

phantomjs: headless browser <http://phantomjs.org>

### Install
`sudo pip install selenium`

wget <https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2>

`tar -xjvf phantomjs-1.9.8-linux-x86_64.tar.bz2`

### Run
`phantomjs-1.9.8-linux-x86_64/bin/phantomjs --webdriver=9134`

> ghostdriver included and running on port 9134

### Example python script
**mini script to just show usage**

    from selenium import webdriver
    
    driver = webdriver.PhantomJS(executable_path='/opt/phantomjs-1.9.8-linux-x86_64/bin/phantomjs', port=9134)
    driver.get("http://127.0.0.1")
    print driver.current_url
    driver.quit
    print "done"
    

`phantomjs-1.9.8-linux-x86_64/bin/phantomjs --webdriver=9134 --ignore-ssl-errors=true`

### Advanced Python example

> more complete example with python unittest framework (used the Firefox Selenium IDE plugin -> Export)

> logs in, asserts there is an Admin tab which when clicked shows Group Info

    :::python
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import Select
    from selenium.common.exceptions import NoSuchElementException
    import unittest, time, re
    
    class SeleniumAdminLogin( unittest.TestCase ):
    
        def setUp( self ):
            self.driver = webdriver.PhantomJS( '/opt/phantomjs-1.9.2-linux-x86_64/bin/phantomjs', port=9134 )
            self.driver.implicitly_wait(30)
            self.base_url = "https://myexample.org"
            self.verificationErrors = []
            self.accept_next_alert = True
            
        def test_selenium_admin_login( self ):
            driver = self.driver
            driver.get( self.base_url + "/" )
            driver.find_element_by_id( "email" ).clear()
            driver.find_element_by_id( "email" ).send_keys( "admin@example.org" )
            driver.find_element_by_id( "password" ).clear()
            driver.find_element_by_id( "password" ).send_keys( "mypassword" )
            driver.find_element_by_id( "signin" ).click()
            self.assertEqual("https://myexample.org/home", driver.current_url)
            self.assertTrue(self.is_element_present(By.LINK_TEXT, "Launch the web app"))
            self.assertTrue(self.is_element_present(By.CSS_SELECTOR, "a.admin > span"))
            driver.find_element_by_css_selector("a.admin > span").click()
            self.assertEqual("Group Info", driver.find_element_by_css_selector("h1").text)
            
        def is_element_present(self, how, what):
            try: 
                self.driver.find_element(by=how, value=what)
            except NoSuchElementException, e: return False
                return True
            
        def is_alert_present(self):
            try: 
                self.driver.switch_to_alert()
            except NoAlertPresentException, e: return False
            return True
        
        def close_alert_and_get_its_text(self):
            try:
                alert = self.driver.switch_to_alert()
                alert_text = alert.text
                if self.accept_next_alert:
                    alert.accept()
                else:
                    alert.dismiss()
                return alert_text
                finally: 
                    self.accept_next_alert = True
            
        def tearDown(self):
            self.driver.quit()
            self.assertEqual([], self.verificationErrors)
            
    if __name__ == "__main__":
        unittest.main()
    
   

### References  
- <http://phantomjs.org/release-1.8.html>
- <https://github.com/ariya/phantomjs/wiki/API-Reference>
- <http://www.realpython.com/blog/python/headless-selenium-testing-with-python-and-phantomjs>
