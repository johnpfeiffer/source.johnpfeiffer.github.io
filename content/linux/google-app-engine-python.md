Title: Google App Engine Python
Date: 2013-01-26 15:01
Author: John Pfeiffer
Slug: google-app-engine-python

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Sign up for Google App Engine (gmail + SMS verification)

</p>

"Google App Engine (often referred to as GAE or simply App Engine, and
also used by the acronym GAE/J) is a platform as a service (PaaS) cloud
computing platform for developing and hosting web applications in
Google-managed data centers. "

</p>

Login and create an Application (e.g. named john-pfeiffer reachable at
[http://john-pfeiffer.appspot.com][] )

</p>

Download and extract the SDK (e.g. gae-python.zip)

</p>

cd google\_appengine

</p>

cp -a new\_project\_template helloworld

</p>

nano helloworld/app.yaml  

application: john-pfeiffer  

version: 1  

runtime: python27  

api\_version: 1  

threadsafe: yes

</p>

handlers:  

- url: /favicon\\.ico  

static\_files: favicon.ico  

upload: favicon\\.ico

</p>

- url: .\*  

script: main.app

</p>

libraries:  

- name: webapp2  

version: "2.5.2"

</p>

nano helloworld/main.py

</p>

\#!/usr/bin/env python  

import webapp2

</p>

class MainHandler( webapp2.RequestHandler ):  

def get( self ):  

self.response.write( 'Hi World!' )

</p>

app = webapp2.WSGIApplication( [  

( '/' , MainHandler )  

], debug=True )

</p>

\# VIEW THE APP ON YOUR LOCAL MACHINE  

./dev\_appserver.py helloworld  

INFO 2012-12-27 04:20:20,399 dev\_appserver\_multiprocess.py:655]
Running application dev\~john-pfeiffer on port 8080:
[http://localhost:8080][]  

INFO 2012-12-27 04:20:20,399 dev\_appserver\_multiprocess.py:657] Admin
console is available at: [http://localhost:8080/\_ah/admin][]

</p>

\# UPLOAD THE APP TO GOOGLE APP ENGINE  

./appcfg.py update helloworld/

</p>

07:44 PM Host: appengine.google.com  

07:44 PM Application: john-pfeiffer; version: 1  

07:44 PM  

Starting update of app: john-pfeiffer, version: 1  

07:44 PM Getting current resource limits.  

07:44 PM Scanning files on local disk.  

07:44 PM Cloning 1 static file.  

07:44 PM Cloning 3 application files.  

07:44 PM Uploading 1 files and blobs.  

07:44 PM Uploaded 1 files and blobs  

07:44 PM Compilation starting.  

07:44 PM Compilation completed.  

07:44 PM Starting deployment.  

07:45 PM Checking if deployment succeeded.  

07:45 PM Will check again in 1 seconds.  

07:45 PM Checking if deployment succeeded.  

07:45 PM Will check again in 2 seconds.  

07:45 PM Checking if deployment succeeded.  

07:45 PM Deployment successful.

</p>

[http://john-pfeiffer.appspot.com][]

</p>

appcfg.py download\_app -A -V

</p>

- - - - - - - - - - - - - - - - - - - - - - - -  

app.yaml

</p>

application: john-pfeiffer  

version: 6  

runtime: python27  

api\_version: 1  

threadsafe: yes

</p>

handlers:  

- url: /favicon\\.ico  

static\_files: favicon.ico  

upload: favicon\\.ico

</p>

- url: .\*  

script: main.app

</p>

libraries:  

- name: webapp2  

version: "2.5.2"

</p>

main.py

</p>

\#!/usr/bin/env python

</p>

import webapp2

</p>

class MainHandler( webapp2.RequestHandler ):  

def get( self ):  

self.response.write( 'hello John Pfeiffer!' )

</p>

class PageOne( webapp2.RequestHandler ):  

def get( self ):

</p>

self.response.write( """

</p>

PageOne

</p>

""");

</p>

class PageTwo( webapp2.RequestHandler ):  

def get( self ):  

self.response.write( 'PageTwo' )

</p>

def post( self ):  

get\_values = self.request.GET  

post\_values = self.request.POST  

self.response.write( str( get\_values ) + "\\n")  

self.response.write( str( post\_values ) )

</p>

app = webapp2.WSGIApplication([  

('/', MainHandler),  

('/page-one', PageOne),  

('/page-two', PageTwo)  

], debug=True)

</p>

def main():  

run\_wsgi\_app( application )

</p>

if \_\_name\_\_ == "\_\_main\_\_":  

main()

</p>

./appcfg.py update john-pfeiffer  

\# update does not publish the new version yet

</p>

./appcfg.py set\_default\_version john-pfeiffer  

\# or you can use the WebUI dashboard to change the default or delete a
Version for an Application Instance

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Programming][]
-   [IT][]

</div>
</p>

  [http://john-pfeiffer.appspot.com]: http://john-pfeiffer.appspot.com
  [http://localhost:8080]: http://localhost:8080
  [http://localhost:8080/\_ah/admin]: http://localhost:8080/_ah/admin
  [Programming]: http://john-pfeiffer.com/category/tags/programming
  [IT]: http://john-pfeiffer.com/category/it
