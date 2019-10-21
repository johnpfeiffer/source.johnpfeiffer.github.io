Title: Intro to Amazon AWS Elastic Beanstalk
Date: 2014-08-08 20:00
Tags: aws, eb, elastic beanstalk, python, flask

[TOC]

While InfrastructureAsAService lightens the load of Operations, to truly push forward Developers require a frictionless place to deploy applications.

Platform-as-a-Service fills this niche: for this specific example AWS Elastic Beanstalk attempts to create a layer of abstraction on top of existing Amazon technologies. *(updated in 2019)*

> PaaS = no OS management, no ssh required, no chef/puppet scripting, potentially easier (dynamic) scaling

*A previous article about a Google PaaS <https://blog.john-pfeiffer.com/google-app-engine-python>*

## Installing dependencies (to use the CLI)

The AWS CLI relies heavily on Python.  *Originally this guide was written for python2 but now the world is all python3.*

    which pip3
    pip3 --version
    sudo apt install python3-pip --reinstall
> *(to fix when it is missing in ubuntu)*

`pip3 install --upgrade awscli`
> make sure to be on the latest AWS CLI

`pip install awsebcli --upgrade`
> This might upgrade libraries from the OS that you prefer not to, so you could use --user

1. <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html> to ElasticBeanstalk
1. <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-install-advanced.html>
1. export PATH=$PATH:~/.local/bin
1. Optionally add this to ~/.bashrc , e.g. `echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc`

*hopefully <https://github.com/aws/aws-elastic-beanstalk-cli-setup> listing all the dependencies can help if there are any issues*

*(deprecated) Read about how to use the CLI <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-api-cli.html>*


## AWS account credentials to generate a CLI security file

There is the usual best practice of creating an IAM user *(e.g. ebdemo)* with a group that has the "AWSElasticBeanstalkFullAccess" attached policy...

And with those credentials...

`vim ~/.ssh/awscli`

    AWSAccessKeyId=Write your AWS access ID
    AWSSecretKey=Write your AWS secret key

`chmod 600 ~/.ssh/awscli`
`export AWS_CREDENTIAL_FILE=~/.ssh/awscli`


Or alternatively use the usual AWS CLI: `aws configure` *which puts things in ~/.aws/credentials*

## Initial directory and dependency setup

    mkdir ebjohnexample
    cd ebjohnexample
    virtualenv venv --python python3.6
    source venv/bin/activate
    pip install flask==1.1.1
    pip freeze > requirements.txt
    vim application.py

### A tiny flask python webapp
*application.py*

    :::python3
    from flask import Flask
    
    application = Flask(__name__)
    
    @application.route("/")
    def hello():
        return "hi"
    
    if __name__ == "__main__":
        application.run()


`python application.py`

    Serving Flask app "application" (lazy loading)
    Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    Debug mode: off
    Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

`curl 127.0.0.1:5000`

- <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-flask.html>
- <https://pypi.org/project/Flask/>

## Creating an Elastic Beanstalk Project

While Java and .jar files are probably the obvious example I preferred to do this in python =)

*The pricing/charges are "only" for the underlying resources, so at first an EC2 instance plus a load balancer...*


`echo "venv" > .ebignore ; cat .ebignore`
> ensure elastic beanstalk ignores the local dev dependencies

`eb init -p python-3.6 ebjohnexample --region us-east-1`
> creates a python3.6 elastic beanstalk application named "ebjohnexample"

*Ignoring setting up SSH since we really ought to never SSH into application servers , 12factor and all that*

<https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb3-init.html>

