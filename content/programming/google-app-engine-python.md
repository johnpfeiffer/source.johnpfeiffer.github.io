Title: Google App Engine Python
Date: 2013-01-26 15:01
Tags: programming, google app engine, python, webapp2

[TOC]

## Setting Up

Sign up for Google App Engine (gmail + SMS verification)

"Google App Engine (often referred to as GAE or simply App Engine, and also used by the acronym GAE/J) is a platform as a service (PaaS) cloud computing platform for developing and hosting web applications in Google-managed data centers."

The Admin Dashboard is linked to your Google profile <https://console.cloud.google.com>

Login and create an Application (e.g. named john-pfeiffer reachable at <http://john-pfeiffer.appspot.com>)

Download and extract the SDK (e.g. gae-python.zip)

    cd google_appengine
    cp -a new_project_template helloworld
> Inside is the minimum file structucture required to have an application

- app.yaml is the configuration file
- index.yaml is how to override configuration for database indices
- favicon.ico is the icon that appears in the browser tab or bookmark <https://en.wikipedia.org/wiki/Favicon>
- main.py is the entrypoint for your application

- - -

### A first helloworld/app.yaml


    application: john-pfeiffer
    version: 1
    runtime: python27
    api_version: 1
    threadsafe: yes
    
    handlers:
    - url: /favicon\.ico
    static_files: favicon.ico
    upload: favicon\.ico
    
    - url: .*
    script: main.app
    
    libraries:
    - name: webapp2
    version: "2.5.2"


### helloworld/main.py

    :::python
    #!/usr/bin/env python
    import webapp2

    class MainHandler(webapp2.RequestHandler):
        def get(self):
            self.response.write('Hi World!')

    app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)


### View the app on your local machine

    cd google_appengine
    ./dev_appserver.py ./helloworld

        INFO 2012-12-27 04:20:20,399 dev_appserver_multiprocess.py:655]
        Running application dev\~john-pfeiffer on port 8080:
        http://localhost:8080
        
        INFO 2012-12-27 04:20:20,399 dev_appserver_multiprocess.py:657] Admin console is available at: http://localhost:8080/\_ah/admin


### Upload the app to Google App Engine

    ./appcfg.py update helloworld/
    
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
    

Verify with `curl http://john-pfeiffer.appspot.com`

## Download an existing application from Google App Engine

    mkdir -p /tmp/myapp
    appcfg.py download_app -A john-pfeiffer /tmp/myapp

> This will use OAuth 2 to open a browser/give you a link where you can confirm the action
> Once confirmed it will download the latest version off your application code and files
> This is independent of and not a replacement for version control!

## Updating the Application for routes and POST requests

It is easy to use the MVC pattern while inheriting from the framework <https://webapp-improved.appspot.com/guide/handlers.html>

### app.yaml

> Note that the version has to be explicitly updated in order to deploy something new

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

### main.py

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


### Update the google app engine application code that is running in the cloud

    ./appcfg.py update john-pfeiffer
> update does not publish the new version yet

    ./appcfg.py set_default_version john-pfeiffer
> or you can use the WebUI dashboard to change the default or delete a Version for an Application Instance

<https://cloud.google.com/appengine/docs/python/config/appref>


- - -
## A simple single file CRUD app using the Google AppEngine Database

Google AppEngine applications can leverage the platforms NoSQL database <https://cloud.google.com/appengine/docs/python/datastore/>

