Title: Selenium headless browser automated testing with PhantomJS and Python
Date: 2013-09-17 21:04
Author: John Pfeiffer
Slug: selenium-headless-browser-automated-testing-with-phantomjs-and-python

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
selenium: automation of browser actions
([http://docs.seleniumhq.org/docs/02\_selenium\_ide.jsp\#introduction][])

</p>

phantomjs: headless browser ([http://phantomjs.org/][])

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - -  

pip install selenium

</p>

wget
[https://code.google.com/p/phantomjs/downloads/detail?name=phantomjs-1.9....][]  

tar -xjvf phantomjs-1.9.2-linux-x86\_64.tar.bz2

</p>

phantomjs-1.9.2-linux-x86\_64/bin/phantomjs --webdriver=9134 \# run
ghostdriver on a port

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - -  

\# mini script to just show usage

</p>

from selenium import webdriver

</p>

driver = webdriver.PhantomJS(
executable\_path='/opt/phantomjs-1.9.2-linux-x86\_64/bin/phantomjs',
port=9134 )  

driver.get( "[http://127.0.0.1][]" )  

print driver.current\_url  

driver.quit  

print "done"

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - -  

phantomjs-1.9.2-linux-x86\_64/bin/phantomjs --webdriver=9134
--ignore-ssl-errors=true

</p>

\# more complete example with python unittest framework (used the
Firefox Selenium IDE plugin -\> Export)  

\# logs in, asserts there is an Admin tab which when clicked shows Group
Info

</p>

from selenium import webdriver  

from selenium.webdriver.common.by import By  

from selenium.webdriver.common.keys import Keys  

from selenium.webdriver.support.ui import Select  

from selenium.common.exceptions import NoSuchElementException  

import unittest, time, re

</p>

class SeleniumAdminLogin( unittest.TestCase ):  

def setUp( self ):  

self.driver = webdriver.PhantomJS(
'/opt/phantomjs-1.9.2-linux-x86\_64/bin/phantomjs', port=9134 )  

self.driver.implicitly\_wait(30)  

self.base\_url = "[https://myexample.org][]"  

self.verificationErrors = []  

self.accept\_next\_alert = True

</p>

def test\_selenium\_admin\_login( self ):  

driver = self.driver  

driver.get( self.base\_url + "/" )  

driver.find\_element\_by\_id( "email" ).clear()  

driver.find\_element\_by\_id( "email" ).send\_keys(
"[admin@example.org][]" )  

driver.find\_element\_by\_id( "password" ).clear()  

driver.find\_element\_by\_id( "password" ).send\_keys( "mypassword" )  

driver.find\_element\_by\_id( "signin" ).click()  

self.assertEqual("[https://myexample.org/home][]", driver.current\_url)  

self.assertTrue(self.is\_element\_present(By.LINK\_TEXT, "Launch the web
app"))  

self.assertTrue(self.is\_element\_present(By.CSS\_SELECTOR, "a.admin \>
span"))  

driver.find\_element\_by\_css\_selector("a.admin \> span").click()  

self.assertEqual("Group Info",
driver.find\_element\_by\_css\_selector("h1").text)

</p>

def is\_element\_present(self, how, what):  

try: self.driver.find\_element(by=how, value=what)  

except NoSuchElementException, e: return False  

return True

</p>

def is\_alert\_present(self):  

try: self.driver.switch\_to\_alert()  

except NoAlertPresentException, e: return False  

return True

</p>

def close\_alert\_and\_get\_its\_text(self):  

try:  

alert = self.driver.switch\_to\_alert()  

alert\_text = alert.text  

if self.accept\_next\_alert:  

alert.accept()  

else:  

alert.dismiss()  

return alert\_text  

finally: self.accept\_next\_alert = True

</p>

def tearDown(self):  

self.driver.quit()  

self.assertEqual([], self.verificationErrors)

</p>

if \_\_name\_\_ == "\_\_main\_\_":  

unittest.main()

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - -  

REFERENCES:  
[http://phantomjs.org/release-1.8.html][]  
[https://github.com/ariya/phantomjs/wiki/API-Reference][]  
[http://www.realpython.com/blog/python/headless-selenium-testing-with-pyt...][]

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Programming][]

</div>
</p>

  [http://docs.seleniumhq.org/docs/02\_selenium\_ide.jsp\#introduction]:
    http://docs.seleniumhq.org/docs/02_selenium_ide.jsp#introduction
  [http://phantomjs.org/]: http://phantomjs.org/
  [https://code.google.com/p/phantomjs/downloads/detail?name=phantomjs-1.9....]:
    https://code.google.com/p/phantomjs/downloads/detail?name=phantomjs-1.9.2-linux-x86_64.tar.bz2
  [http://127.0.0.1]: http://127.0.0.1
  [https://myexample.org]: https://myexample.org
  [admin@example.org]: mailto:admin@example.org
  [https://myexample.org/home]: https://myexample.org/home
  [http://phantomjs.org/release-1.8.html]: http://phantomjs.org/release-1.8.html
  [https://github.com/ariya/phantomjs/wiki/API-Reference]: https://github.com/ariya/phantomjs/wiki/API-Reference
  [http://www.realpython.com/blog/python/headless-selenium-testing-with-pyt...]:
    http://www.realpython.com/blog/python/headless-selenium-testing-with-python-and-phantomjs/
  [Programming]: http://john-pfeiffer.com/category/tags/programming
