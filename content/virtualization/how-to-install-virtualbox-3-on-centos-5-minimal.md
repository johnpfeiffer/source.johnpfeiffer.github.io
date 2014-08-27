Title: How To Install Virtualbox 3 on CentOS 5 Minimal
Date: 2009-11-15 20:59
Tags: virtualbox,centos

From the install DVD:

choose no packages and customize all to deselect all packages

BEWARE: this is a very empty configuration so you will have to install A LOT from yum...

`yum install wget elinks sudo which`

> IF you need to do anything with "compiling"  

`yum install make gcc`

`yum install kernel`  ? maybe necessary?  

`yum install kernel-devel-$(uname -r)`

`yum install kernel-headers-$(uname -r)`

`export KERN_DIR=/usr/src/kernels/$(uname -r)-x86_64`

## to add a repository, e.g. VirtualBox

So create the following file (in the directory) /etc/yum.repos.d/virtualbox.repo

    [virtualbox]
    name=RHEL/CentOS-$releasever / $basearch - VirtualBox  
    baseurl=http://download.virtualbox.org/virtualbox/rpm/rhel/$releasever/$basearch  
    enabled=1  
    gpgcheck=1  
    gpgkey=http://download.virtualbox.org/virtualbox/debian/sun_vbox.asc

then try

yum install virtualbox

## download locations
<http://www.centos.org>

<http://download.virtualbox.org/virtualbox/rpm/rhel/> 

<http://download.virtualbox.org/virtualbox/debian/sun_vbox.asc>
