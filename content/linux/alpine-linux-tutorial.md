Title: Alpine Linux Introduction Tutorial
Date: 2016-02-28 21:19:00
Tags: alpine, linux, security

[TOC]

Alpine Linux is a minimalist secure linux distro.

> In security terms less "footprint" often means less vectors of attack and less complexity to analyze for vulnerabilities

Alpine Linux is becoming a preferred base OS for many foundational official Docker Images (python, php, ruby, nginx, redis, haproxy,) since downloading Docker Images (aka Deploying Docker Containers) can saturate the network at scale.

- <https://hub.docker.com/_/alpine/>
- <http://www.pcworld.com/article/3031765/is-docker-ditching-ubuntu-linux-confusion-reigns.html>
- <https://news.ycombinator.com/item?id=10998667>
- <https://en.wikipedia.org/wiki/Alpine_Linux>

### Basics

Most of the very basic commands are similar to other linux distros like Debian/Ubuntu/Redhat, but of course there are differences ;)

    /bin/sh
> busybox

    cat /etc/passwd
    curl 127.0.0.1
    ls -l /usr/bin /usr/sbin | more
> more busybox

### Package Management

    apk --help
    apk update
    apk search iptables
    apk add iptables


<http://wiki.alpinelinux.org/wiki/Alpine_Linux_package_management>


### Networking
    hostname
    cat /etc/resolv.conf
    ifconfig
    netstat -anp

    apk add iptables
    traceroute

### Compiling

#### prepare musl compiler on alpine linux

> WARNING: below did not work

    docker pull alpine
    docker run -it --rm alpine /bin/sh

    apk update
    apk add musl-dev wget tar gzip gcc make

    wget http://www.musl-libc.org/releases/musl-1.1.15.tar.gz
    tar xf musl-1.1.15.tar.gz
    cd musl-1.1.15
    ./configure
    make
    make install

> Now we've installed the musl compiler?

/usr/local/musl seemed terribly empty of binaries

<http://dominik.honnef.co/posts/2015/06/go-musl/>

#### hi.c

    :::c
    #include <stdio.h>
    
    int main()
    {
      printf("hi");
    }

#### compiling

    apk add file
    gcc -static hi.c
    file a.out
    chmod +x a.out
    ./a.out

> hi
> The default is a.out: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped
> Note that this was just gcc not musl-gcc :(


<http://www.musl-libc.org/how.html>

    docker run -it --rm alpine /bin/sh
    apk update
    apk add alpine-sdk

But maybe because it's already an alpine linux container the gcc already uses musl instead of libc and does not need the musl-gcc wrapper?

#### compile go on alpine linux

Just use the golang image based on alpine linux ;)

<https://github.com/docker-library/docs/tree/master/golang>

    docker pull golang:alpine
    docker run -it --rm golang:alpine /bin/sh
> Now that we've got the container running we can use the shell

`vi intro.go`
    
    package main
    
    import "fmt"
    
    func main() {
      fmt.Println("hi")
    }
    

    go run intro.go
> hi
    ls -l
    go build intro.go
    ls -l
    ./intro
> hi

