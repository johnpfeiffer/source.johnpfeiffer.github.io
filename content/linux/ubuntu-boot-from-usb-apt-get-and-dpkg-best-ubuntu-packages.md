Title: Ubuntu Bootable USB, apt-get and dpkg, and the best packages to install
Date: 2014-08-20 00:00
Tags: Linux, Ubuntu, USB Boot, Ubuntu Recovery, dpkg, apt-get

[TOC]

If you have a modern computer (BIOS) that can boot from USB it is well worth it since having the latest Ubuntu ISO on DVD tends to pile up extra plastic.

After setting up the Operating System you will need to install some software (packages).

And if you have an SSD drive you will want to optimize your OS to not wear it out unnecessarily.

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

Debian has precompiled packages of binaries and libraries that can very easily be installed via the command line (or GUI) using Advanced Packaging Tool (APT) 

<https://wiki.debian.org/Apt>

Since apt is a wonderful wrapper/manager of dpkg when you're in doubt most likely there is a dpkg command that will do what you need but it may take a lot of research and 8 parameters to do it ;]

<https://en.wikipedia.org/wiki/Advanced_Packaging_Tool>

*Hint: Ubuntu is based upon Debian*

### Pro Tip: Force ipv4 to avoid lengthy IPV6 timeouts

`sudo apt-get -o Acquire::ForceIPv4=true update`

`sudo apt-get -o Acquire::ForceIPv4=true install vim`

`sudo echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4 `
> persistent config to always use ipv4


### apt-cache

`apt-cache search ssh`
> to find packages with the name ssh

`apt-cache search ssh | grep server`
> if there are too many results pipe to grep to filter down the results

`apt-cache show ssh`
> to show the details about a specific package

`apt-cache showpkg ssh`
> to show more general info about a package

`apt-cache depends ssh`
> to show the package dependencies

### apt-get

`sudo apt-get install --dry-run byobu`
> simulate what will happen but do not change the system

`sudo apt-get install --download-only byobu`
> packages are retrieved but not installed

`sudo apt-get install --yes byobu`
> install and pre-emptively answer yes to the yes/no prompt

`sudo apt-get install --reinstall byobu
> reinstall even if the package is installed

`sudo apt-get install --fix-broken byobu
> attempt to fix broken dependencies

<http://manpages.ubuntu.com/manpages/precise/man8/apt-get.8.html>

### apt-key

`sudo apt-key update`
> if apt errors: WARNING: The following packages cannot be authenticated


## Best Ubuntu Packages

> as of Utopic 14.10


	sudo apt-get update
	sudo apt-get install -y byobu build-essential elinks unzip unrar nano vim wget curl ntp rcconf dialog git-core 

	sudo apt-get install -y python-pip && sudo pip install --upgrade pip

> pip is the package manager for python packages (different from the debian OS packages) so useful if you do any python development or run python applications
> An alternative to the usually stale OS pip version is to use the not entirely secure grab the .py file from the internet and run it...
> wget -qO- https://bootstrap.pypa.io/get-pip.py | sudo python


- byobu = console terminal multi screen (survives network disconnects) <http://byobu.co>
- build-essential = tools for compiling and building debian packages <http://packages.ubuntu.com/lucid/build-essential>
- elinks = cli browser (just in case your GUI dies and you need to research) <http://kmandla.wordpress.com/2011/01/13/a-comparison-of-text-based-browsers>
- unzip and unrar = utilities to decompress compressed things
- nano = a simple text editor (much easier than vi/vim for just writing new text)
- wget and curl = utilities to download files
- ntp = network time protocol client daemon to keep your clock in sync
- rcconf = easier way to manage what services start at boot <https://packages.debian.org/jessie/rcconf>
- dialog = user friendly dialog boxes for shell scripts (dependency for rcconf)
- git-core = the distributed version control software that is eating the developer world

- python-setuptools = Sometimes required to install pip  <http://pythonhosted.org/setuptools>
- icedtea = open java (plugin = browser java)

- openvpn = opensource vpn client <https://openvpn.net>
- openconnect = opensource compatible with cisco anyconnect vpn <https://en.wikipedia.org/wiki/OpenConnect>

- jdk = java development kit
- iced-tea-7-plugin = open source java 7 support for browsers

`sudo apt-get install openjdk-8-jdk`
> NOT SURE IN UTOPIC: sudo apt-get install openjdk-7-jre openjdk-7-jdk icedtea-7-plugin

### GUI

**Xubuntu Desktop** is my preferred "lightweight" GUI for Ubuntu: <http://xubuntu.org>

`apt-get install -y chromium-browser pepperflashplugin-nonfree geany keepassx xdiskusage`
`apt-get install -y arandr rdesktop`

