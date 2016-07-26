Title: nginx with Docker
Date: 2015-06-13 08:00
Tags: docker, nginx

[TOC]

## nginx overview

<http://nginx.org/en/> is one of the most popular performant web servers in the world (and it's pretty handy as a reverse proxy or load balancer too!). <http://nginx.org/en/docs/http/load_balancing.html>

<https://github.com/nginx/nginx> is written in c (very performant but often needs to be compiled , especially with any of the extra 3rd party modules <https://www.nginx.com/resources/wiki/modules/>).

A recent update means "...optionally load separate shared object files at runtime as modules" 
<https://www.nginx.com/blog/dynamic-modules-nginx-1-9-11/>


## docker pull nginx

With Docker most of the time is spent in preparation, configuration, and testing.  The advantage is that less time is wasted on compiling, packaging, etc. (for all those still eeking out another 1% in efficiency via esoteric flags and bundling all sorts of custom modules - good luck!)

One quick way to attempt to leverage nginx as a front end for your projects is using containers with Docker <https://hub.docker.com/_/nginx/>

    sudo su
    docker pull nginx:alpine
    docker images

> This will grab the latest image based on the very small alpine linux <https://en.wikipedia.org/wiki/Alpine_Linux>, around 13 MB vs 191 MB for the traditional nginx:latest which is based on debian jessie <https://en.wikipedia.org/wiki/Debian>

<https://hub.docker.com/r/library/nginx/tags/> contains what other versions of nginx are provided by the vendor as Docker Images, the default build/image has quite a few modules <http://nginx.org/en/docs/>

> all future references to docker commands will assume you are root or typing sudo first

## docker nginx interactive container

    docker run --rm --publish 127.0.0.1:80:80 nginx
> starts an ephemeral container that binds the container port 80 to the local Host port 80 (binding to 127.0.0.1 prevents any other access except from the Host) , note by not explicitly sharing port 443 it is not connected/available

    docker ps -a
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                 PORTS                           NAMES
    3fccf15a3c24        nginx               "nginx -g 'daemon off"   3 seconds ago       Up 2 seconds        127.0.0.1:80->80/tcp, 443/tcp   pensive_elion

    netstat -antp
    Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
    tcp        0      0 127.0.0.1:80            0.0.0.0:*               LISTEN      5826/docker-proxy


    curl 127.0.0.1:80
> `<h1>Welcome to nginx!</h1>` is part of the default nginx home page, (success)

You will notice the access logs are being output to the console (where the docker container is running).

    192.168.1.100 - - [01/Jan/1970:01:00:59 +0000] "GET / HTTP/1.1" 200 612 "-" "curl/7.38.0" "-"

`Control + C` will terminate the container

## running nginx manually in the interactive docker container

    docker run --rm -i -t --publish 127.0.0.1:80:80 nginx /bin/bash
> Starting as root inside the container 

    root@557ac197e2c1:/# which nginx
        /usr/sbin/nginx

### nginx version and modules
        
    root@557ac197e2c1:/# nginx -V
        nginx version: nginx/1.9.7
        built by gcc 4.9.2 (Debian 4.9.2-10) 
        built with OpenSSL 1.0.1k 8 Jan 2015
        TLS SNI support enabled
        configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --with-threads --with-stream --with-stream_ssl_module --with-mail --with-mail_ssl_module --with-file-aio --with-http_v2_module --with-cc-opt='-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-z,relro -Wl,--as-needed' --with-ipv6
            
### Test your config file

    nginx -t -c /etc/nginx/nginx.conf -g "daemon off;"
> nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
> nginx: configuration file /etc/nginx/nginx.conf test is successful

### run nginx directly
    /usr/sbin/nginx -c /etc/nginx/nginx.conf
> -g "pid /var/run/nginx.pid; worker_processes 2;" from <https://www.nginx.com/resources/wiki/start/topics/tutorials/commandline/>
        
## nginx.conf

While there are quite a few ways to configure nginx one choice to make with Docker is to either

1. `docker run --name some-nginx -v /some/nginx.conf:/etc/nginx/nginx.conf:ro -d nginx`
> run docker as a daemon with a specified Container Name and override the container nginx.conf file with /some/nginx.conf from the hose