`eb create development`
> This command can take around 5 minutes to create all the resources

    Creating application version archive "app-191020_203345".
    Uploading ebjohnexample/app-191020_203345.zip to S3. This may take a while.
    Upload Complete.
    Environment details for: development
      Application name: ebjohnexample
      Region: us-east-1
      Deployed Version: app-191020_203345
      Environment ID: e-zqag8vpi2p
      Platform: arn:aws:elasticbeanstalk:us-east-1::platform/Python 3.6 running on 64bit Amazon Linux/2.9.3
      Tier: WebServer-Standard-1.0
      CNAME: UNKNOWN
      Updated: 2019-10-21 03:33:48.839000+00:00
    
        Printing Status:
    2019-10-21 03:33:47    INFO    createEnvironment is starting.
    2019-10-21 03:33:49    INFO    Using elasticbeanstalk-us-east-1-538676797434 as Amazon S3 storage bucket for environment data.
    2019-10-21 03:34:15    INFO    Created load balancer named: awseb-e-z-AWSEBLoa-1LEU58ECO2D9O
    2019-10-21 03:34:16    INFO    Created security group named: awseb-e-zqag8vpi2p-stack-AWSEBSecurityGroup-HFU5QRINE35V
    2019-10-21 03:34:31    INFO    Created Auto Scaling launch configuration named: awseb-e-zqag8vpi2p-stack-AWSEBAutoScalingLaunchConfiguration-1WRM6IN89BH24
    2019-10-21 03:36:04    INFO    Created Auto Scaling group named: awseb-e-zqag8vpi2p-stack-AWSEBAutoScalingGroup-10LS20VBXQLOU
    2019-10-21 03:36:04    INFO    Waiting for EC2 instances to launch. This may take a few minutes.
    2019-10-21 03:36:20    INFO    Created Auto Scaling group policy named: arn:aws:autoscaling:us-east-1:538676797434:scalingPolicy:a0d4a40a-5060-406b-b3df-8ed43f8834d1:autoScalingGroupName/awseb-e-zqag8vpi2p-stack-AWSEBAutoScalingGroup-10LS20VBXQLOU:policyName/awseb-e-zqag8vpi2p-stack-AWSEBAutoScalingScaleUpPolicy-AQUPYQ179IYF
    2019-10-21 03:36:20    INFO    Created Auto Scaling group policy named: arn:aws:autoscaling:us-east-1:538676797434:scalingPolicy:59cd3027-4bca-42a8-8feb-fe342e5b786a:autoScalingGroupName/awseb-e-zqag8vpi2p-stack-AWSEBAutoScalingGroup-10LS20VBXQLOU:policyName/awseb-e-zqag8vpi2p-stack-AWSEBAutoScalingScaleDownPolicy-CMAG2FZD4Y0B
    2019-10-21 03:36:20    INFO    Created CloudWatch alarm named: awseb-e-zqag8vpi2p-stack-AWSEBCloudwatchAlarmLow-HWA2PL3FJCDQ
    2019-10-21 03:36:20    INFO    Created CloudWatch alarm named: awseb-e-zqag8vpi2p-stack-AWSEBCloudwatchAlarmHigh-14EGWT2CXU238
    2019-10-21 03:37:10    INFO    Application available at development.xyxifvqn9z.us-east-1.elasticbeanstalk.com.
    2019-10-21 03:37:10    INFO    Successfully launched environment: development
    

> Creates an "environment" (because we like to separate Dev, Test, and Production ... which means auto creating an S3 bucket, Elastic IP, and security group, etc.

You can examine the application in the WebUI:

By using AWS Web Console -> Services -> Elastic Beanstalk -> "development" , to see configuration/status

https://console.aws.amazon.com/elasticbeanstalk/home?region=us-east-1#/launchEnvironment?applicationName=ebjohnexample&environmentId=e-zqag8vpi2p


`curl development.xyxifvqn9z.us-east-1.elasticbeanstalk.com`


`eb status --verbose`
> Verify the Status and Health

    Environment details for: development
      Application name: ebjohnexample
      Region: us-east-1
      Deployed Version: app-191020_203345
      Environment ID: e-zqag8vpi2p
      Platform: arn:aws:elasticbeanstalk:us-east-1::platform/Python 3.6 running on 64bit Amazon Linux/2.9.3
      Tier: WebServer-Standard-1.0
      CNAME: development.xyxifvqn9z.us-east-1.elasticbeanstalk.com
      Updated: 2019-10-21 03:37:10.841000+00:00
      Status: Ready
      Health: Green
      Running instances: 1
          i-0365b4a823823ef5c: InService

*Since this was written AWS have created CodeCommit and Deploy for source control and deployment pipelines so even simpler (tighter) integration with Amazon*

### Alternatively using the AWS Console UI

<https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/GettingStarted.CreateApp.html>

### Cleanup and Pricing

`eb terminate development`
> terminate all instances, load balancers, etc. and delete the app from S3 entirely (since s3 costs money too)

*Probably having a better name than just development might make it clearer if there are multiple applications in EB*

Clearly there is very little operational management required: developers have AWS infrastructure at their fingertips.

The EC2 instances *charged per hour cough-cough* costs depend on what sizing you use, t2.micro for a low traffic demo project is near nothing...

But the load balancer at around $.02 an hour comes out to about 50 cents a day or *at least ~$15 a month* even if your application is doing nothing.

<https://aws.amazon.com/elasticloadbalancing/pricing/>

- - -
### Logs

AWS Web Console -> Deployment -> Elastic Beanstalk -> App Name -> Logs

Snapshot Logs -> View Log File

> notice that ElasticBeanstalk leverages CloudFormation under the hood
> /opt/elasticbeanstalk/hooks/preinit/03wsgiuser.s
> also uses virtualenv and pip

- - -
## Credentials via Environment Variables

Environment Variables help keep configuration out of your code (e.g. access keys/passwords)

`mkdir .ebextensions`
`vi .ebextensions/01.config`
> configs are read and run sequentially

BUT oddly enough .config files in ElasticBeanstalk actually need to be committed to the repo (security fail!)

<https://stackoverflow.com/questions/14206760/how-to-set-an-environment-variable-in-amazon-elastic-beanstalk-python>

> override these placeholders with actual secret values,

> AWS Web Console -> Deployment -> Elastic Beanstalk -> App Name -> Configuration -> Software Configuration (Gear Symbol)

     option_settings:
      - option_name: PARAM1
        value: placeholder



## More info

- <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.ec2.html>
- <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/configuring-https.html> to have your *own domain and SSL*
- <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.managing.elb.html>

**container_commands**
<https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python_django.html>

<https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_Python_custom_container.html>
<https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/customize-containers-ec2.html>

**Docker**
<https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create_deploy_docker_eb.html>
