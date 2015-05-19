Title: Drupal Security Tip: disabling anonymous access to cron
Date: 2010-08-30 17:33
Tags: Drupal, security

[TOC]

Drupal is a wonderful way of leveraging many open source advanced web features into one interface that conceivably can be handed off to a "non developer" to maintain.

Along with all of the installation / implementation (often customized to fit the customers' needs) there are two further things that should be considered, Security and Useability.

Here's some tips on security and maintenance.

Drupal is a Content Management System that allows remote users to run scripts and access databases on your web server, this is a **serious responsibility** as Shared Hosting means your runaway/hacked scripts affects others, and Hackers/Spammers are always looking for new Zombies...

### Restrict access to PHP Scripts

Restrict the PHP scripts access from ANONYMOUS USERS ON THE INTERNET!

"index.php" should be allowed (it's your home page) but...

> Cron is the method in linux to run scheduled tasks.

Drupal requires regular scheduled actions for maintenance (e.g. update content in search, cleaning up log files, checking for updates, etc.)

<http://drupal.org/cron.php> (should not be) accessible but <http://example.com/cron.php> may be accessible to ANYONE as that's the default install =( 

To secure the cron.php file in .htacess, you have to do lock it down manually after installation.

To block remote access to cron.php, in the server's .htaccess file or vhost configuration file:

**.htaccess**

    Order Deny,Allow
    Deny from all
    Allow from localhost
    Allow from 127.0.0.1
    Allow from xx.xx.xx.xx <-- your remote IP address

Or protect update.php too in the .htaccess file:

    order deny,allow
    deny from all
    allow from 127.0.0
    # add allowed specific remote IP addresses
    allow from a.b.c.d
    allow from a.b.c.d

NOW ANONYMOUS ACCESS TO CRON.PHP should return either "access denied" or "page not found"...

### Running Drupal cron manually

You can still run cron manually from either of the options below:  

Administer -> Reports -> Status

**http://example.com/admin/reports/status/run-cron**

There's even a way to schedule it to run against localhost or 127.0.0.1 (which is trusted in the .htaccess file we created above)

### Cron explained

**Cpanel -> Advanced -> Cron Jobs**

    * * * * * http://example.com/cron.php

(e.g. for rochen or bluehost cpanelx command should be the 8 char directory)

    php -q /home/yoursite/public_html/cron.php

OR if you have multiple subdomains running different drupal installs:

    php -q /home/8chars/public_html/subdomain/cron.php

Check using your drupal admin to ensure that the cron job has run

**Administer -> Reports -> Status**

This will allow you to test if your cpanel really has the correct permissions as

Administer -> Reports -> Status should now show the cron job status as updated frequently! =)

Here is a diagram of the general crontab syntax, for illustration:

    # +---------------- minute (0 - 59)
    # | +------------- hour (0 - 23)
    # | | +---------- day of month (1 - 31)
    # | | | +------- month (1 - 12)
    # | | | | +---- day of week (0 - 7) (Sunday=0 or 7)
    # | | | | |

    * * * * * command to be executed

> e.g. 59 23 31 12 * /bin/execute/this/script.sh

the five stars (with a space in between each!) represent wildcards:

1. when minute = 59
2. when hour = 23
3. when day = 31
4. when month = 12
5. every day (could be = 5 to limit it to only every friday)


### Update free access = FALSE

/sites/default/settings.php should definitely have:

$update_free_access = FALSE;


### Restricting file upload extensions

Administer -> Site configuration -> File uploads  

"Default permitted file extensions field" for each role should be limited, because obviously you don't want ANONYMOUS users uploading .php files! 

(Or in INPUT FORMAT, .php code entered by an anonymous or hacked authenticated user!)
