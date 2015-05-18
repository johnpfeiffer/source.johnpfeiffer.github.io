Title: Dupal Security Tip: disabling anonymous access to cron
Date: 2010-08-30 17:33
Author: John Pfeiffer
Slug: dupal-security-tip-disabling-anonymous-access-to-cron

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Drupal is a wonderful way of leveraging many open source advanced web
features into one interface that conceivably can be handed off to a "non
developer" to maintain.

</p>

Along with all of the installation / implementation (often customized to
fit the customers' needs) there are two further things that should be
considered, Security and Useability.

</p>

Here's some tips on security and maintenance:

</p>

Drupal is a Content Management System that allows remote users to run
scripts and access databases on your web server, this is a serious
responsibility as Shared Hosting means your runaway/hacked scripts
affects others, and Hackers/Spammers are always looking for new
Zombies...

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -  

Restrict the PHP scripts access from ANONYMOUS USERS ON THE INTERNET

</p>

"index.php" should be allowed (it's your home page) but...

</p>

\*Cron is the method in linux to run scheduled tasks.

</p>

Drupal requires regular scheduled actions for maintenance (e.g. update
content in search,  

cleaning up log files, checking for updates, etc.)

</p>

[http://drupal.org/cron.php][] is not accessible but  
[http://yourdomain.com/cron.php][] may be accessible to ANYONE (as
that's the default install).

</p>

To secure the cron.php file in .htacess, you have to do that manually
after installation:

</p>

To block remote access to cron.php, in the server's .htaccess file or
vhost configuration file:

</p>

Order Deny,Allow  

Deny from all  

Allow from localhost  

Allow from 127.0.0.1  

Allow from xx.xx.xx.xx <-- your remote IP address

</p>

Or protect update.php too in the .htaccess file:

</p>

order deny,allow  

deny from all  

allow from 127.0.0  

\# add allowed remote IP addresses  

allow from a.b.c.d  

allow from a.b.c.d

</p>

NOW ANONYMOUS ACCESS TO CRON.PHP should return either "access denied" or
"page not found"...

</p>

You can still run cron manually from either of the options below:  

Administer -\> Reports -\> Status

</p>

[http://domain.com/admin/reports/status/run-cron][]

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -  

Cpanel -\> Advanced -\> Cron Jobs

</p>

\* \* \* \* \* [http://domain.com/cron.php][]

</p>

(e.g. for rochen or bluehost cpanelx command should be the 8 char
directory)

</p>

php -q /home/yoursite/public\_html/cron.php

</p>

OR if you have multiple subdomains running different drupal installs:  

php -q /home/8chars/public\_html/subdomain/cron.php

</p>

Check using your drupal admin to ensure that the cron job has run  

Administer -\> Reports -\> Status

</p>

This will allow you to test if your cpanel really has the correct
permissions as  

Administer -\> Reports -\> Status should now show the cron job status as
updated frequently! =)

</p>

Here is a diagram of the general crontab syntax, for illustration:

</p>

\# +---------------- minute (0 - 59)  

\# | +------------- hour (0 - 23)  

\# | | +---------- day of month (1 - 31)  

\# | | | +------- month (1 - 12)  

\# | | | | +---- day of week (0 - 7) (Sunday=0 or 7)  

\# | | | | |  

\* \* \* \* \* command to be executed

</p>

e.g. 2 13 28 12 \* /bin/execute/this/script.sh

</p>

the five stars (with a space in between each!) represent wildcards:

</p>

\1. when minute = 2  

\2. when hour = 13  

\3. when day = 28  

\4. when month = 12  

\5. every day (could be = 5 for every friday)

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -  

/sites/default/settings.php should definitely have:

</p>

$update\_free\_access = FALSE;

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -  

Administer \> Site configuration \> File uploads  

"Default permitted file extensions field" for each role should be
limited, because obviously you don't want ANONYMOUS users uploading .php
files! (Or in INPUT FORMAT, .php code entered by an anonymous or hacked
authenticated user!)

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Drupal][]

</div>
</p>

  [http://drupal.org/cron.php]: http://drupal.org/cron.php
  [http://yourdomain.com/cron.php]: http://yourdomain.com/cron.php
  [http://domain.com/admin/reports/status/run-cron]: http://domain.com/admin/reports/status/run-cron
  [http://domain.com/cron.php]: http://domain.com/cron.php
  [Drupal]: http://john-pfeiffer.com/category/tags/drupal