- chromium-browser = opensource branch/clone of google chrome browser
- geany = tabbed text notepad (with syntax highlighting)
- keepassx = secure password inventory (has a mini version for  iphone too)
- xdiskusage = graphical view of disk space usage by folder and file
- arandr = multi display gui config

- rdesktop = RDP client
- grdesktop = gnome UI for rdesktop


`sudo echo "autologin-user=ubuntu" >>  /etc/lightdm/lightdm.conf.d/10-xubuntu.conf`
> Better yet use the UI and just choose auto login ;)


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

`sudo apt-get install git-core curl zlib1g-dev build-essential libssl-dev libreadline-dev libyaml-dev libsqlite3-dev sqlite3 \`
  `libxml2-dev libxslt1-dev libcurl4-openssl-dev python-software-properties libgdbm-dev libncurses5-dev automake libtool bison libffi-dev`

    source ~/.rvm/scripts/rvm
    echo "source ~/.rvm/scripts/rvm" >> ~/.bashrc
    rvm install 2.1.2
    rvm use 2.1.2 --default
    ruby -v
    echo "gem: --no-ri --no-rdoc" > ~/.gemrc
    
    gem install rhc

> red hat client for openshift


## SSD Optimization

### Write Logs to tmpfs instead of disk

tmpfs ram (memory) virtual disk will just use memory (which I guess is overly abundant now) instead of wearing out the Solid State Drive

`sudo vi /etc/fstab`

    # /etc/fstab: static file system information.
    #
    # Use 'blkid' to print the universally unique identifier for a
    # device; this may be used with UUID= as a more robust way to name devices
    # that works even if disks are added and removed. See fstab(5).
    #
    # <file system> <mount point>   <type>  <options>       <dump>  <pass>
    # / was on /dev/sda2 during installation
    UUID=b7577587-22db-42f6-95d1-264a24f9dd90 /               ext4    noatime,errors=remount-ro 0       1
    tmpfs    /tmp        tmpfs    defaults,noatime    0  0
    tmpfs    /var/tmp    tmpfs    defaults,noatime    0  0
    tmpfs    /var/log/apparmor    tmpfs    defaults,noatime    0  0
    tmpfs    /var/log/apt    tmpfs    defaults,noatime    0  0
    tmpfs    /var/log/cups    tmpfs    defaults,noatime    0  0
    tmpfs    /var/log/dist-upgrade tmpfs    defaults,noatime    0  0
    tmpfs    /var/log/installer tmpfs    defaults,noatime    0  0
    tmpfs    /var/log/lightdm  tmpfs    defaults,noatime    0  0
    tmpfs    /var/log/unattended-upgrades tmpfs    defaults,noatime    0  0
    
> the tmpfs disks created in my fstab were discovered through trial and error and will differ based on what applications are actually running (Xubuntu!)

> an older simpler example causes errors as applications create /var/log/SOMETHING directories during installation and then expect them on boot every time later

    /dev/sda1 / 	ext4 	noatime,errors=remount-ro 0 1
    
    tmpfs    /tmp        tmpfs    defaults,noatime    0  0
    tmpfs    /var/tmp    tmpfs    defaults,noatime    0  0
    tmpfs    /var/log    tmpfs    defaults,noatime    0  0
    

> here is a list of directories that probably need to be generated
*for dir in apparmor apt cups dist-upgrade fsck gdm installer news samba unattended-upgrades ; do*
*  mkdir -p /var/log/$dir*
*done*

### Customize Grub Boot Options
I prefer seeing my bootup screens so I remove some but add the SSD enhancement

    vi nano /etc/default/grub
        GRUB_TIMEOUT=1
        #	GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
        GRUB_CMDLINE_LINUX_DEFAULT="elevator=noop"
    
    sudo update-grub2
    cat /boot/grub/grub.cfg
        root=UUID=f0ae2c59-83d2-42e7-81c4-2e870b6b255d ro quiet splash elevator=noop

> only prompt for 1 second
> remove the quiet so the console displays all of the boot information
> the noop scheduler is a simple FIFO scheduler which is usually optimal for SSD or virtual machines <https://en.wikipedia.org/wiki/Noop_scheduler> since any OS attempt at optimization may cnoflict with more accurate information from the Disk or Hypervisor
> update-grub2 is to apply the update <https://help.ubuntu.com/community/Grub2>
> manually verify the changes by examining all of the boot menu options (i.e. find the noop line)


    cat /sys/block/sda/queue/scheduler
        [noop] deadline cfq
> list what schedulers are available , <http://www.linuxhowtos.org/System/iosched.htm>, note that noop is selected


*Note: the above command needs to be run as root, but sudo does not work with it on my system. Run sudo -i if you have a problem to get a root prompt.)*

