Title: HAProxy in Docker
Date: 2015-05-21 20:00
Tags: docker, haproxy

[TOC]

Not only are Containers fast, one of the biggest advantages of Containers is the ability to reduce complexity.

Docker can turn an application/service, it's dependencies, and even the OS level requirements into a single blackbox package (that you can still inspect inside if you really want to).

Here's a trivial example of how I can leverage the haproxy Docker image/container to load balance two web servers.

> There are new problems that go along with the benefits of any new technology, see

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


### vim /opt/mydata/haproxy.cfg
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

`./start-haproxy.sh`

`curl localhost:8443`
    
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
    
    
`curl localhost:8443`
    
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
    

### more info

- <https://registry.hub.docker.com/_/haproxy/>
- <https://cbonte.github.io/haproxy-dconv/configuration-1.5.html>
- <http://docs.docker.com/reference/commandline/cli/#adding-entries-to-a-container-hosts-file>    
