Title: Amazon SES on EC2 free tier to search for a kitteh!
Date: 2011-02-28 00:07
Tags: AWS, EC2, SES, cron

[TOC]

### Mission: hourly poll of a website

...to find out if the Kitteh is available for adoption and immediate email notification if Kitteh is found.

Estimated time to complete: between 15 minutes and hours (depending on setting up your EC2 instance, SES service, etc.)

Skills: Amazon EC2 setup, SSH, centos yum, bash, wget, cronjob


### Amazon Free services tier

If you have an Amazon EC2 instance running (e.g. EC2 Linux Micro Instance in Free Tier = centos!)

(And you're not running over the GET/POST upload/download free tier bandwidths)

(If you don't know how to setup a quick Amazon Linux Micro Instance in the free tier search this blog for more info)

1. Sign up for SES (then receive a verification email for your Amazon AWS Account)
1. Account Security Credentials (for AWS access identifiers)  
1. Use nano or vi to create a file "aws-credentials" (Amazon's sample below)
        
        AWSAccessKeyId=022QF06E7MXBSH9DHM
        AWSSecretKey=kWcrlUX5JEDGM/LtmEENI/aVmYvHNif5zB+d9+

1. Download the example perl scripts via: <http://aws.amazon.com/code/Amazon-SES>
        
        wget http://aws-catalog-download-files.s3.amazonaws.com/AmazonSES-2011-02-02.zip
        unzip AmazonSES-2011-02-02.zip
        chmod +x /home/ec2-user/*.pl
        /home/ec2-user/bin/ses-verify-email-address.pl -k aws-credentials -v youreemail@example.com
    
### Amazon EC2 Missing some perl

    "Can't locate XML/LibXML.pm in @INC (@INC contains:

    /usr/local/lib64/perl5
    /usr/local/share/perl5       
    /usr/local/share/perl5 
    /usr/lib64/perl5   
    /usr/share/perl5
    /usr/share/perl5
    /usr/lib64/perl5
    /usr/share/perl5
    /usr/local/lib64/perl5/site_perl/5.10.0/x86_64-linux-thread-multi

    /usr/local/lib/perl5/site_perl/5.10.0
    /usr/lib64/perl5/vendor_perl/5.10.0/x86_64-linux-thread-multi
    /usr/lib/perl5/vendor_perl
    /usr/lib/perl5/site_perl .) at ./ses-verify-email-address.pl line 26.

    BEGIN failed--compilation aborted at ./ses-verify-email-address.pl line 26."

THANKS AMAZON! Using their preconfigured Instance means they don't have all of the Perl packages installed...

1. `sudo yum install perl-XML-LibXML perl-digest-SHA`
1. `sudo yum provides */SHA.pm`
>tells me what other packages I might have missed...
1. `sudo yum search perl-Digest`
1. `sudo yum install perl-Digest-SHA`
>What a difference a D versus d makes!
1. *sudo yum perl-libxml-perl libxml2-devel perl-IO-Socket-SSL libxslt-devel ?*
1. Debian: `sudo apt-get install libio-socket-ssl-perl libxml-libxml-perl`
1. `tail /var/log/maillog` for troubleshooting sendmail...

### Verify an SES linked email address by running the perl script

`/home/ec2-user/bin/ses-verify-email-address.pl -k aws-credentials -v youreemail@example.com`

Use the email account you gave above for verification and click on the link...  

> You have successfully verified an email address with Amazon Simple Email Service.

- - -

    ~/amazonses/bin/ses-send-email.pl -k ~/amazonses/bin/aws-credentials -s "Test AWS" -f youremail@example.com youremail@example.com,secondemail@example.com < ~/kittysearch/result.txt

### Search.sh

    :::bash
    #/bin/bash
    wget -O ~/kittysearch/page1.htm 'http://adopt.hssv.org/search/searchResults.asp?task=search&searchid=&advanced=&s=adoption&animalType=2%2C15&statusID=3&state=&regionID=&submitbtn=Find+Animals'
    wget -O ~/kittysearch/page2.htm 'http://adopt.hssv.org/search/searchResults.asp?tpage=2&task=search&searchid=&advanced=&s=&animalType=2,15&statusID=3&state=&regionID=&submitbtn=Find+Animals'
    wget -O ~/kittysearch/page3.htm 'http://adopt.hssv.org/search/searchResults.asp?tpage=3&task=search&searchid=&advanced=&s=&animalType=2,15&statusID=3&state=&regionID=&submitbtn=Find+Animals'
    grep -i "bandit" ~/kittysearch/page1.htm ~/kittysearch/page2.htm ~/kittysearch/page3.htm > ~/kittysearch/result.txt
    
    if [ -s ~/kittysearch/result.txt ]; then
        # must move to the directory to use the SES.pm
        cd ~/amazonses/bin
        ./ses-send-email.pl -k ~/amazonses/bin/aws-credentials -s "Test AWS" -f myemail@domain.com myemail@domain.com,secondrecipient@domain.com < ~/kittysearch/result.txt
    fi
    # http://docs.amazonwebservices.com/ses/latest/DeveloperGuide/ for full details about email.pl
        

### Trigger the search with cron

`crontab -e`
> i key to enter input in vi

    55 * * * * /home/ec2-user/kittysearch/kittysearch.sh

> escape key gets : then x to save and quit

### Troubleshooting "Cannot locate SES.pm"
Running the script from a different directory or CRON gets the error: "Can't locate SES.pm in @INC"

    cp /home/ec2-user/amazonses/bin/SES.pm /home/ec2-user/kittysearch

> FIXED! must move to the directory in the script using cd first to have access to SES.pm

### SES Message Limit

Yyou can send 2,000 messages for free each day when you call Amazon SES from an Amazon EC2
instance directly or through AWS Elastic Beanstalk. (Note bandwidth charges may still apply)

### More info
Apparently since 2011 there has come along infrastructure like page2rss and ifttt that makes these kind of custom solutions less helpful (unless you need customization!)
