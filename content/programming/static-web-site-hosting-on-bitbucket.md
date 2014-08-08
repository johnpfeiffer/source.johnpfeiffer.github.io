Title: Creating a static web site with Bitbucket
Date: 2014-06-30 20:20
Tags: programming
Author: John Pfeiffer
Summary: How to host a static web site on Bitbucket for free

1. create a bitbucket account with username
1. create a repo named username.bitbucket.org
1. mkdir username.bitbucket.org
1. cd username.bitbucket.org
1. echo "hi" > index.html
1. git init .
1. git add
1. git commit -m "first site index"
1. git remote add origin git@bitbucket.org:username/username.bitbucket.org.git
1. git push origin master
1. git branch --set-upstream master origin/master
1. git pull
1. https://username.bitbucket.org

<https://confluence.atlassian.com/display/BITBUCKET/Publishing+a+Website+on+Bitbucket>

Scroll down to the comments:
*You can setup a CNAME for your account .  You cannot set up a CNAME for a static website hosted on Bitbucket.  The account you setup a CNAME for may have a repository that represents a static website.*
