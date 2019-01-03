Title: Selenium headless browser automated testing with PhantomJS and Python
Date: 2013-09-17 21:04
Tags: selenium, python, programming, test, phantomjs, CI, tech debt

[TOC]

### Why Automated Testing
Automated Testing is critical to maintaining quality while increasing velocity *(aka avoiding being crushed to death by technical debt).*
Web sites are inherently complex to test:

- requires a client and server,
- combination of UI and Logic,
- lots of paths,
- etc

A challenge facing the HipChat team is how to maintain quality while supporting both SaaS and BTF versions, expanding the team, increasing the functionality, and experiment with architecture (or even just normal bug fixing refactoring).

### Choosing Selenium
Continued innovation by the Selenium project has created a stable and usable programmatic interface such that clicking on different components in a web page can be automated.

Selenium tests can be generated manually by a Firefox plugin <https://docs.seleniumhq.org/projects/ide/> and then saved to a .html file which is helpful in that it can be done by non programmers. Eessentially selenium as a Domain Specific Language creates artifacts rather than tribal knowledge.

*The Selenium Documentation is overly complicated by legacy versions just use the IDE, play with the record button and click on stuff, save the .html, and analyze and you'll quickly get the hang of it.*

#### Example Selenium Test HTML

    :::html
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/>
    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head profile="http://selenium-ide.openqa.org/profiles/test-case">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <link rel="selenium.base" href="https://mysite.com/" />
    <title>selenium-login</title>
    </head>
    <body>
        <table cellpadding="1" cellspacing="1" border="1">
	    <thead>
	    <tr><td rowspan="1" colspan="3">selenium-login</td></tr>
	    </thead><tbody>
	    <tr>
	    <td>open</td>
	    <td>/</td>
	    <td></td>
	    </tr>
	    <tr>
	    <td>type</td>
	    <td>id=email</td>
	    <td>admin@mysite.com</td>
	    </tr>
	    <tr>
	    <td>type</td>
	    <td>id=password</td>
	    <td>examplepassword</td>
	    </tr>
	    <tr>
	    <td>clickAndWait</td>
	    <td>id=signin</td>
	    <td></td>
	    </tr>
	    <tr>
	    <td>assertLocation</td>
	    <td>https://mysite.com/home</td>
	    <td></td>
	    </tr>
	    <tr>
	    <td>assertElementPresent</td>
	    <td>link=Launch the web app</td>
	    <td></td>
	    </tr>
	    </tbody></table>
    </body>
    </html>

To get started with the IDE automation framework for interactions with websites (like a programmatic browser) <http://docs.seleniumhq.org/docs/02_selenium_ide.jsp#introduction>

### Selenium WebDriver
Characteristics of good test plans are focusing on "happy path" high value tests, avoiding fragility/brittleness (any change invalidates many tests), and of course avoiding manual intervention.

Having a huge suite of IDE based tests incurs potentially unsustainable technical testing debt *(e.g. investigating/rewriting why/when many tests fail).*

And requiring a testing machine with a UI with a browser etc. is a lot of overhead if you intend on (correctly!) running the tests really often.

Converting raw .html tests to a specific language binding (i.e. moving more to WhiteBox) can remove non essential parts of the test and increase flexibility (multiple browsers!).

`sudo pip install selenium`
> installation assuming linux and python

#### Example Selenium Python Webdriver

