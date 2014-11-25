Title: Ubuntu Bootable USB and Best Packages to Install
Date: 2014-08-20 00:00
Tags: Linux, Ubuntu, USB Boot, Ubuntu Recovery

[TOC]

If you have a modern computer (BIOS) that can boot from USB it is well worth it since having the latest Ubuntu ISO on DVD tends to pile up.

## Write an ISO to usb

    fdisk -l
    umount /dev/sdc1

    sudo dd if=/home/ubuntu/Desktop/ubuntu-14.04.1-server-amd64.iso of=/dev/sdc
    
    1171456+0 records in
    1171456+0 records out
    599785472 bytes (600 MB) copied, 260.364 s, 2.3 MB/s

## Ubuntu Recovery mode 
(which is access to a single root user command line)

boot in recovery mode by using the arrow keys during boot (down to select Recovery)

1. mount networking 
1. root shell
    - `mount -o rw,remount /`

> mount --all # might be needed too

Now you can fix grub or /etc/passwd or free up some hard drive space


## Best Ubuntu Packages

> as of Utopic 14.10


	sudo apt-get update
	sudo apt-get install -y byobu build-essential elinks unzip unrar nano vim wget curl \
	ntp rcconf dialog openvpn git-core 

	wget -qO- https://bootstrap.pypa.io/get-pip.py | sudo python

	NOT SURE IN UTOPIC: sudo apt-get install openjdk-7-jre openjdk-7-jdk icedtea-7-plugin

	sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
	echo "deb https://get.docker.io/ubuntu docker main" > /etc/apt/sources.list.d/docker.list

	sudo apt-get install lxc-docker

- byobu = console terminal multi screen (survives network disconnects) <http://byobu.co>
- build-essential = tools for compiling and building debian packages <http://packages.ubuntu.com/lucid/build-essential>
- elinks = cli browser (just in case your GUI dies and you need to research) <http://kmandla.wordpress.com/2011/01/13/a-comparison-of-text-based-browsers>
- unzip and unrar = utilities to decompress compressed things
- nano = a simple text editor (much easier than vi/vim for just writing new text)
- wget and curl = utilities to download files
- ntp = network time protocol client daemon to keep your clock in sync
- openvpn = opensource vpn client <https://openvpn.net>
- rcconf = easier way to manage what services start at boot <https://packages.debian.org/jessie/rcconf>

- docker = virtual machine/container platform based on a unionfs

- python-setuptools = Sometimes required to install pip (the "drug dealer" for python based software) <http://pythonhosted.org//setuptools>
- icedtea = open java (plugin = browser java)


jdk = java development kit

### GUI

**Xubuntu Desktop** is my preferred "lightweight" GUI for Ubuntu: <http://xubuntu.org>

	apt-get install -y chromium-browser pepperflashplugin-nonfree geany arandr \
	keepassx xdiskusage rdesktop vlc

- geany = tabbed text notepad
- vlc = movies/music
- arandr = multi display gui config
- rdesktop = RDP client
- grdesktop = gnome UI for rdesktop
- ubuntu-restricted-extras
- dropbox = cloud file storage
- filezilla = file transfer protocol client (that supports sftp = secure ssh ftp)


	deb http://linux.dropbox.com/ubuntu utopic main
	sudo apt-key adv --keyserver pgp.mit.edu --recv-keys 5044912E
	
        deb http://repository.spotify.com stable non-free
	sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 94558F59

	sudo add-apt-repository ppa:pithos/ppa

        deb http://downloads.hipchat.com/linux/apt stable main
        wget -O - https://www.hipchat.com/keys/hipchat-linux.key | apt-key add -

	apt-get update; apt-get install dropbox spotify-client pithos hipchat


## Other Useful Packages


### Heroku CLI

- deb http://toolbelt.heroku.com/ubuntu ./
- wget -O- https://toolbelt.heroku.com/apt/release.key | apt-key add -
- apt-get install -y heroku-toolbelt


### Ruby and OpenShift CLI

https://gorails.com/setup/ubuntu/14.04

sudo apt-get install git-core curl zlib1g-dev build-essential libssl-dev libreadline-dev libyaml-dev libsqlite3-dev sqlite3 libxml2-dev libxslt1-dev libcurl4-openssl-dev python-software-properties
libgdbm-dev libncurses5-dev automake libtool bison libffi-dev

source ~/.rvm/scripts/rvm
echo "source ~/.rvm/scripts/rvm" >> ~/.bashrc
rvm install 2.1.2
rvm use 2.1.2 --default
ruby -v
echo "gem: --no-ri --no-rdoc" > ~/.gemrc

gem install rhc
red hat client for openshift

sudo echo "autologin-user=ubuntu" >>  /etc/lightdm/lightdm.conf.d/10-xubuntu.conf 


