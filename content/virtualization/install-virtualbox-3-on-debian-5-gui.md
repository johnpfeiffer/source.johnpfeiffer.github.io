Title: Install Virtualbox 3 on Debian 5 gui
Date: 2010-01-09 07:00
Tags: virtualbox,debian

[TOC]

NOTE: this is a command line installation of VirtualBox 3 proprietary driver edition...

The "open source edition" does not include RDP into VM's nor USB drivers for VM's to access host USB's


### Preparation Steps

`uname -r //find your kernel version`

`apt-cache search linux-headers //in the long list see if your version is there`

`sudo apt-get install linux-headers-$(uname -r) //failed because I have "squeeze" 2.6.32-rc8-686`

> unfortunately the rc8 headers were missing from debian website

`apt-get install linux-headers-2.6.32-trunk-686 //manual way (instead of the fancy function returns a result)`

`ls -ahl /usr/src //ensure the folders are there, sometimes no kernel folder`

`export KERN_DIR=/usr/src/kernels/2.6.32-trunk-686 //sometimes instead /usr/src/2.6.32-trunk-686`


### Actual Installation

<http://www.virtualbox.org/wiki/Linux_Downloads>

`nano /etc/apt/sources.list //add line`

    deb http://download.virtualbox.org/virtualbox/debian lenny non-free

`apt-get update`

`apt-cache search virtualbox`

`apt-get install virtualbox-3.0 //install without verification...`

`sudo addusers username vboxusers`

OR `usermod -a -G vboxusers USERNAME`


### GUI Management

    Setting up virtualbox-3.0 (3.0.12-54655_Debian_lenny) ...
    addgroup: The group \`vboxusers' already exists as a system group.
    Exiting.
    
    Messages emitted during module compilation will be logged to /var/log/vbox-install.log.
    Success!
    
    Starting VirtualBox kernel module:done..

    Setting up libsdl-ttf2.0-0 (2.0.9-1) ...

type `VBoxManage -v` to see if everything is working (shows your VirtualBox version)

`VirtualBox`
> this command starts the GUI interface where you can easily create/manage

you can test it - from the command line create and start a VM, you'll see it appear in the GUI!

`VBoxManage createvm --name VM1 --register`

`VBoxManage startvm VM1`

VirtualBox GUI is pretty straightforward but I highly recommend that you
skim the manual and especially that you learn to play with the command line VBoxManage


### Troubleshooting

`/etc/init.d/vbox_drv setup`

> The above command often fails, and when it fails, check the install log

`nano /var/log/vbox-install.log`

1. no kernel headers installed/downloaded or export (so the OS knows where!)

2. the user running VirtualBox needs to be in the /etc/group/vboxusers

if you have not installed the right headers (e.g. Virtualbox is compiling a driver specific to your kernel)

So you need gcc, make... also you need the kernel-headers source

`uname -a`
> will show you exactly what kernel you have installed

`ls -ahl /usr/src`
>will show you exactly what directories are there... 

see some varations:

    export KERN_DIR=/usr/src/2.6.32-trunk-686
    export KERN_DIR=/usr/src/kernels/2.6.32-trunk-686
    export KERN_DIR=/usr/src/kernels/2.6.18-128.4.1.el5-x86_64/
    
`sudo apt-get remove virtualbox-3.0`
> the easiest method to uninstall

do all of the fixes (e.g. in my case I had to downgrade my kernel from 2.6.32-rc8 to 2.6.32-trunk)

    sudo apt-get install linux-image-686
    sudo apt-get install linux-headers-$(uname -r)
    export KERN_DIR=/usr/src/2.6.32-trunk-686
    sudo apt-get install virtualbox-3.0
    usermod -a -G vboxusers USERNAME
    
> after the reinstall hopefully you'll see:


    Setting up libcurl3 (7.19.7-1) ...
    Setting up virtualbox-3.0 (3.0.12-54655\_Debian\_lenny) ...
    addgroup: The group \`vboxusers' already exists as a system group.
    Exiting.
    
    Messages emitted during module compilation will be logged to /var/log/vbox-install.log.
    Success!
        
    Starting VirtualBox kernel module:done..
    
    Setting up libsdl-ttf2.0-0 (2.0.9-1) ...

type `VBoxManage -v` to see if everything is working (shows your VirtualBox version)

