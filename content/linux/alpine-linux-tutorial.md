Title: Alpine Linux Introduction Tutorial
Date: 2016-02-28 21:19:00
Tags: alpine, linux, security

[TOC]

Alpine Linux is a minimalist secure linux distro.

> In security terms less "footprint" often means less vectors of attack and less complexity to analyze for vulnerabilities

Alpine Linux is becoming a preferred base OS for many foundational official Docker Images (python, php, ruby, nginx, redis, haproxy, go) since downloading many large Docker Images (aka Deploying Docker Containers) can saturate the network at scale.

- <http://www.pcworld.com/article/3031765/is-docker-ditching-ubuntu-linux-confusion-reigns.html>
- <https://news.ycombinator.com/item?id=10998667>
- <https://en.wikipedia.org/wiki/Alpine_Linux>

### Getting started with Alpine Linux in Docker

This will pull the latest alpine image (around 4MB) and run it in an ephemeral container.

`sudo docker run -it --rm alpine /bin/sh`

- <https://hub.docker.com/_/alpine/>

### Basics

Most of the very basic commands are similar to other linux distros like Debian/Ubuntu/Redhat, but of course there are differences ;)

    ls -l /bin/sh
> /bin/busybox

    cat /etc/passwd
    less /etc/passwd
    vi /etc/passwd
    grep root /etc/passwd
    ls -l /usr/bin /usr/sbin | more
> more busybox

### Package Management

    apk update
    apk --help
> update the local index for all remote packages, list the options of the package manager

    apk info
> list all of the packages installed locally

    apk search curl
    apk search curl | sort
    apk info curl
    apk add curl
>  search the remote packages for a keyword (unsorted results), get info for a specific package, install a specific package

- <http://wiki.alpinelinux.org/wiki/Alpine_Linux_package_management>
- <https://pkgs.alpinelinux.org/packages>


### Networking
    hostname
    cat /etc/resolv.conf
    ifconfig
    netstat -anp

    traceroute
    apk add iptables


### Compiling C on Alpine Linux

    apk add build-base gcc abuild binutils

*This should probably be part of a Dockerfile rather than run every time in an ephemeral container*

<https://wiki.alpinelinux.org/wiki/How_to_get_regular_stuff_working#Compiling_:_a_few_notes_and_a_reminder>

`vi hi.c`

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
    chmod +x a.out
    file a.out
> The default is a.out: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, not stripped

    ./a.out
`hi`

> Note that this was just gcc not musl-gcc :(


#### Incomplete musl compiler on alpine linux

> WARNING: below did not work, TODO: <https://bitbucket.org/GregorR/musl-cross>

I suspect that I am overwriting the existing gcc toolchain and I need to specify a different prefix (/usr/local) 

    apk update
    apk add wget tar gzip gcc make
#    apk add musl-dev wget tar gzip gcc make

    wget --no-check-certificate http://www.musl-libc.org/releases/musl-1.1.15.tar.gz
    tar xf musl-1.1.15.tar.gz
    cd musl-1.1.15
    ./configure
    make install

> Now we've installed the musl compiler?

/usr/local/musl seemed terribly empty of binaries (i.e. no /usr/local/musl/bin/)

- <https://www.musl-libc.org/faq.html>
- <http://www.musl-libc.org/how.html>


    apk add alpine-sdk

But maybe because it's already an alpine linux container the gcc already uses musl instead of libc and does not need the musl-gcc wrapper?

<http://www.guidesbyeric.com/statically-link-c-programs-with-musl-gcc>

### Compile Go on Alpine Linux

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

> To just run the source code `go run intro.go`

`hi`

    :::bash
    ls -l
    go build intro.go
    ls -l
    ./intro

`hi`

Maybe 

<http://dominik.honnef.co/posts/2015/06/go-musl/> ?

### Git with Alpine

    :::bash
    apk update
    apk add --no-cache git
    git --version

