Title: Tiny Core Linux with Linksys Wireless Card - no CD required installation
Date: 2010-08-04 01:52
Tags: linux, tiny core linux

[TOC]

Tiny Core Linux is fast and works great... but it does take some effort to get setup... 

Here's how I got my Linksys wpc54g (v3) pci wireless card working with WPA - and I didn't burn a tiny core cd!

You can't repartition a hard drive while actually using it so you'll most likely need GParted (ie from SystemRescueCD bootable cd) so that you can repartition / (root) and resize to have a spare linux partition... AND use:

`mke2fs -t ext3 /dev/hda3`
> (or wherever it is...)
> hda3 = third partition on the first hard drive, you may need to use `fdisk -l`
> or Start -> Control Panel -> Administrative Tools -> Computer Management -> Disk Management


### Prerequisites

- grub bootloader installed (preferrably to the MBR)  
- tinycore.iso (cd image of tiny core installation/live cd)  
- uniextract or isobuster (to open files from iso's)  
- ext2fsd (winxp application that allows copying files in/out of an ext2/ext3 partition)

*tcz* files from an FTP repository listed in the section "Install on a Hard Drive Without Being Connected to the Internet" from  <http://wiki.tinycorelinux.net/wiki:start#installing>

- wireless-2.6.29.1-tinycore.tcz  
- wireless_tools.tcz  
- wpa_supplicant.tcz  
- b43-fwcutter.tcz  
- open-ssl-0.9.8m.tcz

### Getting the pieces ready

1. Extract the files from the **tinycore.iso** (using IsoBuster or UniExtract)...  
OR if you have linux: `mount -o loop /path-to-iso/image-filename.iso /mnt/custom`
2. We only need the **bzImage** and **tinycore.gz** files... 
> CAPITAL I ON THE bzImage!
3. USING Ext2 Volume Manager (ext2fsd) ... browse to your linux partition and create the following folder: **/boot/tinycore**
4. Copy the "bzimage" and "tinycore.gz" files into the linux partition **/boot/tinycore folder**
5. Also create the following text file: **/tce/onboot.lst**
    
        wireless-2.6.29.1-tinycore.tcz
        wireless_tools.tcz
        b43-fwcutter.tcz
        openssl-0.9.8m.tcz
        wpa_supplicant.tcz
        nano.tcz
    
> BE CAREFUL TO NOT HAVE ANY MISSPELLINGS OR EXTRA SPACES

Finally, create the directory /tce/optional and copy the above .tcz files into it.

*TinyCore uses /tce/mydata.tgz to store your files in the /home and /opt directories. (Therefore you could sneak something in if you wanted to...?)*

*ALSO, it uses .ashrc (e.g. not BASH command prompt) so any aliases are in /tce/mydata.tgz -> home/tc/.ashrc*


### Modify your Grub (legacy) menu

**menu.lst**
    
    title tinycore  
    root (hd0,2)  
    kernel /boot/tinycore/bzimage  
    initrd /boot/tinycore/tinycore.gz
    

### Oh Wait, Wifi Drivers!

BUT my wifi depends on this Linksys wpc54g (v3) pci wireless card AND wpa encryption...

So I've got **wl_apsta.o** from my previous debian kernel 2.6.26 (with all of the linux-header and make and compiling commands to get that binary...)

Without the correct fw5 (b43 firmware) `dmesg` will contain:

    b43-phy0 ERROR: firmware file "b43/ucode5.fw"
    
> kernel firmware unhappy with wrong linksys driver


COPY **wl_apsta.o** into **/mnt/hda3/tce** (with EXT2FSD or usb stick or whatever)

*Rather than hack into my-data.tgz we'll wait until we've booted into Tiny Core...*

### Booting into Tiny Core Linux

BOOTING INTO TINY CORE IS VERY FAST... (fingers crossed about everything before)

Right Click -> Control Panel or a funny icon in the middle with screwdriver = Control Panel

First check that our "onboot.lst" hack worked: Apps Audit -> OnBoot -> Maintenance

*(could also use: nano /mnt/hda3/tce/onboot.lst)*


**WHEN YOU CHOOSE TO SAVE/BACKUP** (or when prompted when closing to Save a Backup)  

**mydata.tgz** is created and it includes any modifications to **/opt/bootlocal.sh**

since things put in the **bootlocal.sh** script are run as root... my wifi hack works...

`nano bootlocal.sh`
    
    mkdir /lib/firmware  
    b43-fwcutter -w /lib/firmware /mnt/hda3/tce/wl_apsta.o  
    wpa_supplicant -B -iwlan0 -c/mnt/hda3/tce/wpa_supplicant.conf  
    udhcpc -H hostname -b -i wlan0


the /lib/firmware directory is necessary for the kernel to get the new drivers  

the b43-fwcutter firmware cutter gets the drivers to the directory  

wpa_supplicant starts in the background using wlan0 and the config file wpa_supplicant.conf

`wpa_passphrase ssid-network-name > wpa_supplicant.conf`
> prompts for the wireless network password, after you type it in press enter

udhcpc is busybox's dhcp client using "hostname", in the background on wlan0

An alternative configuration in bootlocal.sh for a static ip would be...
    
    ifconfig wlan0 10.0.0.99 netmask 255.255.255.0 up  
    route add default gw 10.0.0.138  
    echo "nameserver 10.0.0.138" > /etc/resolv.conf
    

### Verify after reboot

AFTER I REBOOTED ifconfig wlan0 //shows me my ip address  

`ping 10.0.0.138` and `ping http://kittyandbear.net`
> ALL OK!


### Adding a browser to Tiny Core Linux

Of course, now I have to install a browser...

Since tinycore works from the core image and with then added modifications to be as lean and fast as possible you really need to explicitly choose what you want on your hard drive AND what you want started at boot time.

1. Right Click -> AppsBrowser or funny icon on the bottom right (gears)
1. File -> Install Local Extension (anything on your hard drive but not in onboot.lst)  
1. By default it lists your TCE/optional directory, double click on the one you want...
(If it isn't onboot and it isn't "installed" by above then it's not on your tinycore yet!)

OR File -> AppsBrowser ... when you choose to install something from the "repository" be prepared to wait for about 5 minutes for it to load the hundreds of packages...

### Miscellaneous Tiny Core Linux Notes

Right Click -> Shells -> Shell Dark or funny icon on the bottom left (terminal with prompt)

Right Click -> Control Panel -> System Stats OR funny icon in the middle with screwdriver = Panel -> System Stats

dmesg TAB shows you the b43 stuff  

cpu is cpu type  

mem is RAM free  

net is network devices installed...

loadkmap < /usr/share/kmap/uk.kmap

