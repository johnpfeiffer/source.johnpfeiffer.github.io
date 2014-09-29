Title: Jinja2, a web html template layout for everyone
Date: 2013-04-30 04:35
Author: John Pfeiffer
Slug: jinja2-a-web-html-template-layout-for-everyone

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Web development used to be so hard (and static). (read &\#60;bold&\#62;)

</p>

Now everyone realizes (along with version control and automated testing)
that decoupling views and displays from dynamic code makes everyone's
life easier! (Refresh your colors and layout without having to touch
your backend logic! Re-engineer your persistence layer and business
logic but leave your uber wow design intact! Allow front end and back
end developers to work in parallel!)

</p>

Jinja2 is an excellent framework for python developers (to go with your
uwsgi + django or webapp2) to get html templates (do not repeat
yourself!) that can show off all of your backend python data magic with
some pizazz.

</p>

It's fairly easy to do all sorts of powerful things (like accessing
variables, loops, etc.)  
[http://jinja.pocoo.org/docs/][]

</p>

When combined with css and jquery (i.e. tablesorter) you can quickly
throw together a decent looking interactive experience.  
[http://jquery.com/download/][]
[http://tablesorter.com/docs/\#Download][]

</p>

Here's my budding ode to sorting algorithms (yes, Google App Engine is
free)

</p>

[http://john-pfeiffer.appspot.com/algorithms][] \#TODO: finish using
jquery tablesorter

</p>

A webapp2 project layout and source code example (please excuse the code
formatting, you'll need to imagine the correct indents)...
[http://john-jinja2.appspot.com/main][]

</p>

assets/css/style.css  

assets/css/tablesorter.css  

assets/images/css/asc.gif (bg.gif, desc.gif, etc.)  

assets/js/jquery-1.9.1.min.js  

assets/js/jquery.tablesorter.min.js

</p>

mainhandler.py  

templates/main.html  

app.yaml (only required if using AppEngine)  

main.py  

routes.py

</p>

APP.YAML  

application: john-jinja2  

version: 1  

runtime: python27  

api\_version: 1  

threadsafe: true

</p>

handlers:  

- url: /favicon\\.ico  

static\_files: favicon.ico  

upload: favicon\\.ico

</p>

- url: /css  

static\_dir: assets/css

</p>

- url: /js  

static\_dir: assets/js

</p>

- url: /images  

static\_dir: assets/images

</p>

- url: /.\*  

script: main.app

</p>

libraries:  

- name: webapp2  

version: "2.5.2"

</p>

- name: jinja2  

version: latest

</p>

MAIN.PY  

\# -\*- coding: utf-8 -\*-  

import webapp2  

from routes import entry\_points

</p>

\# must be named "application" for uwsgi webapp2, in AppEngine it should
be "app"  

application = webapp2.WSGIApplication( entry\_points , debug = False )

</p>

ROUTES.PY  

\# -\*- coding: utf-8 -\*-  

import webapp2  

from mainhandler import MainHandler

</p>

\# Map url's to handlers in the handlers module , optionally choosing
specific target method and request type  

entry\_points = [ webapp2.Route( '/main', handler=MainHandler,
handler\_method='get', methods=['GET'] ),  

]

</p>

MAINHANDLER.PY  

\# -\*- coding: utf-8 -\*-  

import webapp2  

import jinja2  

import os  

\# weird hack to ensure we go up a directory level to correctly find the
templates directory  

jinja\_environment = jinja2.Environment( loader =
jinja2.FileSystemLoader( os.path.dirname(\_\_file\_\_) ) )

</p>

class MainHandler( webapp2.RequestHandler ):

</p>

def get( self ):  

result\_list = [ ('apples','green'), ('bananas','yellow'),
('cherries','red') ] \# a list of tuples  

template = jinja\_environment.get\_template( 'templates/main.html' )  

template\_values = { 'title': 'fruits and colors', 'body\_content':
'fruits and colors', 'result\_list': result\_list }  

self.response.content\_type = 'text/html'  

self.response.out.write( template.render( template\_values ) )

</p>

TEMPLATES/MAIN.HTML  

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"[http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"\>][]  

<html xmlns="[http://www.w3.org/1999/xhtml"][]
xmlns="[http://www.w3.org/1999/html"\>][]  

<head\>  

<meta http-equiv="Content-Type" content="text/html; charset=utf-8" /\>  

<title\>{{title}}</title\>  

<link type="text/css" rel="stylesheet" href="/css/tablesorter.css" /\>  

<script type="text/javascript"
src="/js/jquery-1.9.1.min.js"\></script\>  

<script type="text/javascript"
src="/js/jquery.tablesorter.min.js"\></script\>  

</head\>

</p>

<body\>  

{{body\_content}}

</p>

<div\>  

<table id="results" class="tablesorter"\>  

<thead\>  

<tr\>  

<th\>Fruit</th\>  

<th\>Color</th\>  

</tr\>  

</thead\>  

<tbody\>  

{% for item in result\_list %}  

<tr\>  

<td\><a href="/{{item[0]}}"\>{{ item[0] }}</a\></td\><td\>{{ item[1]
}}</td\>  

</tr\>  

{% endfor %}  

</tbody\>  

</table\>  

</div\><br/\>  

<script type="text/javascript"\>  

$(document).ready(function() {  

$("\#results").tablesorter( {sortList:[[0,1]]} ); \# sort descending by
the first element  

});  

</script\>

</p>

</ body\>  

</ html\>

</p>

IF NOT USING APPENGINE, /etc/init.d/uwsgi.sh might look like...  

\#!/bin/bash  

\# 2013-02-22 johnpfeiffer

</p>

start(){  

/usr/local/bin/uwsgi --pidfile /var/www/pidfile-uwsgi.pid
--touch-reload=/var/www/pidfile-uwsgi.pid --logto2
/var/www/python-john/uwsgi.log --http :8080 --wsgi-file /var/www/main.py
--pythonpath /var/www/ &  

}

</p>

stop(){  

kill -INT \`cat /var/www/pidfile-uwsgi.pid\`  

sleep 1  

}

</p>

status(){  

ps aux | grep uwsgi  

}

</p>

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

\*\*)  

echo "Usage: $0 {start|stop|reload}" 1\>&2  

exit 1  

;;  

esac

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

  [http://jinja.pocoo.org/docs/]: http://jinja.pocoo.org/docs/
  [http://jquery.com/download/]: http://jquery.com/download/
  [http://tablesorter.com/docs/\#Download]: http://tablesorter.com/docs/#Download
  [http://john-pfeiffer.appspot.com/algorithms]: http://john-pfeiffer.appspot.com/algorithms
  [http://john-jinja2.appspot.com/main]: http://john-jinja2.appspot.com/main
  [http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"\>]: http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
  [http://www.w3.org/1999/xhtml"]: http://www.w3.org/1999/xhtml&quot
  [http://www.w3.org/1999/html"\>]: http://www.w3.org/1999/html">
  [Programming]: http://john-pfeiffer.com/category/tags/programming
