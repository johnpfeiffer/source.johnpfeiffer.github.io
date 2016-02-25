Title: Debian Packages for Deployment
Date: 2016-02-24 20:40
Tags: debian, deb, build, packaging, deployment, scale

[TOC]

### What is a Debian Package?

A debian package is a way to distribute and install a collection of files (aka software) onto a system (i.e. Debian or Ubuntu).

While a piece of software might depend on other debian packages (e.g. libraries) usually a single .deb file represents some sort of module that serves a single purpose.

Once a debian package is built any client (dpkg or apt which also uses dpkg ;) can use it to install the software.


### Why use a Debian Package?

> When you're developing on your own box you can pretty much get away with anything

A complex and large scale production environment typically has a lot of costs (both operationally and in not becoming a bottleneck to dev velocity). Any opportunity to increase determinism and reduce risk is welcome.

Deploying source code directly from git version control doesn't always scale well (streaming tons of small files, dedicated read only service user direct to production, etc.) nor does it create enough determinism with dependency management.

As deployments become more frequent and the Continuous Integration becomes more complex it is really important to embrace the "build once" principle so that a single artifact (hopefully with all of its dependencies) can pass through the guantlet of integration testing and canary/incremental rollout.  

So now that you're convinced "Artifacts" are the way to go lets just skip .exe, .msi, .jar, .etc and go straight to...

The Debian Package is a "battle tested" format with lots of features (dependency requirements, preinst scripts, postinst scripts, etc.) but if there is a bug in a specific .deb file it is not always practical to get the full source code and rebuild the whole thing (especially considering static bindings and specific compilation environment/parameters).

One example people give is an erroneous pre install or post install script that is preventing either installation or removal.

The example below is more on just simply changing the control file "Description:"

### How to unpack a debian package, modify the control file, and repack it

To unpack, modify, and repack a debian package:

    wget https://example.com/example.deb --output-document /tmp/example.deb
    docker run --rm --it --volume /tmp:/tmp ubuntu:14.04 /bin/bash
    apt-get update
    apt-get install vim
    cd /tmp
    mkdir emptydir
    dpkg-deb -R example.deb /tmp/emptydir
    ls -ahl /tmp/emptydir
    ls -ahl /tmp/emptydir/DEBIAN
    vi /tmp/emptydir/DEBIAN/control
    dpkg-deb -b emptydir /tmp/example-fixed.deb


On your host /tmp should now contain example.deb and example-fixed.deb


### more info

- <https://www.debian.org/doc/manuals/debian-faq/ch-pkg_basics.en.html>
- <http://unix.stackexchange.com/questions/138188/easily-unpack-deb-edit-postinst-and-repack-deb>
- <http://manpages.ubuntu.com/manpages/hardy/man1/dpkg-deb.1.html>