2. Use a Dockerfile (based on the upstream nginx Docker image) to copy your own configuration file and other custom bits in and build your own custom Docker image (a highly recommended way of not being completely dependent on an upstream provider - especially if you push your Docker Image to your own private registry afterwards)

e.g. <https://hub.docker.com/r/jwilder/nginx-proxy/~/dockerfile/> which also has "Foreman in Go lang" and makes use of expecting the Host to provide the SSL certificates

- <https://www.nginx.com/resources/admin-guide/nginx-web-server/>
- <https://www.nginx.com/resources/wiki/start/topics/examples/full/>

    docker run --rm --publish 127.0.0.1:80:80 nginx /bin/bash -c "nginx -t -c /etc/nginx/nginx.conf"
        nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
        nginx: configuration file /etc/nginx/nginx.conf test is successful
        


## Build your own nginx Dockerfile

If you require 3rd party modules then you will have to build nginx from source, e.g.
<https://github.com/openresty/headers-more-nginx-module#installation>

That being the case you'll probably want to have a build process with 2 Docker files:

1. the first Dockerfile will contain build-essentials, gcc, make, etc. so that you can build the binary from source (with any 3rd party modules) <http://nginx.org/en/docs/configure.html>
1. The second docker image would be your "production container" where you copy in the custom nginx binary, install the dependencies (i.e. openssl), and setup the default config.

### Converting an existing nginx 3rd party module to a dynamic module
Since NGINX 1.9.11 supports dynamic modules and attempts to maintain API compatibility then it is possible to sometimes convert a module into a dynamic module (i.e. build the shared library object)

    ./configure --add-dynamic-module=/opt/source/ngx_my_module/
    make -f objs/Makefile modules

> Look for .so files in the objs directory after compilation or the modules subdirectory during installation

<https://www.nginx.com/resources/wiki/extending/converting/>

## Configuring nginx

There are entire books about how to configure nginx so I will just jot down some basics for myself.

### /etc/nginx/nginx.conf
    user nginx;
    worker_processes 4;
    pid /run/nginx.pid;
    
    events {
        worker_connections 1024;
    }
    
    http {
        server {
            location / {
                root /var/www;
            }
        }
#        include /etc/nginx/conf.d/*.conf;
    }
    

> Run the service as the www-data user and define 4 worker processes
> define an HTTP server that listens on port 80 by default
> the root location will return the contents of /var/www
> a best practice is to use multiple configuration files in the conf.d directory (as a really long complex configuration in a single is difficult to maintain)
> BUT we must comment it out as in the installation there can be a default.conf that overrides our nginx.conf


    sudo docker run -it --rm --publish 0.0.0.0:80:80 --volume /tmp/nginx.conf:/etc/nginx/nginx.conf:ro  nginx:alpine /bin/sh
