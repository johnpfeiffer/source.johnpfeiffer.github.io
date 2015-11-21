Title: nginx with Docker
Date: 2015-06-13 08:00
Tags: docker, nginx

[TOC]

- <http://nginx.org/en/>
- nginx is one of the most popular performant web servers in the world (and it's pretty handy as a reverse proxy or load balancer too!). 
<http://nginx.org/en/docs/http/load_balancing.html>

<https://github.com/nginx/nginx> is written in c (very performant but often needs to be compiled , especially with any of the extra 3rd party modules <https://www.nginx.com/resources/wiki/modules/>).


## docker pull nginx

One quick way to attempt to leverage nginx as a front end for your projects is using containers with Docker <https://hub.docker.com/_/nginx/>

    sudo su
    docker pull nginx:latest
    docker images

<https://hub.docker.com/r/library/nginx/tags/> contains what other versions of nginx are provided by the vendor as Docker Images, the default build/image has quite a few modules <http://nginx.org/en/docs/>

> all future references to docker commands will assume you are root or typing sudo first

### docker nginx interactive

`docker run --rm --publish 127.0.0.1:80:80 nginx`
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

Control + C will terminate the container

### docker nginx interactive

`docker run --rm -i -t --publish 127.0.0.1:80:80 nginx /bin/bash`
> Starting as root inside the container 

    root@557ac197e2c1:/# which nginx
        /usr/sbin/nginx
        
    root@557ac197e2c1:/# nginx -V
        nginx version: nginx/1.9.7
        built by gcc 4.9.2 (Debian 4.9.2-10) 
        built with OpenSSL 1.0.1k 8 Jan 2015
        TLS SNI support enabled
        configure arguments: --prefix=/etc/nginx --sbin-path=/usr/sbin/nginx --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --pid-path=/var/run/nginx.pid --lock-path=/var/run/nginx.lock --http-client-body-temp-path=/var/cache/nginx/client_temp --http-proxy-temp-path=/var/cache/nginx/proxy_temp --http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp --http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp --http-scgi-temp-path=/var/cache/nginx/scgi_temp --user=nginx --group=nginx --with-http_ssl_module --with-http_realip_module --with-http_addition_module --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_stub_status_module --with-http_auth_request_module --with-threads --with-stream --with-stream_ssl_module --with-mail --with-mail_ssl_module --with-file-aio --with-http_v2_module --with-cc-opt='-g -O2 -fstack-protector-strong -Wformat -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-z,relro -Wl,--as-needed' --with-ipv6
            
Test your config file:

`nginx -t -c /etc/nginx/nginx.conf -g "daemon off;"`
> nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
> nginx: configuration file /etc/nginx/nginx.conf test is successful

<https://www.nginx.com/resources/wiki/start/topics/tutorials/commandline/>
    
        
### nginx.conf

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

