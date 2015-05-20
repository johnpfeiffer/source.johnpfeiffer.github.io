Title: Tomcat deployment on Openshift for free
Date: 2012-09-11 13:48
Tags: cloud, paas, openshift, tomcat

[TOC]

openshift is the cloud PaaS offering from RedHat

### Prerequisites and dependencies

    
    sudo apt-get update
    sudo apt-get install ruby1.9.3 git-core
    //yay for ubuntu 12.04

    sudo gem install rhc
    //red hat openshift client


### OpenShift Client tools setup

`rhc setup`

    Created local config file: /home/ubuntu/.openshift/express.conf
    The express.conf file contains user configuration, and can be transferred to different computers.
    No SSH keys were found. We will generate a pair of keys for you.
    
    2: No such file or directory
    Created: /home/ubuntu/.ssh/id_rsa.pub  
    
    Your public ssh key must be uploaded to the OpenShift server. Would you like us to upload it for you? (yes/no) yes

### rhc commands

`rhc -h`

`rhc domain show`
> prompts for password

`rhc app create -h`

Valid application types are (nodejs-0.6, ruby-1.9, jbossas-7, python-2.6, jenkins-1.4, ruby-1.8, jbosseap-6.0, diy-0.1, php-5.3, perl-5.10)

`rhc app create -a john -t diy-0.1`

`rhc app show -a john`

`rhc app cartridge list`


### Your local git repo

ON YOUR LOCAL MACHINE BROWSE TO WHERE YOU WANT TO STORE YOUR GIT REPO

`git clone ssh://a261d0fc2932413694456e3473fdc972@APPNAME-DOMAIN.rhcloud.com/~/git/...`

`git status`

`git pull`

### REPO LAYOUT of ~/john/repo

    :::bash
    .openshift/action_hooks/start - Script that gets run to start your application  
    .openshift/action_hooks/stop - Script that gets run to stop your application  
    .openshift/action_hooks/pre_build - Script that gets run every git push before the build  
    .openshift/action_hooks/build - Script that gets run every git push as part of the build process (on the CI system if available)  
    .openshift/action_hooks/deploy - Script that gets run every git push after build but before the app is restarted  
    .openshift/action_hooks/post_deploy - Script that gets run every git push after the app is restarted  

    diy  
    misc  
    README  
    static/ If it exists externally exposed static content goes here


CHANGES ARE ONE DIRECTIONAL FROM THE GIT CLONE TO THE OPENSHIFT BOX

`mv diy/testrubyserver.rb ../misc`

`mv diy/index.html ../misc`

`git add -A`

`git commit -m "moved initial test stuff to /misc"`

`git push`
> if the app is running then a git push automatically ...

    Counting objects: 6, done.
    Delta compression using up to 4 threads.  
    Compressing objects: 100% (4/4), done.  
    Writing objects: 100% (4/4), 607 bytes, done.  
    Total 4 (delta 1), reused 1 (delta 0)  
    remote: Stopping application...  
    remote: Done  
    remote: ~/git/john.git ~/git/john.git  
    remote: ~/git/john.git
    remote: Running .openshift/action_hooks/pre_build  
    remote: Running .openshift/action_hooks/build  
    remote: Running .openshift/action_hooks/deploy  
    remote: Starting application...  
    remote: Done  
    remote: Running .openshift/action_hooks/post_deploy
    

`ssh 33d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com`
> //note that HOME is /var/lib/stickshift/12315longidentifier  

`cd app-root/data`

`wget http://mirror.cc.columbia.edu/pub/software/apache/tomcat/tomcat-7/v7.0.29/bin/apache-tomcat-7.0.29.tar.gz`

tar -xzvf apache-tomcat-7.0.29.tar.gz
> expands to 13MB, note that JAVA is already installed by default

`rm apache-tomcat-7.0.29.tar.gz`


### Openshift ports and proxy

Since OpenShift has a proxy setup that passes port 80 to your local server on port 8080, BUT  

OpenShift does not allow users to bind to any port below 15000 other than 8080, so...

`ssh 33d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com`


`env`
> shows you all of the environment variables in the openShift

multitenant config

`env | grep INTERNAL`

> OPENSHIFT_INTERNAL_PORT=8080  
> OPENSHIFT_INTERNAL_IP=127.13.29.1

`vi app-root/data/apache-tomcat-7.0.29/conf/server.xml`

escape key then :x (save and quit)


- - -

`cd app-root/data/apache-tomcat-7.0.29/bin`

`sh startup.sh && tail -f ../logs/*`

(this is how you can start it manually from within ssh, you'll have to stop it manually too!)


ADDING Tomcat to your default start and stop scripts (which are used during every git push)


In your local git repo there is a hidden directory ".openshift"

`cd APPNAME/.openshift/action_hooks`


### vi .openshift/action_hooks/start

    :::bash
    #nohup $OPENSHIFT_REPO_DIR/diy/testrubyserver.rb
    $OPENSHIFT_INTERNAL_IP $OPENSHIFT_REPO_DIR/diy > $OPENSHIFT_LOG_DIR/server.log 2>&1 &

    cd $OPENSHIFT\_DATA\_DIR/apache-tomcat-7.0.29/bin
    nohup sh startup.sh
    echo "completed tomcat7 startup"


### vi .openshift/action_hooks/stop

    :::bash
    cd $OPENSHIFT_DATA_DIR/apache-tomcat-7.0.29/bin  
    nohup sh shutdown.sh  
    echo "completed tomcat7 shutdown"  
    exit 0



`git add -A`

`git commit -m "removed testrubyserver.rb and added tomcat to start/stop scripts"  

`git push`


**<http://APPNAME-DOMAINNAME.rhcloud.com>**


### Autodeploy the latest

MOVE YOUR WEBAPPS DIRECTORY TO THE GIT REPO SO THAT A GIT PUSH WILL AUTO DEPLOY THE NEWEST

`mv $OPENSHIFT_DATA_DIR/apache-tomcat-7.0.29/webapps ~/john/repo/diy/webapps`

`ln -s ~/john/repo/diy/webapps webapps`


Strongly advised to remove the manager and example apps (just deploy your .war's)

`rhc app stop -a APPNAME -p YOURPASSWORD`
> yes, it uses your RHCloud account username and password for app management

`ssh 33d90ea45fd91e42096651d937e@john-pfeiffer.rhcloud.com`

`mv ~/app-root/data/apache-tomcat-7.0.29/webapps/* app-root/repo/misc`

`mv app-root/repo/misc/ROOT ~/app-root/data/apache-tomcat-7.0.29/webapps`


> rhc app start -a APPNAME -p YOURPASSWORD

### ONCE YOU'VE SSH'D IN...  

`help`

    ps|ls|
    ctl_app start [stop|restart|status]
    mysql | mongo | quota

NOTE: sometimes it's easier to use a UI <https://openshift.redhat.com/app/console/applications>

My Account -> Public Keys

My Applications -> APPLICATION_NAME ->

`rhc app add-alias -a myapp --alias myapp.net`


## Future Thoughts

Eclipse + m2e (maven plugin) + jetty plugin for fast and easy dependency management -> mvn install + added custom script can put your .war into your local openshift repo for continuous deployment.


<https://www.openshift.com/>