The example application below also shows how to override the default 404 and 500 errors with custom jinja2 templates which would require installing the jinja2 dependency and an extra subdirectory named templates with the HTML
- <https://blog.john-pfeiffer.com/jinja2-a-web-html-template-layout-for-everyone/>
- <https://cloud.google.com/appengine/docs/python/ndb/> has improved and deprecated the DB Datastore library used below

    :::python
    #!/usr/bin/env python
    # 2013-01-20 johnpfeiffer
    
    import os
    import logging
    import traceback
    import cgi
    import datetime
    import webapp2
    import jinja2
    
    from google.appengine.ext import db

    jinja_environment = jinja2.Environment( loader=jinja2.FileSystemLoader( os.path.dirname( os.path.dirname( __file__ ) ) ) )        
    
    class Node( db.Model ):
        id = db.StringProperty()
        name = db.StringProperty()
        parent_id = db.StringProperty()
        date = db.DateTimeProperty( auto_now_add = True )
    
    
    # TODO: navigation bar
    class MainPage( webapp2.RequestHandler ):
      def get( self ):
        self.response.out.write( '<html><body>' )
        self.response.out.write( """Welcome <br/>
    
             <form action="/listnodes" method="get">
                 <input type="submit" value="List Nodes">
             </form>
             <br/>
             <form action="/createnodeform" method="get">
                 <input type="submit" value="Create Node">
             </form>
             <form action="/deletenode" method="post">
                 <label>id</label></td><td><input type="text" id="id" name="id" />
                 <input type="submit" value="Delete Node">
             </form>
    
             """
        )
        self.response.out.write( "</body></html>" )
    
    
    class ListNodes( webapp2.RequestHandler ):
      def get( self ):
        self.response.out.write( '<html><body>' )
        self.response.out.write( 'Welcome <br/>' )
        q = db.Query( Node )
        q.order( "name" )
        q.fetch( 100 )
        self.response.out.write( "%s , %s , %s ( %s )<br/>" % ( "name" , "id" , "parent_id" , "created" ) )
        for node in q :
            self.response.out.write( "%s , %s , %s ( %s )<br/>" % ( node.name , node.id , node.parent , node.date ) )
    
        self.response.out.write( "</body></html>" )
    
    
    # TODO: use template system
    class CreateNode( webapp2.RequestHandler ):
      def get( self ):
        self.response.out.write( '<html><body>' )
        self.response.write( 'Create uses POST' )
        self.response.out.write( "</body></html>" )
    
      def post( self ):
        self.response.out.write( '<html><body>' )
        post_values = self.request.POST
    
        # todo extract to helper for input validation and sanitization
        name = post_values[ "nodename" ]
        id = post_values[ "id" ]
        parent_id = post_values[ "parentid" ]
    
        if( name == None or id == None or parent_id == None ):
            self.response.out.write( 'ERROR: DEBUG:' , post_values )
        else:
            node = Node()
            node.name = name
            node.id = id
            node.parent_id = parent_id
    
            node.put()
            self.response.out.write( 'successfully created: ' + name )
            self.response.out.write( """
             <form action="/listnodes" method="get">
                 <input type="submit" value="List Nodes">
             </form>
            """
            )
    
        self.response.out.write( "</body></html>" )
    
    
    class CreateNodeForm( webapp2.RequestHandler ):
        def get( self ):
            self.response.out.write( '<html><body>' )
            self.response.out.write( """
             <form action="/createnode" method="post">
                <table>
                    <tr><td><label>node name</label></td><td><input type="text" id="nodename" name="nodename" /></td></tr>
                    <tr><td><label>id</label></td><td><input type="text" id="id" name="id" /></td></tr>
                    <tr><td><label>parent id</label></td><td><input type="text" id="parentid" name="parentid" /></td></tr>
                    <tr><td></td><td><input type="submit"></td></tr>
                </table>
              </form>
            """ )
            self.response.out.write( "</body></html>" )
    
    
    # TODO: use template system
    class DeleteNode( webapp2.RequestHandler ):
      def get( self ):
        self.response.out.write( '<html><body>' )
        self.response.write( 'Delete uses POST' )
        self.response.out.write( "</body></html>" )
    
      def post( self ):
        self.response.out.write( '<html><body>' )
        post_values = self.request.POST
    
        # todo extract to helper for input validation and sanitization
        id = post_values[ "id" ]
    
    #    q = db.Query( Node )    # keys_only is faster and cheaper than retrieving the entities
    #    q.filter( "id=" , id )
        q = Node.all( keys_only = True ).filter( "id=", id )
        node_to_delete = q.run()
    
    #    db.delete( )
    #    node_key =          # __key__
    
        self.response.out.write( "%s , %s , %s ( %s )<br/>" % ( "name" , id , "parent_id" , node_to_delete ) )
    
    
        self.response.out.write( "</body></html>" )
    
    
    
    # url handler below -----------------------------
    
    app = webapp2.WSGIApplication( [
      ( '/', MainPage ),
      ( '/listnodes' , ListNodes ),
      ( '/createnode' , CreateNode ),
      ( '/createnodeform' , CreateNodeForm ),
      ( '/deletenode' , DeleteNode )
    ], debug = True )

    
    
    def handle_404 (request , response , exception) :
        template_dictionary = { 'title' : 'ERROR 404' , 'body_content' : exception.status }
        template = jinja_environment.get_template ( 'templates/error.html' )
        response.write ( template.render ( template_dictionary ) )
        response.set_status ( exception.status_int )
    
    
    def handle_500 (request , response , exception) :
        logging.error ( traceback.print_exc ( ) )
        logging.error ( exception )
        template_dictionary = { 'title' : 'Meow' , 'body_content' : 'Meow.  Meow meow meow, meow meow.' }
        template = jinja_environment.get_template ( 'templates/error.html' )
        response.write ( template.render ( template_dictionary ) )
        response.set_status ( 500 )
    
    
    app.error_handlers [ 404 ] = handle_404
    app.error_handlers [ 500 ] = handle_500

