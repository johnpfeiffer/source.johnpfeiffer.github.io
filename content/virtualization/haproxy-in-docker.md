Title: HAProxy in Docker
Date: 2015-05-21 20:00
Tags: docker, haproxy

[TOC]

Not only are Containers fast, one of the biggest advantages of Containers is the ability to reduce complexity.

Docker can turn an application/service, it's dependencies, and even the OS level requirements into a single blackbox package (that you can still inspect inside if you really want to).

One thing I really like is less code.  Seriously.  Configuration over coding (whenever I don't need customization) means far less maintenance and bugs.

Here's a trivial example of how I can leverage the HAProxy Docker image/container to load balance two web servers. (aka "reverse proxy" <http://en.wikipedia.org/wiki/Reverse_proxy>)

        client -> all other sites
          |
    reverse proxy (haproxy)
      /         \
    BackendA  BackendB


> There are new problems that go along with the benefits of any new technology, see the complicated networking/port coordination

### Prerequisites

    sudo docker pull haproxy:1.5

#### Some backend web servers

    mkdir -p /tmp/BackendA
    echo "foo" > /tmp/BackendA/foo.txt
    cd /tmp/BackendA
    python -m SimpleHTTPServer 8000 &
    
    mkdir -p /tmp/BackendB
    echo "bar" > /tmp/BackendB/bar.txt
    cd /tmp/BackendB
    python -m SimpleHTTPServer 8001 &
    
> Clearly a trivial example (more likely two remote hosts in logical/geographic disparate areas if aiming for High Availability, or at least on different hosts to scale with more resources)


### /opt/mydata/haproxy.cfg
    global
            debug
    
    defaults
            log global
            mode    http
            timeout connect 5000
            timeout client 5000
            timeout server 5000
    
    listen http_proxy :8443
            mode tcp
            balance roundrobin
            server srv1 docker:8000 check
            server srv2 docker:8001 check
    

### start haproxy.sh

    :::bash
    #!/bin/bash
    HOSTIP=`ip addr show | grep docker0 | grep global | awk '{print $2}' | cut -d / -f1`

    sudo docker run -p 8443:8443 --add-host=docker:${HOSTIP} --rm -it -v /opt/mydata/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro --name myhaproxy haproxy:1.5 

> Now that the docker container's /etc/hosts file has the Host IP Address injected (with the name "docker") the haproxy config file probably makes more sense

- running the container
- the host port 8443 mapped to the container port 8443
- injecting into the container /etc/hosts the Host IP Address as "docker"
- ephemeral container (automatic cleanup on termination)
- interactive
- tty
- readonly mapping of the /opt/mydata/haproxy.cfg file on the host to /usr/local/etc/haproxy/haproxy.cfg
- name the container myhaproxy (each container name must be unique)
- the container is using the haproxy version 1.5 Docker Image

    ./start-haproxy.sh

    curl localhost:8443
    
    :::html
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>
    <title>Directory listing for /</title>
    <body>
    <h2>Directory listing for /</h2>
    <hr>
    <ul>
    <li><a href="bar.txt">bar.txt</a>
    </ul>
    <hr>
    </body>
    </html>
    
    
    curl localhost:8443
    
    :::html
    <!DOCTYPE html PUBLIC "-//W3C//DTD HTML 3.2 Final//EN"><html>
    <title>Directory listing for /</title>
    <body>
    <h2>Directory listing for /</h2>
    <hr>
    <ul>
    <li><a href="foo.txt">foo.txt</a>
    </ul>
    <hr>
    </body>
    </html>


### HAProxy Stats

    sudo docker rm -f myhaproxy

#### /opt/mydata/haproxy.cfg
    global
        debug
    
    defaults
        log global
        mode    http
        timeout connect 5000
        timeout client 5000
        timeout server 5000
    
    listen http_proxy :8443
        mode tcp
        balance roundrobin
        server srv1 docker:8000 check
        server srv2 docker:8001 check

    # optional section to enable statistics for haproxy protected by basic auth (replace with your own user and password)
    listen stats :1936
        stats enable
        stats uri /
        stats realm HAProxyStatistics
        stats auth user:password


    ./start-haproxy.sh

### nginx forward proxy

client -> forward proxy (nginx) -> all other sites

    docker pull nginx:alpine

#### nginx.conf

    worker_processes  1;
    
    events {
        worker_connections  1024;
    }
    
    http {
        include       mime.types;
        default_type  application/octet-stream;
    
        sendfile        on;
        keepalive_timeout  65;
    
        gzip  on;
    
        server {
            listen       8080;
    
            location / {
                resolver 8.8.8.8;
                proxy_pass http://$http_host$uri$is_args$args;
            }
    
            error_page   500 502 503 504  /50x.html;
            location = /50x.html {
                root   html;
            }
        }
    }



    docker run -it --rm -p 8080:8080 -v /tmp/nginx.conf:/etc/nginx/nginx.conf:ro --name mynginx nginx:alpine

> bind to port 8080 on the host and run an ephemeral container based on the alpine linux with nginx image that uses the /tmp/nginx config

    http_proxy=127.0.0.1:8080 curl example.com

> set the linux operating system proxy environment just for this one curl command and see the dockerized nginx forward proxy log show: 172.17.0.1 - - [06/May/2016:22:37:22 +0000] "GET HTTP://example.org/ HTTP/1.1" 200 1270 "-" "curl/7.35.0"


Configure your browser (firefox) to use 127.0.0.1:8080 as the proxy for all protocols and watch the log statements fly by when you test http://example.com

> NOTE: this does not support HTTPS <http://forum.nginx.org/read.php?2,15124,15256#msg-15256> 

> Attempting https://example.com will return "CONNECT example.com:443 HTTP/1.1" 400 173 "-" "-"  and the browser will show "Server not found"

** Warning ** do not use *http_proxy=http://127.0.0.1:8080* as that will fail =[

You can permanently set the environment proxy with export http_proxy=127.0.0.1:8080

### HAProxy as a limited outbound proxy

    sudo docker pull haproxy:1.6-alpine

Now that you have the 10MB haproxy image...

> Note there is a limitation to haproxy in that it always assumes a syslog facility (no direct logging to stdout or files)

- <https://github.com/dockerfile/haproxy/issues/3>
- <http://www.gnu.org/software/libc/manual/html_node/Overview-of-Syslog.html>


#### /opt/mydata/haproxy.cfg
This is the more readable config style which separates the frontend from backend and this is haproxy 1.6

> The logging probably does not work =(

    global
            debug
            log /dev/log local0 info
    
    defaults
            mode http
            timeout connect 5s
            timeout client 5s
            timeout server 5s
    
    frontend myfrontend
            bind *:8443
            default_backend mybackend
    
    backend mybackend
            server s1 example.com:443 ssl verify none
    


#### starting the haproxy docker container
    docker run -p 8443:8443 --rm -it -v /home/admin/haproxy.cfg:/usr/local/etc/haproxy/haproxy.cfg:ro -v /dev/log:/dev/log --name myhaproxy haproxy:1.6-alpine


> Control + C to quit



### more info

- <https://registry.hub.docker.com/_/haproxy/>
- <https://cbonte.github.io/haproxy-dconv/configuration-1.5.html>
- <https://cbonte.github.io/haproxy-dconv/configuration-1.6.html>
- <http://www.haproxy.org/git?p=haproxy-1.6.git;a=tree;f=examples>
- <http://docs.docker.com/reference/commandline/cli/#adding-entries-to-a-container-hosts-file>
