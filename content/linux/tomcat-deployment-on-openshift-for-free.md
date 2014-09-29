Title: Tomcat deployment on Openshift for free
Date: 2012-09-11 13:48
Slug: tomcat-deployment-on-openshift-for-free

[TOC]
openshift is the cloud PaaS offering from RedHat


### Prerequisites

    sudo apt-get update
    sudo apt-get install ruby1.9.3 git-core
    //yay for ubuntu 12.04

    sudo gem install rhc
   //red hat client

- - -

rhc setup  

    Created local config file: /home/ubuntu/.openshift/express.conf
    The express.conf file contains user configuration, and can be transferred to different computers.
    No SSH keys were found. We will generate a pair of keys for you.
    
    2: No such file or directory
    Created: /home/ubuntu/.ssh/id_rsa.pub  
    
    Your public ssh key must be uploaded to the OpenShift server. Would you like us to upload it for you? (yes/no) yes

### rhc commands

rhc -h

rhc domain show //prompts for password

rhc app create -h  

Valid application types are (nodejs-0.6, ruby-1.9, jbossas-7,
python-2.6, jenkins-1.4, ruby-1.8, jbosseap-6.0, diy-0.1, php-5.3,
perl-5.10)

rhc app create -a john -t diy-0.1

rhc app show -a john

rhc app cartridge list


ON YOUR LOCAL MACHINE BROWSE TO WHERE YOU WANT TO STORE YOUR GIT REPO


git clone git clone
ssh://a261d0fc2932413694456e3473fdc972@APPNAME-DOMAIN.rhcloud.com/\~/git/...

git status
git pull

REPO LAYOUT of \~/john/repo

</p>

.openshift/action\_hooks/start - Script that gets run to start your
application  

.openshift/action\_hooks/stop - Script that gets run to stop your
application  

.openshift/action\_hooks/pre\_build - Script that gets run every git
push before the build  

.openshift/action\_hooks/build - Script that gets run every git push as
part of the build process (on the CI system if available)  

.openshift/action\_hooks/deploy - Script that gets run every git push
after build but before the app is restarted  

.openshift/action\_hooks/post\_deploy - Script that gets run every git
push after the app is restarted  

diy  

misc  

README  

static/ If it exists externally exposed static content goes here

</p>

CHANGES ARE ONE DIRECTIONAL FROM THE GIT CLONE TO THE OPENSHIFT BOX

</p>

mv diy/testrubyserver.rb ../misc  

mv diy/index.html ../misc

</p>

git add -A  

git commit -m "moved initial test stuff to /misc"  

git push //if the app is running then a git push automatically ...

</p>

Counting objects: 6, done.  

Delta compression using up to 4 threads.  

Compressing objects: 100% (4/4), done.  

Writing objects: 100% (4/4), 607 bytes, done.  

Total 4 (delta 1), reused 1 (delta 0)  

remote: Stopping application...  

remote: Done  

remote: \~/git/john.git \~/git/john.git  

remote: \~/git/john.git  

remote: Running .openshift/action\_hooks/pre\_build  

remote: Running .openshift/action\_hooks/build  

remote: Running .openshift/action\_hooks/deploy  

remote: Starting application...  

remote: Done  

remote: Running .openshift/action\_hooks/post\_deploy

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - -  

ssh [51233d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com][] //note
that HOME is /var/lib/stickshift/12315longidentifier  

cd app-root/data  

