Title: Ubuntu Bootable USB, apt-get and dpkg, and the best packages to install
Date: 2014-08-20 00:00
Tags: Linux, Ubuntu, USB Boot, Ubuntu Recovery, dpkg, apt-get

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


## package management with apt commands

### Pro Tip: Force ipv4 to avoid lengthy IPV6 timeouts

`sudo apt-get -o Acquire::ForceIPv4=true update`

`sudo apt-get -o Acquire::ForceIPv4=true install vim`

`sudo echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4 `
> persistent config to always use ipv4


### apt-cache

debian has precompiled packages of binaries and libraries that can very easily be installed via the command line (or GUI) using Advanced Packaging Tool (APT) <https://wiki.debian.org/Apt>

`apt-cache search ssh`
> to find packages with the name ssh

`apt-cache show ssh`
> to show the details about a specific package

`apt-cache showpkg ssh`
> to show more general info about a package

`apt-cache depends ssh`
> to show the package dependencies

### apt-get

`sudo apt-get install ssh`

### apt-key

`sudo apt-key update`
> if apt errors: WARNING: The following packages cannot be authenticated


## Best Ubuntu Packages

> as of Utopic 14.10


	sudo apt-get update
	sudo apt-get install -y byobu build-essential elinks unzip unrar nano vim wget curl ntp rcconf dialog git-core 

	wget -qO- https://bootstrap.pypa.io/get-pip.py | sudo python



- byobu = console terminal multi screen (survives network disconnects) <http://byobu.co>
- build-essential = tools for compiling and building debian packages <http://packages.ubuntu.com/lucid/build-essential>
- elinks = cli browser (just in case your GUI dies and you need to research) <http://kmandla.wordpress.com/2011/01/13/a-comparison-of-text-based-browsers>
- unzip and unrar = utilities to decompress compressed things
- nano = a simple text editor (much easier than vi/vim for just writing new text)
- wget and curl = utilities to download files
- ntp = network time protocol client daemon to keep your clock in sync
- rcconf = easier way to manage what services start at boot <https://packages.debian.org/jessie/rcconf>


- python-setuptools = Sometimes required to install pip (the "drug dealer" for python based software) <http://pythonhosted.org//setuptools>
- icedtea = open java (plugin = browser java)

- openvpn = opensource vpn client <https://openvpn.net>


jdk = java development kit

`sudo apt-get install openjdk-8-jdk`
> NOT SURE IN UTOPIC: sudo apt-get install openjdk-7-jre openjdk-7-jdk icedtea-7-plugin

### Docker
docker = virtual machine/container platform based on a unionfs

	sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
	echo "deb https://get.docker.io/ubuntu docker main" > /etc/apt/sources.list.d/docker.list

	sudo apt-get install lxc-docker

### GUI

**Xubuntu Desktop** is my preferred "lightweight" GUI for Ubuntu: <http://xubuntu.org>

`apt-get install -y chromium-browser pepperflashplugin-nonfree geany arandr keepassx xdiskusage rdesktop`

- chromium-browser = opensource branch/clone of google chrome browser
- geany = tabbed text notepad (with syntax highlighting)
- arandr = multi display gui config
- keepassx = secure password inventory (has a mini version for  iphone too)
- xdiskusage = graphical view of disk space usage by folder and file
- rdesktop = RDP client

- grdesktop = gnome UI for rdesktop


- dropbox = cloud file storage

	deb http://linux.dropbox.com/ubuntu utopic main
	sudo apt-key adv --keyserver pgp.mit.edu --recv-keys 5044912E

        deb http://downloads.hipchat.com/linux/apt stable main
        wget -O - https://www.hipchat.com/keys/hipchat-linux.key | apt-key add -

	apt-get update; apt-get install dropbox hipchat

- filezilla = file transfer protocol client (that supports sftp = secure ssh ftp)

### music and video

`sudo apt-get install ubuntu-restricted-extras vlc`

- vlc = movies/music
- ubuntu-restricted-extras = all of the encumbered with licenses packages to generally just watch or listen to stuff :(


#### spotify in ubuntu 15.04
<https://www.spotify.com/us/download/linux/>

`sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys D2C19886`
> trust the spotify repository

> libnss3-1d : Depends: libnss3 (= 2:3.17.4-0ubuntu1) but 2:3.19.2-0ubuntu15.04.1 is to be installed
> spotify is behind the times or only wants to support 14.04 and LTS releases =(

<https://launchpad.net/ubuntu/vivid/amd64/libnss3/2:3.17.4-0ubuntu1>
<https://launchpad.net/ubuntu/wily/amd64/libnss3/2:3.19.2.1-0ubuntu0.15.10.1>

    dpkg -i libnss3_3.17.4-0ubuntu1_amd64.deb
    apt-get install spotify-client
    apt-get -f install

`spotify: error while loading shared libraries: libgcrypt.so.11: cannot open shared object file: No such file or directory`
> what fun, the internet explains 15.04 and 15.10 use the new libgcrypt20 so...

`wget https://launchpad.net/ubuntu/+archive/primary/+files/libgcrypt11_1.5.3-2ubuntu4.2_amd64.deb`
`apt-get install --reinstall spotify-client`

#### pithos is an open source pandora client

- `sudo add-apt-repository ppa:pithos/ppa`
- `sudo apt-get install pithos`


#### more codecs and DVD playback
`sudo apt-get install ffmpeg gstreamer0.10-plugins-bad lame libavcodec-extra`
`sudo /usr/share/doc/libdvdread4/install-css.sh`


## Packages you will probably want to remove

`apt-get remove brltty`
> unless you are using braille on your computer


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


