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

### Force Apt to use  IPv4 to avoid lengthy IPv6 timeouts

    sudo apt-get -o Acquire::ForceIPv4=true update
    sudo apt-get -o Acquire::ForceIPv4=true install vim
    sudo echo 'Acquire::ForceIPv4 "true";' > /etc/apt/apt.conf.d/99force-ipv4
> update, then install vim, then save the persistent config to always use ipv4

### apt-get

#### updating package indices with apt-get update

Apt contains indices that need to be updated from the upstream repositories

**/etc/apt/sources.list** is the main ubuntu repository listing

**/etc/apt/sources.list.d** is the directory where additional apt repositories can be added (usually from ppa or 3rd party vendors)

- <http://www.debian.org/mirror/mirrors_full> for the Debian package mirror sites
- <http://packages.ubuntu.com/> for a web ui based search of package details

   apt-get clean
> /var/cache/apt/archive folder keeps a copy of the downloaded .deb files
> you will need an internet connection to download again any removed .deb files

    rm -rf /var/lib/apt/lists/*
> remove the indices in case they have gotten orphaned or corrupted, needs to be followed by apt-get update to repopulate

    apt-get update
> use /etc/apt/sources.list and /etc/apt/sources.list.d to update the package indices to determine if there are newer packages available
    deb file:///file_store/archive trusty main universe
> a snippet for how to configure apt to use a local repository (e.g. use reprepro to make a local mirror)


    apt-cache dump
> shows all installed packages

To install netselect, a debian application that allows you to choose the "best" package mirror:
    sudo apt-get install netselect netselect-apt
    netselect-apt


#### installing and force installing with apt

    sudo apt-get install --dry-run byobu
> simulate what will happen but do not change the system

    sudo apt-get install --download-only byobu
> packages are retrieved but not installed

    sudo apt-get install --yes byobu
> install and pre-emptively answer yes to the yes/no prompt

    sudo apt-get install --reinstall byobu
> reinstall even if the package is installed

    sudo apt-get install --fix-broken byobu
> attempt to fix broken dependencies

    DEBIAN_FRONTEND=noninteractive apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install --reinstall byobu
> the most non interactive way to force install a package where all prompts are auto answered such that old configuration files are maintained

- <http://manpages.ubuntu.com/manpages/precise/man8/apt-get.8.html>
- <https://help.ubuntu.com/community/AptGet/Howto>


    apt-get upgrade
> upgrades to the latest version of existing packages, no new packages (so if the new version has new dependencies nothing happens)
    apt-get dist-upgrade
> upgrades to the latest version of existing packages and will try to grab any new dependencies as required

    apt-get install update-manager-core
> newer versions of ubuntu require a helper utility, <http://packages.ubuntu.com/trusty/admin/update-manager-core>

Before you do a major upgrade of Ubuntu you should bring all packages to the latest version... (apt-get update && apt-get dist-upgrade)

    do-release-upgrade -f DistUpgradeViewNonInteractive
> non interactive upgrade to a new version of Ubuntu (hold onto your seat!), often requires a reboot after for kernel upgrades

    lsb_release -a
    cat /etc/lsb_release
    uname -a
> verify that your system has been upgraded (kernel too)

### removing packages with apt
    apt-get remove wget
> uninstall a package
    apt-get purge wget
> remove the package and all files from disk

    apt-get autoremove
> attempt to clean up packages that are no longer needed (i.e. old versions of dependencies or unused kernel images)


### apt-key

`sudo apt-key update`
> if apt errors: WARNING: The following packages cannot be authenticated

## dpkg really manages everything

Underneath apt is dpkg (and similar tools) which actually does all of the hard work but are sometimes hard to use =)

### listing and finding packages with dpkg

    dpkg -l
> lists all of the packages installed (name, version, architecture, description)
    dpkg -l | grep foobar
> lists all of the packages but filters for something specific (i.e. a prefix or partial match)
    dpkg -l packagename > myoutput.txt
> lists whether a specific package is installed or not and redirects the output to a file
    dpkg --get-selections
> lists the package names and the state (installed, uninstalled, etc.)
  dpkg-query -f '${binary:Package}\n' -W
> lists just the package names, slightly more convenient is `apt-cache pkgnames | sort`
    dpkg -S stdio.h
> find a package that contains a specific file
    dpkg -c packagename.deb
> list the contents of the .deb file

<https://wiki.debian.org/ListInstalledPackages>
> you can also manually inspect /var/lib/apt and /var/lib/dpkg

#### dpkg logs

    vi /var/log/dpkg.log
    tail -f /var/log/dpkg.log
> in conjunction with `apt-get upgrade -y`

#### Installing and removing packages with dpkg
    dpkg -i packagename.deb
> install the .deb file, `dpkg -i *.deb` will install all of the .deb files in the current directory
    dpkg -i --force depends packagename.deb
> installs and turns a dependency error into a warning (i.e. libc6 circular dependency)
    dpkg -L packagename
> list the locations of the installed files
    dpkg -s packagename
> shows if the package is installed and information about it, `dpkg -s | grep Version`
> or `dpkg -l | awk '$2=="packagename" { print $3 }'` to only print the version (if it exists)

    dpkg -r packagename.deb
> remove a package but leave the configuration files, also known as `dpkg --remove`
    dpkg --purge
> remove a package and delete all configuration files (even if they have been customized by the user)

    dpkg --force-help

####  to manually install a package (forcefully if synaptic and apt-get are stuck)
    mv /var/lib/dpkg/info/postgresql.* /tmp/
    dpkg --remove --force-remove-reinstreq postgresql-9.1
> do the same for postgresql-common and other packages

apt-get install postgresql-9.1
apt-get purge postgresql-9.1 postgresql-client-9.1 postgresql-common postgresql-client-common
> in order to have apt-get remove all of the binaries




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

sudo apt-get install openconnect network-manager-openconnect network-manager-openconnect-gnome

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

- chromium-browser = opensource branch/clone of google chrome browser, 
- - maybe srware.net with privacy badger and adblock plus (fanboy block lists) too?
- geany = tabbed text notepad (with syntax highlighting)
- keepassx = secure password inventory (has a mini version for iphone as well)
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
> what fun, the internet explains 15.04 (vivid) and 15.10 (wily) use the new libgcrypt20 so...


    wget https://launchpad.net/ubuntu/+archive/primary/+files/libgcrypt11_1.5.3-2ubuntu4.2_amd64.deb
    dpkg -i libgcrypt*.deb
    apt-get install --reinstall spotify-client


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

    sudo vi /etc/fstab


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

