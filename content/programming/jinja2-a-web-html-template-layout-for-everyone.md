Title: Jinja2, a web html template layout for everyone
Date: 2013-04-30 04:35
Tags: programming, jinja2, python, webapp2, tablesorter.js

Web development used to be so hard (and static). (read &\#60;bold&\#62;)

Now everyone realizes (along with version control and automated testing) that decoupling views and displays from dynamic code makes everyone's life easier! 

(Refresh your colors and layout without having to touch your backend logic! Re-engineer your persistence layer and business logic but leave your uber wow design intact! Allow front end and back end developers to work in parallel!)

Jinja2 is an excellent framework for python developers (to go with your uwsgi + django or webapp2) to get html templates (do not repeat yourself!) that can show off all of your backend python data magic with some pizazz.

It's fairly easy to do all sorts of powerful things (like accessing variables, loops, etc.)
<http://jinja.pocoo.org/docs>

When combined with css and jquery (i.e. tablesorter) you can quickly throw together a decent looking interactive experience.

- <http://jquery.com/download>
- <http://tablesorter.com/docs>


Here's my budding ode to sorting algorithms (yes, Google App Engine is free)
<http://john-pfeiffer.appspot.com/algorithms>  #TODO: finish using jquery tablesorter


A webapp2 project layout and source code example (please excuse the code formatting, you'll need to imagine the correct indents)...

## File Layout
    assets/css/style.css  
    assets/css/tablesorter.css  
    assets/images/css/asc.gif (bg.gif, desc.gif, etc.)  
    assets/js/jquery-1.9.1.min.js  
    assets/js/jquery.tablesorter.min.js

    mainhandler.py  
    templates/main.html  
    app.yaml (only required if using AppEngine)  
    main.py  
    routes.py

## app.yaml

    application: john-jinja2  
    version: 1  
    runtime: python27  
    api_version: 1  
    threadsafe: true

    handlers:  
    - url: /favicon.ico  
    static_files: favicon.ico  
    upload: favicon.ico

    - url: /css  
    static_dir: assets/css

    - url: /js  
    static_dir: assets/js

    - url: /images  
    static_dir: assets/images

    - url: /.*  
    script: main.app


    libraries:  
    - name: webapp2  
    version: "2.5.2"

    - name: jinja2  
    version: latest


## main.py
    :::python
    # -*- coding: utf-8 -*-
    import webapp2
    from routes import entry_points
    
    # must be named "application" for uwsgi webapp2, in AppEngine it should be "app"
    application = webapp2.WSGIApplication( entry_points , debug = False )
    
## routes.py
    :::python
    # -*- coding: utf-8 -*-
    import webapp2
    from mainhandler import MainHandler
    
    # Map url's to handlers in the handlers module , optionally choosing specific target method and request type
    entry_points = [ webapp2.Route( '/main', handler=MainHandler, handler_method='get', methods=['GET'] ), ]
    
## mainhandler.py
    :::python
    # -*- coding: utf-8 -*-
    import webapp2
    import jinja2
    import os
    # weird hack to ensure we go up a directory level to correctly find the templates directory
    jinja_environment = jinja2.Environment( loader = jinja2.FileSystemLoader( os.path.dirname(__file__) ) )
    
    class MainHandler( webapp2.RequestHandler ):
        def get( self ):
            # a list of tuples
            result_list = [ ('apples','green'), ('bananas','yellow'), ('cherries','red') ] 
            template = jinja_environment.get_template( 'templates/main.html' )
            template_values = { 'title': 'fruits and colors', 'body_content': 'fruits and colors', 'result_list': result_list }
            self.response.content_type = 'text/html'
            self.response.out.write( template.render( template_values ) )
        
## templates/main.html

    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/1999/html">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <title>{{title}}</title>
        <link type="text/css" rel="stylesheet" href="/css/tablesorter.css" />
        <script type="text/javascript" src="/js/jquery-1.9.1.min.js"></script>
        <script type="text/javascript" src="/js/jquery.tablesorter.min.js"></script>
    </head>
    
    <body>
        {{body_content}}
        
        <div>
            <table id="results" class="tablesorter">
            <thead>
            <tr>
            <th>Fruit</th>
            <th>Color</th>
            </tr>
            </thead>
            <tbody>
            {% for item in result_list %}
            <tr>
            <td><a href="/{{item[0]}}">{{ item[0] }}</a></td><td>{{ item[1] }}</td>
            </tr>
            {% endfor %}
            </tbody>
            </table>
        </div><br/>
        <script type="text/javascript">
        $(document).ready(function() {
        $("#results").tablesorter( {sortList:[[0,1]]} ); # sort descending by the first element
        });
        </script>
    </body>
    </html>
    


## IF NOT USING APPENGINE, /etc/init.d/uwsgi.sh might look like...

    #!/bin/bash
    # 2013-02-22 johnpfeiffer
    
    start(){
        /usr/local/bin/uwsgi --pidfile /var/www/pidfile-uwsgi.pid --touch-reload=/var/www/pidfile-uwsgi.pid --logto2 /var/www/python-john/uwsgi.log --http :8080 --wsgi-file /var/www/main.py --pythonpath /var/www/ &
    }
    
    stop(){
        kill -INT `cat /var/www/pidfile-uwsgi.pid`
        sleep 1
    }
    
    status(){
        ps aux | grep uwsgi
    }
    
    case "$1" in
    status)
        status
        exit 0
        ;;
    start)
        start
        exit 0
        ;;
    stop)
        stop
        exit 0
        ;;
    reload|restart|force-reload)
        stop
        start
        exit 0
        ;;
    **)
        echo "Usage: $0 {start|stop|reload}" 1>&2
        exit 1
        ;;
    esac
   
## Alternate Flask Jinja2 Example
<https://bitbucket.org/johnpfeiffer/tddflask/src>