wget
[http://mirror.cc.columbia.edu/pub/software/apache/tomcat/tomcat-7/v7.0.2...][]  

tar -xzvf apache-tomcat-7.0.29.tar.gz //expands to 13MB, note that JAVA
is already installed by default  

rm apache-tomcat-7.0.29.tar.gz

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - -  

Since OpenShift has a proxy setup that passes port 80 to your local
server on port 8080, BUT  

OpenShift does not allow users to bind to any port below 15000 other
than 8080, so...

</p>

ssh [521233d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com][]

</p>

env //shows you all of the environment variables in the openShift
multitenant config  

env | grep INTERNAL  

OPENSHIFT\_INTERNAL\_PORT=8080  

OPENSHIFT\_INTERNAL\_IP=127.13.29.1

</p>

vi app-root/data/apache-tomcat-7.0.29/conf/server.xml

</p>

escape key then :x (save and quit)

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - -  

cd app-root/data/apache-tomcat-7.0.29/bin

</p>

sh startup.sh && tail -f ../logs/\*

</p>

(this is how you can start it manually from within ssh, you'll have to
stop it manually too!)

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - -  

ADDING Tomcat to your default start and stop scripts (which are used
during every git push)

</p>

In your local git repo there is a hidden directory ".openshift"

</p>

cd APPNAME/.openshift/action\_hooks

</p>

vi .openshift/action\_hooks/start  

\#nohup $OPENSHIFT\_REPO\_DIR/diy/testrubyserver.rb
$OPENSHIFT\_INTERNAL\_IP $OPENSHIFT\_REPO\_DIR/diy \>
$OPENSHIFT\_LOG\_DIR/server.log 2\>&1 &

</p>

cd $OPENSHIFT\_DATA\_DIR/apache-tomcat-7.0.29/bin  

nohup sh startup.sh  

echo "completed tomcat7 startup"

</p>

vi .openshift/action\_hooks/stop  

cd $OPENSHIFT\_DATA\_DIR/apache-tomcat-7.0.29/bin  

nohup sh shutdown.sh  

echo "completed tomcat7 shutdown"  

exit 0

</p>

git add -A  

git commit -m "removed testrubyserver.rb and added tomcat to start/stop
scripts"  

git push

</p>

[http://APPNAME-DOMAINNAME.rhcloud.com][]

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - -  

MOVE YOUR WEBAPPS DIRECTORY TO THE GIT REPO SO THAT A GIT PUSH WILL AUTO
DEPLOY THE NEWEST

</p>

mv $OPENSHIFT\_DATA\_DIR/apache-tomcat-7.0.29/webapps
\~/john/repo/diy/webapps

</p>

ln -s \~/john/repo/diy/webapps webapps

</p>


Strongly advised to remove the manager and example apps (just deploy your .war's)


//rhc app stop -a APPNAME -p YOURPASSWORD //yes, it uses your RHCloud
account username and password for app management

ssh [521233d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com][]  

mv \~/app-root/data/apache-tomcat-7.0.29/webapps/\* app-root/repo/misc  

mv app-root/repo/misc/ROOT \~/app-root/data/apache-tomcat-7.0.29/webapps


//rhc app start -a APPNAME -p YOURPASSWORD

### ONCE YOU'VE SSH'D IN...  

help  

ps|ls|  

ctl\_app start [stop|restart|status]  

mysql | mongo | quota


NOTE: sometimes it's easier to use a UI
[https://openshift.redhat.com/app/console/applications][]  

My Account -\> Public Keys

My Applications -\> APPLICATION\_NAME -\>

rhc app add-alias -a myapp --alias myapp.net


### FUTURE THOUGHTS

Eclipse + m2e (maven plugin) + jetty plugin for fast and easy dependency management -\> mvn install + added custom script can put your .war into your local openshift repo for continuous deployment.


  [ssh://a261d0fc2932413694456e3473fdc972@APPNAME-DOMAIN.rhcloud.com/\~/git/...]:
    ssh://a261d0fc2932413694456e3473fdc972@APPNAME-DOMAIN.rhcloud.com/~/git/APPNAME.git/
  [51233d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com]: mailto:51233d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com
  [http://mirror.cc.columbia.edu/pub/software/apache/tomcat/tomcat-7/v7.0.2...]:
    http://mirror.cc.columbia.edu/pub/software/apache/tomcat/tomcat-7/v7.0.29/bin/apache-tomcat-7.0.29.tar.gz
  [521233d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com]: mailto:521233d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com
  [http://APPNAME-DOMAINNAME.rhcloud.com]: http://APPNAME-DOMAINNAME.rhcloud.com
  [https://openshift.redhat.com/app/console/applications]: https://openshift.redhat.com/app/console/applications