> The IDE helpfully not only can save a Test but can File -> Export Test Case As -> python

    :::python
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import Select
    from selenium.common.exceptions import NoSuchElementException
    import unittest, time, re
    
    
    class SeleniumLogin(unittest.TestCase):
	def setUp(self):
	    self.driver = webdriver.Firefox()
	    self.driver.implicitly_wait(30)
	    self.base_url = "https://mysite.com/"
	    self.verificationErrors = []
	    self.accept_next_alert = True
    
	def test_selenium_login(self):
	    driver = self.driver
	    driver.get(self.base_url + "/")
	    driver.find_element_by_id("email").clear()
	    driver.find_element_by_id("email").send_keys("admin@mysite.com")
	    driver.find_element_by_id("password").clear()
	    driver.find_element_by_id("password").send_keys("examplepassword")
	    driver.find_element_by_id("signin").click()
	    self.assertEqual("https://mysite.com/home", driver.current_url)
	    self.assertTrue(self.is_element_present(By.LINK_TEXT, "Launch the web app"
    
	def is_element_present(self, how, what):
	    try: self.driver.find_element(by=how, value=what)
	    except NoSuchElementException, e: return False
	    return True
    
	def is_alert_present(self):
	    try: self.driver.switch_to_alert()
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
	    finally: self.accept_next_alert = True
     
	def tearDown(self):
	    self.driver.quit()
	    self.assertEqual([], self.verificationErrors)
    
    
    if __name__ == "__main__":
	unittest.main()

`python selenium-login.py runs the tests (opens Firefox, executes all of the commands)`

Docs for the webdriver interface:

- <https://selenium-python.readthedocs.io/api.html>
- <https://seleniumhq.github.io/selenium/docs/api/py/api.html>

> useful for looking up things like `driver.current_url`

### Selenium Performance with PhantomJS

Removing the UI requirement improves test performance and increases the options of where the test is run (Dev machines, headless VMs, cloud servers, etc.)

Installing the python selenium library, downloading the phantomJS binary running it was relatively easy with Ubuntu Linux since the project integrated GhostDriver too.

The phantomjs headless browser <http://phantomjs.org> **Archived as of 2018-03 and no longer under active development**

#### Installing PhantomJS

**Archived as of 2018-03 and no longer under active development** <http://phantomjs.org/download.html>

For example for Linux one might use:

    wget <https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-1.9.8-linux-x86_64.tar.bz2>
    tar -xjvf phantomjs-1.9.8-linux-x86_64.tar.bz2


#### Example PhantomJS webdriver python script
**mini script to just show usage**

    :::python
    from selenium import webdriver
     
    driver = webdriver.PhantomJS(executable_path='/opt/phantomjs-1.9.8-linux-x86_64/bin/phantomjs', port=9134)
    driver.get("http://127.0.0.1")
    print driver.current_url
    driver.quit
    print "done"
    
**To run the phantomJS binary** `phantomjs-1.9.8-linux-x86_64/bin/phantomjs --webdriver=9134`
> ghostdriver included and running on port 9134

As an example I found PhantomJS to be at least twice as fast as Firefox
    ./phantomjs --webdriver=127.0.0.1:9134 --ignore-ssl-errors=true
> skip verifying SSL 


#### Advanced Python and PhantomJS example

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
    
### Basic Polling with Firefox and Mac

    import datetime
    import os
    import sys
    import time
    import urllib2

    from selenium import webdriver
    from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


    FIREFOX_MAC_PATH = '/Applications/Firefox.app/Contents/MacOS/firefox-bin'
    G_URL = 'https://g.example.com'

    if __name__ == '__main__':

        if len(sys.argv) < 2:
            print('Usage error: requires a username')
            sys.exit(1)
        print(sys.argv)
        username = sys.argv[1]

        # https://docs.python.org/2/library/datetime.html#strftime-strptime-behavior
        new_server_name = datetime.datetime.now().strftime('%d%b%H%M%S').lower()

        if os.path.exists(FIREFOX_MAC_PATH):
            driver = FirefoxBinary(firefox_path=FIREFOX_MAC_PATH)
        else:
            driver = webdriver.Firefox()

        driver.get(G_URL)
        print(driver.current_url)
        if driver.current_url.endswith('login'):
            driver.find_element_by_name('username').clear()
            driver.find_element_by_name('username').send_keys(username)
            driver.find_element_by_css_selector('input[type="submit"]').click()

        driver.get('{}/deploy/simple_server'.format(G_URL))
        driver.find_element_by_name('name').clear()
        driver.find_element_by_name('name').send_keys('{}-{}'.format(username, new_server_name))
        driver.find_element_by_name('hostname').clear()
        driver.find_element_by_name('hostname').send_keys('{}-{}'.format(username, new_server_name))
        driver.find_element_by_css_selector('input[type="submit"]').click()
        url = 'https://{}-{}.example.com'.format(username, new_server_name)

        print('requested build of {}'.format(url))
        for _ in xrange(20):
            status_code = 404
            try:
                connection = urllib2.urlopen(urllib2.Request(url))
                status_code = connection.getcode()
                content = connection.read()
            except Exception as error:
                print('waiting for {}'.format(url))

            if status_code == 200:
                break
            time.sleep(30)

        driver.get(url)
        print(driver.current_url)
        print(driver.title)
        driver.quit()
        print('done')


**More Info** <https://realpython.com/headless-selenium-testing-with-python-and-phantomjs/>

