Title: Drupal with Docker Compose and nginx and php-fpm and mariadb
Date: 2016-07-28 23:59
Tags: docker, docker-compose, digitalocean, packer, drupal, php, nginx

[TOC]

## Replacing: cherokee webserver, php-cgi, MySQL

In my professional life I've seen the webserver front end default choice shift from Apache to NGINX occur for production services.

Nginx is compelling due to simpler configuration and improved performance so I suspect the existing preponderance of Apache deployments are because "if it ain't broke don't fix it" (which makes lots of sense in Operations) along with the large number of Ops/SysAdmins who already know how to configure and integrate Apache (which makes a lot of sense to Management).

<https://www.nginx.com/blog/nginx-vs-apache-our-view/>

For a personal project I experimented with and chose Cherokee web server (<http://cherokee-project.com/>) because it offered good performance and a simpler setup (Web UI even!)

Unfortunately as the project Dev and adoption slowed it seemed to make a lot of sense to finally convert my personal project to nginx. <https://github.com/cherokee/webserver/commits/master>

I also wanted to experiment with a Docker based infrastructure (with docker-compose and a single YAML config file, ideally leveraging as much as possible the many official upstream docker images (<https://hub.docker.com/explore/>))

Benefits:

- this would isolate my app from the Host OS (increased portability)
- allow for simpler component swapping or upgrades (with testing and rollback and even local Dev)
- leave room for adding other isolated components

## Almost able to leverage everything right out of the box

I spent time researching nginx and php-fpm and created a minimal config that worked (two docker commands) based on the slimmer alpine linux docker images. <https://blog.john-pfeiffer.com/nginx-with-docker/>

This wasn't quite far off from the official Drupal Dockerfile except there are some more OS dependencies like GD and XML so I instead opted to use the official Drupal Docker image. (Non alpine linux so larger size but they've done the work of packaging the complexity and by not customizing it will be easier to update in the future - and avoid a Docker Build entirely!)

### docker-compose.yml for nginx and drupal:7-fpm and mariadb:5.5

    # https://docs.docker.com/compose/compose-file/
    # https://docs.docker.com/compose/environment-variables/
    # https://www.nginx.com/resources/wiki/start/topics/recipes/drupal
    
    nginx:
      image: nginx:alpine
      ports:
        - "80:80"
      volumes:
        - ./nginx.conf:/etc/nginx/nginx.conf:ro
        - ./default.conf:/etc/nginx/conf.d/default.conf:ro
        - /var/www/html:/var/www/html/
      links:
        - fpm
    
    # https://hub.docker.com/_/drupal/
    fpm:
      image: drupal:7-fpm
      ports:
        - "9000:9000"
      volumes:
        - /var/www/html:/var/www/html/
      links:
        - mysql
    
    # https://hub.docker.com/_/mariadb/
    mysql:
      image: mariadb:5.5
      ports:
        - "3306:3306"
      environment:
        - MYSQL_ROOT_PASSWORD
        - MYSQL_USER
        - MYSQL_PASSWORD
        - MYSQL_DATABASE


Adding the MariaDB (compatible with MySQL) image/container was fairly straightforward (just reading the docs on how to override and setup the default user and DB via Environment Variables)

> I am ok with the Database files being kept completely inside of a persistent container.  I expect to do regular backups (mysqldump and scp) and may also spend the money to just use DigitalOcean's backup service (no poweroff required!)

### And the bugs

I discovered a bug where the css/themes didn't render correctly.  As part of the troubleshooting I installed nginx, php, and MySQL locally on the host with my override configs (no bug exhibited).  I then replaced each "native host installed service" with the Docker one, working from the backend DB forward I was able to identify the issue.

Unfortunately the nginx image uses a default user of "nginx" whereas the drupal:php image uses "www-data" which caused issues when accessing the Drupal source files (which I was sharing via --volume on the host, preferring to eschew a "data container").

My personal Linux maxim still holds true: "If there's a problem with something running in Linux it's probably a Permissions issue". ;)

### Do not add complexity

I avoided creating my own docker image build FROM drupal:php with nginx included because:

- simplest with as few build steps possible
- contrary to the "do one thing well" principle
- contrary to the "one container one app" Docker principle
- tight coupling of nginx and php would make it harder to update one or the other independently

### Cache your upstream dependencies

Ironically I also ended up providing my own drupal.tar.gz downloaded from Drupal.org but cached in Bitbucket as the upstream ftp.drupal.org proved unreliable.

## The pragmatic solution

Instead, as I was already using packer on DigitalOcean to automate building the Host and uploading the custom configs, docker-compose.yaml, and Drupal source, I added a few steps to install nginx directly to the Host OS.

### packer.json

    NEWUSER_NAME=username NEWUSER_PASSWORD=yourpassword DIGITALOCEAN_API_TOKEN=yourapitoken /opt/packer build packer.json
> A few files and a single command (packer is just a single binary downloaded from hashicorp) I can have another Docker based Drupal host ready (awyeah)


    {
      "_comment": "https://www.packer.io/docs/builders/digitalocean.html",
      "variables": {
        "digitalocean_api_token": "{{env `DIGITALOCEAN_API_TOKEN`}}",
        "newuser_name": "{{env `NEWUSER_NAME`}}",
        "newuser_password": "{{env `NEWUSER_PASSWORD`}}"
      },
    
      "builders": [{
        "type": "digitalocean",
        "api_token": "{{user `digitalocean_api_token`}}",
        "size": "512mb",
        "region": "lon1",
        "image": "ubuntu-16-04-x64",
        "droplet_name": "drupal-from-packer-{{timestamp}}",
        "snapshot_name": "drupal-from-packer-{{isotime \"2006.01.02.030405\"}}"
      }],
    
      "provisioners": [
        {
          "type": "shell",
          "inline": [
            "ip a",
            "curl -s http://checkip.amazonaws.com",
            "apt-get update",
            "sudo apt-get install -y vim curl wget byobu ntp tar gzip",
            "timedatectl set-timezone Etc/UTC",
            "cat /etc/timezone",
            "date",
            "useradd -s /bin/bash -m {{user `newuser_name`}}",
            "usermod -a -G admin {{user `newuser_name`}}",
            "echo '{{user `newuser_name`}}:{{user `newuser_password`}}'|chpasswd",
            "cat /etc/passwd",
            "sed -i 's/Port 22/Port 2222/g' /etc/ssh/sshd_config",
            "sed -i 's/PermitRootLogin yes/PermitRootLogin no/g' /etc/ssh/sshd_config",
            "echo 'PasswordAuthentication no' >> /etc/ssh/sshd_config",
            "cat /etc/ssh/sshd_config",
            "mkdir -p /home/{{user `newuser_name`}}/.ssh",
            "fallocate -l 1G /swapfile",
            "chmod 600 /swapfile",
            "mkswap /swapfile",
            "swapon /swapfile",
            "swapon --show",
            "free -h",
            "echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab",
            "echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf",
            "echo 'vm.vfs_cache_pressure=50' | sudo tee -a /etc/sysctl.conf"
          ]
        },
        {
          "type": "file",
          "source": "authorized_keys",
          "destination": "/home/{{user `newuser_name`}}/.ssh/authorized_keys"
        },
        {
          "type": "shell",
          "script": "install-docker.sh"
        },
        {
          "type": "file",
          "source": "docker-compose.yml",
          "destination": "/home/{{user `newuser_name`}}/docker-compose.yml"
        },
        {
          "type": "shell",
          "inline": [
            "mkdir -p /var/www/html",
            "wget https://bitbucket.org/yourusername/yourrepository/raw/97360be2edd53b93149d750db24f749aebc27988/binaries/drupal-7.50.tar.gz",
            "tar xf drupal-7.50.tar.gz --strip-components=1 -C /var/www/html",
            "ls -ahl /var/www/html",
            "mkdir -p /var/www/html/sites/default/files",
            "chmod 777 /var/www/html/sites/default/files",
            "cp -a /var/www/html/sites/default/default.settings.php /var/www/html/sites/default/settings.php",
            "chmod 777 /var/www/html/sites/default/settings.php"
          ]
        },
        {
          "type": "shell",
          "inline": [
            "apt-get install -y nginx"
          ]
        },
        {
          "type": "file",
          "source": "nginx.conf",
          "destination": "/etc/nginx/nginx.conf"
        },
        {
          "type": "file",
          "source": "default.conf",
          "destination": "/etc/nginx/conf.d/default.conf"
        }
    
      ]
    
    }

> HINT: A DigitalOcean 512MB droplet needs swap enabled due to the MySQL/MariaDB memory defaults, otherwise you get strange errors about inode unavailable while starting the MariaDB container

- <https://www.suse.com/documentation/opensuse114/book_tuning/data/cha_tuning_memory_vm.html>
- <https://www.kernel.org/pub/linux/kernel/people/akpm/patches/2.6/2.6.7/2.6.7-mm1/broken-out/vfs-shrinkage-tuning.patch>

- One thing that is annoying is as a single partition it is potentially vulnerable to a /var/log DenialOfService
- A very nice tool to add is fail2ban (apt-get install fail2ban) but I want to ensure I tweak the configs correctly


#### install-docker.sh

    :::bash
    #!/bin/sh
    # ubuntu 16.04 is xenial , https://blog.john-pfeiffer.com/docker-intro-install-run-and-port-forward/
    sudo apt-key adv --keyserver hkp://pgp.mit.edu:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D
    sudo sh -c "echo 'deb https://apt.dockerproject.org/repo ubuntu-xenial main' > /etc/apt/sources.list.d/docker.list"
    sudo apt-get update || exit 1
    sudo apt-get install -y linux-image-extra-$(uname -r) || exit 1
    sudo apt-get install -y docker-engine docker-compose || exit 1
    service docker status || exit 1
    docker info || exit 1
> linux-image-extra is to ensure we have AUFS because docker needs a proper storage driver

An alternative is to download the docker-compose binary directly (to /usr/local/bin):
- <https://github.com/docker/compose/releases> 

`sudo curl -L "https://github.com/docker/compose/releases/download/1.25.4/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
`sudo chmod +x /usr/local/bin/docker-compose`
`which docker-compose ; sudo docker-compose --version`

#### docker-compose.yml with drupal:7-fpm and mariadb:5.5

    :::docker
    # https://hub.docker.com/_/drupal/
    fpm:
      image: drupal:7-fpm
      ports:
        - "127.0.0.1:9000:9000"
    #    - "9000:9000"
      volumes:
        - /var/www/html:/var/www/html/
      links:
        - mysql
    
    # https://hub.docker.com/_/mariadb/
    mysql:
      image: mariadb:5.5
      ports:
        - "3306:3306"
      environment:
        - MYSQL_ROOT_PASSWORD
        - MYSQL_USER
        - MYSQL_PASSWORD
        - MYSQL_DATABASE

> 2 out of 3 ain't bad


#### nginx.conf

    :::nginx
    # slightly modified /etc/nginx/nginx.conf from "apt-get install nginx"
    # https://www.nginx.com/resources/wiki/start/topics/examples/full/
    
    user www-data;
    worker_processes auto;
    pid /run/nginx.pid;
    
    events {
            worker_connections 768;
            # multi_accept on;
    }
    
    http {
    
            sendfile on;
            tcp_nopush on;
            tcp_nodelay on;
            keepalive_timeout 65;
            types_hash_max_size 2048;
            server_tokens off;
    
            include /etc/nginx/mime.types;
            default_type application/octet-stream;
    
            access_log /var/log/nginx/access.log;
            error_log /var/log/nginx/error.log;
    
            gzip on;
            gzip_disable "msie6";
    
            gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;
    
            include /etc/nginx/conf.d/*.conf;
    
    }

#### default.conf

    :::nginx
    server {
        listen      80;
        server_name physicstime.com;
        root /var/www/html; ## <-- Your only path reference.
    
        location = /favicon.ico {
            log_not_found off;
            access_log off;
        }
    
        location = /robots.txt {
            allow all;
            log_not_found off;
            access_log off;
        }
    
        # Very rarely should these ever be accessed outside of your lan
        location ~* \.(txt|log)$ {
            deny all;
        }
    
        location ~ \..*/.*\.php$ {
            return 403;
        }
    
        location ~ ^/sites/.*/private/ {
            return 403;
        }
    
        # Allow "Well-Known URIs" as per RFC 5785
        location ~* ^/.well-known/ {
            allow all;
        }
    
        # Block access to "hidden" files and directories whose names begin with a
        # period. This includes directories used by version control systems such
        # as Subversion or Git to store control files.
        location ~ (^|/)\. {
            return 403;
        }
    
        location / {
            # try_files $uri @rewrite; # For Drupal <= 6
            try_files $uri /index.php?$query_string; # For Drupal >= 7
        }
    
        location @rewrite {
            rewrite ^/(.*)$ /index.php?q=$1;
        }
    
        # Don't allow direct access to PHP files in the vendor directory.
        location ~ /vendor/.*\.php$ {
            deny all;
            return 404;
        }
    
        # In Drupal 8, we must also match new paths where the '.php' appears in
        # the middle, such as update.php/selection. The rule we use is strict,
        # and only allows this pattern with the update.php front controller.
        # This allows legacy path aliases in the form of
        # blog/index.php/legacy-path to continue to route to Drupal nodes. If
        # you do not have any paths like that, then you might prefer to use a
        # laxer rule, such as:
        #   location ~ \.php(/|$) {
        # The laxer rule will continue to work if Drupal uses this new URL
        # pattern with front controllers other than update.php in a future
        # release.
        location ~ '\.php$|^/update.php' {
            fastcgi_split_path_info ^(.+?\.php)(|/.*)$;
            # Security note: If you're running a version of PHP older than the
            # latest 5.3, you should have "cgi.fix_pathinfo = 0;" in php.ini.
            # See http://serverfault.com/q/627903/94922 for details.
            include fastcgi_params;
            # Block httpoxy attacks. See https://httpoxy.org/.
            fastcgi_param HTTP_PROXY "";
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_path_info;
            fastcgi_intercept_errors on;
            # PHP 5 socket location.
            #fastcgi_pass unix:/var/run/php5-fpm.sock;
            # PHP 7 socket location.
            # fastcgi_pass unix:/var/run/php/php7.0-fpm.sock;
    
            fastcgi_pass 127.0.0.1:9000;
            # fastcgi_pass fpm:9000;
        }
    
        # Fighting with Styles? This little gem is amazing.
        # location ~ ^/sites/.*/files/imagecache/ { # For Drupal <= 6
        location ~ ^/sites/.*/files/styles/ { # For Drupal >= 7
            try_files $uri @rewrite;
        }
    
        # Handle private files through Drupal.
        location ~ ^/system/files/ { # For Drupal >= 7
            try_files $uri /index.php?$query_string;
        }

        # prevent hotlinking
        location ~ ^/sites/.*/files/ {
            valid_referers none blocked www.physicstime.com physicstime.com;
            if ($invalid_referer) {
              return 403;
            }
        }
    
        location ~* \.(js|css|png|jpg|jpeg|gif|ico)$ {
            # prevent hotlinking
            valid_referers none blocked www.physicstime.com physicstime.com;
            if ($invalid_referer) {
              return 403;
            }
            expires max;
            log_not_found off;
        }
    
    }

> slightly modified from the wonderful reference provided by nginx, mostly the first 3 lines and later the fastcgi_pass

- <https://www.nginx.com/resources/wiki/start/topics/recipes/drupal/>

## Post boot manual configuration (ohgodwhy)

Post boot of a "fresh from built-by-packer snapshot" there were still the basic steps of configuring Drupal (which I did manually with a browser and install.php though I'm pretty sure I could have just overridden the settings.php directly).

And for this migration project a MySQL dump, SCP of the existing extra modules, and of course the already uploaded user images/files.

I'm sure with more tinkering I can overcome the nginx vs www-data user permissions issue but since I time boxed this project I stuck with this compromise which is still much more improved and automated than my previous setup.

For migrating data there is of course the prerequisite: `mysqldump -uroot -p physicstime > backup.sql`


    vi /var/www/html/themes/bartik/css/style.css
        font-size: 2.929em;
    
    cat /var/www/html/themes/bartik/css/style.css | tr '\n' '\r' | sed -e 's/#site-slogan {\r  font-size: 0.929em/#site-slogan {\r  font-size: 2.929em/' | tr '\r' '\n' > /var/www/html/themes/bartik/css/style.css.updated

> customize increased visibility of the #site-slogan { , occasionally needs cache cleared in admin/config/development/performance
> The oneliner is a complicated way of sed replacing two lines at once (tr replaces newlines with \r temporarily)


    sed -i 's/font-size: 87.5/font-size: 120/' /var/www/html/themes/bartik/css/style.css
> Because the world does not need yet another 10pt font website

    hostnamectl set-hostname physicstime.com
    docker-compose up &

> Hint: `/etc/hosts` locally and use a browser to do initial install.php config before a DNS cutover

> DB connection string requires 172.17.0.1 (the default docker private IP network bridge)

    root@physicstime:/home/USER/physicstime.com# mv files/ /var/www/html/sites/physicstime.com/
    mv all /var/www/html/sites/
    
    ifconfig | grep Bc
        172.17.0.1
    
    docker run -it --rm --volume /opt:/opt mariadb:5.5 /bin/bash
        mysql -h172.17.0.1 -uYOURUSER -p physicstime
            show tables;
            exit
        mysql -h172.17.0.1 -uroot -p physicstime < backup.sql
    
    chown root:root -R /var/www/html/sites/
    chmod 400 /var/www/html/sites/default/settings.php

> ensure /var/www/html/sites/default/files has the correct permissions, otherwise no CSS for you!


    docker-compose stop
    docker ps --all
    docker-compose up &
    docker-compose logs |& tee /var/log/physicstime.log
    tail -f /var/log/physicstime.log /var/log/nginx/access.log
> This starts it manually and displays any traffic

    cd /etc/init.d; touch physicstime.sh; chmod +x physicstime.sh; vi physicstime.sh
        
        #!/bin/bash
        echo "starting physicstime after boot" >> /var/log/physicstime.log
        cd /home/YOURUSER; docker-compose up &
    
    update-rc.d physicstime.sh defaults
> this starts the docker based services automatically on boot (not including extra logging)



- - -
## Adhoc Performance and Latency Testing

Data driven decisions is a big deal, but let's be honest, engineers love numbers :)

    ab -l -r -n 500 -c 100 -k -H "Accept-Encoding: gzip, deflate" http://physicstime.com/node?page=1
> The unscientific "watching top": 80% for about 5 seconds vs 78% for about 5 seconds

<https://httpd.apache.org/docs/2.4/programs/ab.html>

### Linode and Cherokee and php-cgi 5.3 and MySQL 5.5

    Concurrency Level:      100
    Time taken for tests:   7.255 seconds
    Complete requests:      500
    Failed requests:        0
    Keep-Alive requests:    0
    Total transferred:      5321000 bytes
    HTML transferred:       5089500 bytes
    Requests per second:    68.92 [#/sec] (mean)
    Time per request:       1451.029 [ms] (mean)
    Time per request:       14.510 [ms] (mean, across all concurrent requests)
    Transfer rate:          716.22 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        2    2   0.4      2       6
    Processing:   102 1313 320.0   1437    1525
    Waiting:       89 1308 320.2   1431    1521
    Total:        104 1315 319.8   1439    1526
    
    Percentage of the requests served within a certain time (ms)
      50%   1439
      66%   1456
      75%   1466
      80%   1473
      90%   1488
      95%   1505
      98%   1516
      99%   1519
     100%   1526 (longest request)


### DigitalOcean and nginx and Docker php-fpm and MariaDB 5.5

    Concurrency Level:      100
    Time taken for tests:   7.791 seconds
    Complete requests:      500
    Failed requests:        0
    Keep-Alive requests:    0
    Total transferred:      5320068 bytes
    HTML transferred:       5082000 bytes
    Requests per second:    64.18 [#/sec] (mean)
    Time per request:       1558.145 [ms] (mean)
    Time per request:       15.581 [ms] (mean, across all concurrent requests)
    Transfer rate:          666.87 [Kbytes/sec] received
    
    Connection Times (ms)
                  min  mean[+/-sd] median   max
    Connect:        0    1   1.1      0       4
    Processing:   542 1421 201.6   1453    2020
    Waiting:      531 1417 201.2   1447    2017
    Total:        545 1422 201.0   1453    2022
    
    Percentage of the requests served within a certain time (ms)
      50%   1453
      66%   1470
      75%   1485
      80%   1494
      90%   1510
      95%   1674
      98%   1877
      99%   1930
     100%   2022 (longest request)

> So it seems there's a slight edge in either cherokee over nginx OR not running dockerized applications OR linode vs digitalocean BUT...

When I tweaked it for higher concurrency `ab -l -r -n 500 -c 200 -k -H "Accept-Encoding: gzip, deflate" http://physicstime.com/node?page=8`

Linode + Cherokee + php-cgi

    Time taken for tests:   9.933 seconds
    Requests per second:    50.34 [#/sec] (mean)
    Time per request:       3973.367 [ms] (mean)

DigitalOcean + Nginx + Docker + php-fpm

    Time taken for tests:   8.120 seconds
    Requests per second:    61.58 [#/sec] (mean)
    Time per request:       3248.067 [ms] (mean)

I can see the trend reverse (shrug)

#### Latency testing

<https://tools.pingdom.com/>

- website speed test (NY) for cherokee and php-cgi had a load time of 1.17s
- website speed test (NY) for nginx and Docker had a load time of 1.46s

> meh


### Conclusions

Adding docker simplifies one kind of complexity (stringing together multiple services that are packaged upstream) but can come at some cost to performance. (Though this might also be due to the cheaper node price)

The other major advantage of using docker is that different components/services can be upgraded independently (and even just "test upgraded") which allows for a faster adoption of upstream project improvements.

I personally don't like relying on the OS of the host for all of the global dependencies to play nice (and especially that different packages won't have conflicting dependencies).

Since all of these processes are running in the same host that I own I expect I'm not worse off security wise.

I'm curious to see if given enough time I run into the infamous /var/lib/docker issues of orphan containers, running out of disk space, or other issues.

A next step might be to run this in a PlatormAsAService like OpenShift or better yet break up each container to run via a ContainerAsAService (if it's free ;)

Obviously if performance and scale of a mostly read-only content distribution system was really an issue adding a cache layer like Varnish or Cloudflare or even just tweaking the various configurations would help =]