> debug the image interactively by overriding the default CMD with a shell (remember that Alpine is limited so `apk update` and `apk add SOMENAME`

    sudo docker run --rm --publish 0.0.0.0:80:80 --volume /tmp/nginx.conf:/etc/nginx/nginx.conf:ro  nginx:alpine /bin/sh -c "nginx -t -c /etc/nginx/nginx.conf"
> alternative method to just test your configuration file

    sudo docker run --rm --publish 0.0.0.0:80:80 --volume /tmp/nginx.conf:/etc/nginx/nginx.conf:ro --volume /tmp/www:/var/www:ro  nginx:alpine

> assumes you have a config file and some index file defined

    /var/www/index.html
    <html><body>hi</body></html>

That's it, now you have nginx serving static files! (curl localhost OR use a browser and visit localhost or http://hostfqdn)
> of course /tmp is an insecure location so please store production nginx configuration files and web content from a secure directory in the docker host filesystem


- <http://nginx.org/en/docs/beginners_guide.html>
- <http://nginx.org/en/docs/ngx_core_module.html#worker_processes>

### nginx with ssl

It is hard to imagine running a production (or even test or dev server that should mirror production) without SSL since all traffic could be intercepted or hijacked.  It takes a little more work but clearly it is an important step in running a service that others will use.

#### /etc/nginx/nginx.conf
    user nobody;
    worker_processes 4;
    pid /run/nginx.pid;
    
    events {
        worker_connections 1024;
    }
    
    http {
        server {
            listen 443 ssl;
    
            ssl_certificate /etc/nginx/server.crt;
            ssl_certificate_key /etc/nginx/server.key;
    
            location / {
                root /var/www;
            }
        }
    }    

#### openssl self signed certificates

    openssl req -subj '/CN=example.com/O=My Company Name LTD./C=US' -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout /tmp/server.key -out /tmp/server.crt

    mkdir -p /tmp/www

    echo "<html><body>hi</body></html>" > /tmp/www/index.html

#### dockerized nginx with ssl

    sudo docker run --rm --publish 0.0.0.0:443:443 --volume /tmp/nginx.conf:/etc/nginx/nginx.conf:ro --volume /tmp/server.crt:/etc/nginx/server.crt --volume /tmp/server.key:/etc/nginx/server.key --volume /tmp/www:/var/www:ro  nginx:alpine

    curl --insecure https://localhost
    firefox https://localhost

- <http://nginx.org/en/docs/http/configuring_https_servers.html>

### nginx with ssl and http/2

<https://en.wikipedia.org/wiki/HTTP/2> is a new and more capable and performant standard for the venerable HTTP protocol.  It has widespread vendor support so you can use most modern servers (e.g. nginx) and most modern browsers (e.g. chrome) and get the benefits immediately. (With of course all sorts of fallbacks for legacy clients)


#### /etc/nginx/nginx.conf
    user nobody;
    worker_processes 4;
    pid /run/nginx.pid;
    
    events {
        worker_connections 1024;
    }
    
    http {
        server {
            listen 80;
            location / {
                return 301 https://$host$request_uri;
            }
        }
        server {
            listen 443 ssl http2 default_server;
            
            ssl_certificate /etc/nginx/server.crt;
            ssl_certificate_key /etc/nginx/server.key;
            
            location / {
                root /var/www;
            }
        }
    }

> Assuming the previous nginx with ssl steps of creating a certificate and content, be aware that **browsers permanently CACHE the 301 redirect** so use Private Browsing mode otherwise you will never see a different result for localhost =[

    sudo docker run --rm --publish 0.0.0.0:80:80 --publish 0.0.0.0:443:443 --volume /tmp/nginx.conf:/etc/nginx/nginx.conf:ro --volume /tmp/server.crt:/etc/nginx/server.crt --volume /tmp/server.key:/etc/nginx/server.key --volume /tmp/www:/var/www:ro  nginx:alpine

#### Verifying HTTP/2

**curl**

    curl localhost
    
    <html>
    <head><title>301 Moved Permanently</title></head>
    <body bgcolor="white">
    <center><h1>301 Moved Permanently</h1></center>
    <hr><center>nginx/1.9.12</center>
    </body>
    </html>
    

    curl --insecure --location localhost

    <html><body>hi</body></html>
    
**openssl s_client**

    openssl s_client -connect localhost:443 -nextprotoneg ''
    
    CONNECTED(00000003)
    Protocols advertised by server: h2, http/1.1

**chrome browser**
    
Browse directly to https://localhost/ with the chrome extension installed: <https://chrome.google.com/webstore/detail/http2-and-spdy-indicator/mpbpobfflnpcgagjijhmgnchggcjblin/related?hl=en>

The blue lightning symbol on the far far right (next to the "hamburger") indicates HTTP/2 is working.

> **browsers permanently CACHE the 301 redirect** so connecting to http://localhost will forever see a different result for localhost =[

1. Browse directly to https://localhost/  (If using a self signed certificate accept any warnings about insecure SSL)
2. Chrome/Chromium Settings -> More tools -> Developer tools (aka Control + Shift + I)
3. Click on the Network section
4. Control + Shift + F5 to reload (or click on the arrow circling up)
5. Right click on the Name colum in the result so that you can add results for column heading, "Protocol"
6. Control + Shift + F5 to reload (or click on the arrow circling up)

Protocol: h2

- <https://www.nginx.com/blog/nginx-1-9-5/>
- <https://blog.cloudflare.com/tools-for-debugging-testing-and-using-http-2/>
- <http://tech.finn.no/2015/09/25/setup-nginx-with-http2-for-local-development/>
