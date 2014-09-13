Title: Mobile edit cloud execution of python code
Date: 2014-09-07 21:37
Tags: python, flask, openshift

Haven't you just wanted to work through a coding kata <http://codekata.com> or puzzle on your phone?

Python is a great language for getting stuff done, and while there are some mobile apps often they are limited by the platform (eg ios sans file system).

Using the link from a Dropbox text file and a linode server (could be openshift red hat cloud?)...

- start running the script on the remote server that waits for new code to execute `python myflaskapp.py &`
- I can edit using Nocs 
- Nocs syncs from iOS to Dropbox
- hitting a URL in my browser 
    - the python script downloads the latest version of the code (using shell to curl as Dropbox use javascript to authorize and return a link to the latest version) 
    - executes using the remote python environment 
    - returns the output

**Note! This may be dangerous as hackers could exploit to run arbitrary code, use at your own risk.**

*Also, clearly, downloading from Dropbox using curl is a hack with no guarantee of future support =]

    from flask import Flask
    import os
    from subprocess import Popen, PIPE
    import urllib2

    app = Flask(__name__)

    @app.route('/mysecreturl')
    def update_and_run():
      output=''
      try:
          name = 'exercises.py'
          path = '/var/www/mystuff'
          urlpath = 'https://www.dropbox.com/s/ancdefgrandom/exercises.py?dl=0'
          os.system('curl --silent --location --insecure --output exercises.py https://www.dropbox.com/s/ancdefgrandom/exercises.py?dl=0')      
          output = Popen(["python",name], stdout=PIPE).communicate()[0]
      except Exception as error:
          return str(error)
      return output


    if __name__ == '__main__':
        app.run('0.0.0.0', 8080, use_reloader=True)


### Flask Application on OpenShift

git clone https://github.com/openshift/flask-example.git

Use the OpenShift WebUI to create an application

On the right of your application the WebUI has a note on how to clone the default repo:

    git clone ssh://12345random@appname-domain.rhcloud.com/~/git/appname.git/
    cd appname
    git remote add upstream -m master git://github.com/openshift/flask-example.git
    git pull -s recursive -X theirs upstream master
    git push
    cd wsgi/
    virtualenv venv

`vi myflaskapp.py`

    from flask import Flask
    import os
    from subprocess import Popen, PIPE
    import urllib2
    
    
    app = Flask(__name__)
    
    @app.route("/")
    def hello():
        return "Hello World!"
    
    
    @app.route('/mysecreturl')
    def update_and_run():
      output=''
      try:
          path = '/var/lib/openshift/12345appid/app-root/data/exercises.py'
          urlpath = 'https://www.dropbox.com/s/12345random/exercises.py?dl=0'
          os.system('curl --silent --location --insecure --output ' + path + ' ' + urlpath)
          output = Popen(["python",path], stdout=PIPE).communicate()[0]
          # output = Popen(["touch",path], stdout=PIPE).communicate()[0]
      except Exception as error:
          return str(error)
      return output
    
    
    if __name__ == "__main__":
        app.run()
    


### More Info

<https://www.openshift.com/blogs/beginners-guide-to-writing-flask-apps-on-openshift>