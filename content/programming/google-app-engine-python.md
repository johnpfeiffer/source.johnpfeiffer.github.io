Title: Google App Engine Python
Date: 2013-01-26 15:01
Tags: programming, google app engine, python, webapp2

Sign up for Google App Engine (gmail + SMS verification)

"Google App Engine (often referred to as GAE or simply App Engine, and also used by the acronym GAE/J) is a platform as a service (PaaS) cloud computing platform for developing and hosting web applications in Google-managed data centers."

Login and create an Application (e.g. named john-pfeiffer reachable at <http://john-pfeiffer.appspot.com>)

Download and extract the SDK (e.g. gae-python.zip)

`cd google_appengine`

`cp -a new_project_template helloworld`


## helloworld/app.yaml

    application: john-pfeiffer  
    version: 1  
    runtime: python27  
    api_version: 1  
    threadsafe: yes
    
    handlers:
    - url: /favicon.ico
    static_files: favicon.ico
    upload: favicon.ico
    - url: /.*
    script: main.app

    libraries:
    - name: webapp2
    version: "2.5.2"


## helloworld/main.py

    :::python
    #!/usr/bin/env python
    import webapp2

    class MainHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write('Hi World!')

    app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)


## View the app on your local machine

`./dev_appserver.py helloworld`

INFO 2012-12-27 04:20:20,399 dev_appserver_multiprocess.py:655]
Running application dev\~john-pfeiffer on port 8080:
http://localhost:8080

INFO 2012-12-27 04:20:20,399 dev_appserver_multiprocess.py:657] Admin console is available at: http://localhost:8080/\_ah/admin


## Upload the app to Google App Engine

`./appcfg.py update helloworld/`

    07:44 PM Host: appengine.google.com  
    07:44 PM Application: john-pfeiffer; version: 1  
    07:44 PM Starting update of app: john-pfeiffer, version: 1  
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
    

<http://john-pfeiffer.appspot.com>


`appcfg.py download_app -A -V`


## app.yaml

    application: john-pfeiffer
    version: 6
    runtime: python27
    api_version: 1
    threadsafe: yes
    
    handlers:  
    - url: /favicon.ico
    static_files: favicon.ico
    upload: favicon.ico
    
    - url: /.*
    script: main.app
    
    libraries:  
    - name: webapp2
    version: "2.5.2"
    
## main.py

    :::python
    #!/usr/bin/env python
    import webapp2

    class MainHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write('hello John Pfeiffer!')

    class PageOne(webapp2.RequestHandler):
        def get(self):
            self.response.write("""
                PageOne
            """);

    class PageTwo(webapp2.RequestHandler):
        def get(self):
            self.response.write('PageTwo')

        def post(self):
            get_values = self.request.GET
            post_values = self.request.POST
            self.response.write(str(get_values) + "\n")
            self.response.write(str(post_values))

    app = webapp2.WSGIApplication([  
            ('/', MainHandler),
            ('/page-one', PageOne),
            ('/page-two', PageTwo)
        ], debug=True)
    
    def main():  
        run_wsgi_app(application)
    
    
    if __name__ == "__main__":  
        main()


## Update the code in the cloud

`./appcfg.py update john-pfeiffer`
> update does not publish the new version yet

`./appcfg.py set_default_version john-pfeiffer`

> or you can use the WebUI dashboard to change the default or delete a Version for an Application Instance

<https://cloud.google.com/appengine/docs/python/config/appconfig>