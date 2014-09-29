Title: Amazon SES on EC2 free tier to search for a kitteh!
Date: 2011-02-28 00:07
Slug: content/amazon-ses-on-ec2-free-tier-to-search-for-a-kitteh
Tags: AWS, EC2, SES, cron


[TOC]

### Mission: hourly poll of a website

...to find out if the Kitteh is available for adoption and immediate email notification if Kitteh is found.

Estimated time to complete: between 15 minutes and hours (depending on
setting up your EC2 instance, SES service, etc.)

Skills: Amazon EC2 setup, SSH, centos yum, bash, wget, cronjob


### Amazon Free services tier

If you have an Amazon EC2 instance running (e.g. EC2 Linux Micro
Instance in Free Tier = centos!)  

(And you're not running over the GET/POST upload/download free tier
bandwidths)

(If you don't know how to setup a quick Amazon Linux Micro Instance in
the free tier search this blog for more info)

Sign up for SES (then receive a verification email for your Amazon AWS Account)  

Account Security Credentials (for AWS access identifiers)  

Use nano or vi to create a file "aws-credentials" (Amazon's sample
below)

        AWSAccessKeyId=022QF06E7MXBSH9DHM  
            AWSSecretKey=kWcrlUX5JEDGM/LtmEENI/aVmYvHNif5zB+d9+

Download the example perl scripts via:
<http://aws.amazon.com/code/Amazon-SES>

`wget
<http://aws-catalog-download-files.s3.amazonaws.com/AmazonSES-2011-02-02.zip>`

`unzip AmazonSES-2011-02-02.zip`

`chmod +x /home/ec2-user/*.pl`

`/home/ec2-user/bin/ses-verify-email-address.pl -k aws-credentials -v
[youreemail@domain.com]`

- - -
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

`sudo yum install perl-XML-LibXML perl-digest-SHA`

`sudo yum provides */SHA.pm`

>tells me what other packages I might have missed...

`sudo yum search perl-Digest`

`sudo yum install perl-Digest-SHA`
>What a difference a D versus d makes!

*sudo yum perl-libxml-perl libxml2-devel perl-IO-Socket-SSL libxslt-devel ?*

Debian: `sudo apt-get install libio-socket-ssl-perl libxml-libxml-perl`

`tail /var/log/maillog` for troubleshooting sendmail...

- - -  

`/home/ec2-user/bin/ses-verify-email-address.pl -k aws-credentials -v
youreemail@domain.com`

use the email account you gave above for verification and click on the
link...  

You have successfully verified an email address with Amazon Simple Email Service.

- - -

\~/amazonses/bin/ses-send-email.pl -k \~/amazonses/bin/aws-credentials
-s "Test AWS" -f [youremail@domain.com][]
[youremail@domain.com][],[secondemail@domain.com][] <
\~/kittysearch/result.txt

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - -  

\#/bin/bash

</p>

wget -O \~/kittysearch/page1.htm
'[http://adopt.hssv.org/search/searchResults.asp?task=search&searchid=&adv...][]'

</p>

wget -O \~/kittysearch/page2.htm
'[http://adopt.hssv.org/search/searchResults.asp?tpage=2&task=search&searc...][]'

</p>

wget -O \~/kittysearch/page3.htm
'[http://adopt.hssv.org/search/searchResults.asp?tpage=3&task=search&searc...][]'

</p>

grep -i "bandit" \~/kittysearch/page1.htm \~/kittysearch/page2.htm
\~/kittysearch/page3.htm \> \~/kittysearch/result.txt

</p>

if [ -s \~/kittysearch/result.txt ] then

</p>

\# must move to the directory to use the SES.pm  

cd \~/amazonses/bin

</p>

./ses-send-email.pl -k \~/amazonses/bin/aws-credentials -s "Test AWS" -f
[myemail@domain.com][]
[myemail@domain.com][],[secondrecipient@domain.com][] <
\~/kittysearch/result.txt

</p>

fi

</p>

\# [http://docs.amazonwebservices.com/ses/latest/DeveloperGuide/][] for
full details about email.pl

</p>

- - -

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
~/amazonses/bin/ses-send-email.pl -k ~/amazonses/bin/aws-credentials -s "Test AWS" -f youremail@domain.com youremail@domain.com,secondemail@domain.com < ~/kittysearch/result.txt

### Search.sh

    #/bin/bash
    
    wget -O ~/kittysearch/page1.htm 'http://adopt.hssv.org/search/searchResults.asp?task=search&searchid=&adv...'
    
    wget -O ~/kittysearch/page2.htm 'http://adopt.hssv.org/search/searchResults.asp?tpage=2&task=search&searc...'
    
    wget -O ~/kittysearch/page3.htm 'http://adopt.hssv.org/search/searchResults.asp?tpage=3&task=search&searc...'

    grep -i "bandit" ~/kittysearch/page1.htm ~/kittysearch/page2.htm ~/kittysearch/page3.htm > ~/kittysearch/result.txt

    if [ -s ~/kittysearch/result.txt ]; then

# must move to the directory to use the SES.pm
cd ~/amazonses/bin

./ses-send-email.pl -k ~/amazonses/bin/aws-credentials -s "Test AWS" -f myemail@domain.com myemail@domain.com,secondrecipient@domain.com < ~/kittysearch/result.txt

fi

# http://docs.amazonwebservices.com/ses/latest/DeveloperGuide/ for full details about email.pl

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
crontab -e
(i key to enter input in vi)
55 * * * * /home/ec2-user/kittysearch/kittysearch.sh
(escape key gets : then x to save and quit)

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Running the script from a different directory or CRON gets the error: "Can't locate SES.pm in @INC"

cp /home/ec2-user/amazonses/bin/SES.pm /home/ec2-user/kittysearch

FIXED! # must move to the directory in the script using cd first to have access to SES.pm

- - -

< you can send 2,000 messages for free each day when you call Amazon SES from an Amazon EC2
instance directly or through AWS Elastic Beanstalk. (Note bandwidth charges may still apply)

    <http://kittyandbear.net/john/virtualization/amazon-aws-free-tier-linux-web-server.txt>
  <http://aws.amazon.com/code/Amazon-SES>

<http://aws-catalog-download-files.s3.amazonaws.com/AmazonSES-2011-02-02.zip>

  [youreemail@domain.com]: mailto:youreemail@domain.com
  [youremail@domain.com]: mailto:youremail@domain.com
  [secondemail@domain.com]: mailto:secondemail@domain.com
  
    <http://adopt.hssv.org/search/searchResults.asp?task=search&searchid=&advanced=&s=adoption&animalType=2%2C15&statusID=3&state=&regionID=&submitbtn=Find+Animals>
    <http://adopt.hssv.org/search/searchResults.asp?tpage=2&task=search&searchid=&advanced=&s=&animalType=2,15&statusID=3&state=&regionID=&submitbtn=Find+Animals>

    <http://adopt.hssv.org/search/searchResults.asp?tpage=3&task=search&searchid=&advanced=&s=&animalType=2,15&statusID=3&state=&regionID=&submitbtn=Find+Animals>

### more info
Apparently since 2011 there has come along infrastructure like page2rss and ifttt that makes these kind of custom solutions less helpful (unless you need customization!)
