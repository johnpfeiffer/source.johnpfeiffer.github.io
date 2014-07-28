Title: Tiny Core Linux with Linksys Wireless Card - no CD required installation
Date: 2010-08-04 01:52
Author: John Pfeiffer
Slug: tiny-core-linux-with-linksys-wireless-card-no-cd-required-installation

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Tiny Core Linux is fast and works great... but it does take some effort
to get setup... here's how I got my Linksys wpc54g (v3) pci wireless
card working with WPA - and I didn't burn a tiny core cd!

</p>

You can't repartition a hard drive while actually using it so you'll
most likely need GParted (ie from SystemRescueCD bootable cd) so that
you can repartition / resize to have a spare linux partition... AND use:

</p>

mke2fs -t ext3 /dev/hda3 (or wherever it is...)

</p>

PREREQUISITES:  

grub bootloader installed (preferrably to the MBR)  

tinycore.iso (cd image of tiny core installation/live cd)  

uniextract or isobuster (to open files from iso's)  

ext2fsd (winxp application that allows copying files in/out of an
ext2/ext3 partition)

</p>

tcz files from an FTP repository listed in the section "Install on a
Hard Drive Without Being Connected to the Internet" from  
[http://wiki.tinycorelinux.com/tiki-index.php][]

</p>

wireless-2.6.29.1-tinycore.tcz  

wireless\_tools.tcz  

wpa\_supplicant.tcz  

b43-fwcutter.tcz  

open-ssl-0.9.8m.tcz

</p>

NOTE: hda3 = third partition on the first hard drive, you may need to
use fdisk -l  

or Start -\> Control Panel -\> Administrative Tools -\> Computer
Managemt -\> Disk Management

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

Extract the files from the tinycore.iso (using IsoBuster or
UniExtract)...  

OR if you have linux: mount -o loop /path-to-iso/image-filename.iso
/mnt/custom

</p>

we only need the bzImage and tinycore.gz files... (CAPITAL I ON THE
bzImage!)

</p>

USING Ext2 Volume Manager (ext2fsd) ... browse to your linux partition
and create the following folder

</p>

/boot/tinycore

</p>

copy the "bzimage" and "tinycore.gz" files into the linux partition
/boot/tinycore folder

</p>

Also create the following text file: /tce/onboot.lst

</p>

wireless-2.6.29.1-tinycore.tcz  

wireless\_tools.tcz  

b43-fwcutter.tcz  

openssl-0.9.8m.tcz  

wpa\_supplicant.tcz  

nano.tcz

</p>

BE CAREFUL TO NOT HAVE ANY MISSPELLINGS OR EXTRA SPACES

</p>

Create the directory /tce/optional and copy the above .tcz files into
it.

</p>

TinyCore uses /tce/mydata.tgz to store your files in the /home and /opt
directories.  

(Therefore you could sneak something in if you wanted to...?)

</p>

ALSO, it uses .ashrc (e.g. not BASH command prompt) so any aliases are
in  

/tce/mydata.tgz -\> home/tc/.ashrc

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

MODIFY YOUR GRUB (LEGACY) MENU

</p>

menu.lst

</p>

title tinycore  

root (hd0,2)  

kernel /boot/tinycore/bzimage  

initrd /boot/tinycore/tinycore.gz

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

BUT my wifi depends on this Linksys wpc54g (v3) pci wireless card AND
wpa encryption...

</p>

So I've got "wl\_apsta.o" from my previous debian kernel 2.6.26 (with
all  

of the linux-header and make and compiling commands to get that
binary...)

</p>

Without the correct fw5 (b43 firmware) dmesg will contain (ie kernel
firmware unhappy with wrong linksys driver)

</p>

b43-phy0 ERROR: firmware file "b43/ucode5.fw"

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

COPY wl\_apsta.o into /mnt/hda3/tce  

(with EXT2FSD or usb stick or whatever)

</p>

Rather than hack into my-data.tgz we'll wait until we've booted into
Tiny Core...  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

BOOTING INTO TINY CORE IS VERY FAST... (fingers crossed about the

</p>

Right Click -\> Control Panel  

OR funny icon in the middle with screwdriver = Control Panel

</p>

First check that our "onboot.lst" hack worked: Apps Audit -\> OnBoot -\>
Maintenance

</p>

(could also use: nano /mnt/hda3/tce/onboot.lst )  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -

</p>

WHEN YOU CHOOSE TO SAVE/BACKUP (or when prompted when closing to Save a
Backup)  

mydata.tgz is created and it includes any modifications to
/opt/bootlocal.sh

</p>

since things put in the bootlocal.sh script are run as root... my wifi
hack works...

</p>

nano bootlocal.sh

</p>

mkdir /lib/firmware  

b43-fwcutter -w /lib/firmware /mnt/hda3/tce/wl\_apsta.o  

wpa\_supplicant -B -iwlan0 -c/mnt/hda3/tce/wpa\_supplicant.conf  

udhcpc -H hostname -b -i wlan0

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

the /lib/firmware directory is necessary for the kernel to get the new
drivers  

the b43-fwcutter firmware cutter gets the drivers to the directory  

wpa\_supplicant starts in the background using wlan0 and the config file
wpa\_supplicant.conf

</p>

wpa\_passphrase ssid-network-name \> wpa\_supplicant.conf  

//prompts for the wireless network password, after you type it in press
enter

</p>

udhcpc is busybox's dhcp client using "hostname", in the background on
wlan0

</p>

An alternative configuration in bootlocal.sh for a static ip would be...

</p>

ifconfig wlan0 10.0.0.99 netmask 255.255.255.0 up  

route add default gw 10.0.0.138  

echo "nameserver 10.0.0.138" \> /etc/resolv.conf

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

AFTER I REBOOTED ifconfig wlan0 //shows me my ip address  

ping 10.0.0.138 and ping [http://kittyandbear.net][] //ALL OK!

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

Of course, now I have to install a browser...

</p>

Since tinycore works from the core image and with then added
modifications to be as lean and fast as possible you really need to
explicitly choose what you want on your hard drive AND what you want
started at boot time.

</p>

Right Click -\> AppsBrowser or funny icon on the bottom right (gears)

</p>

File -\> Install Local Extension (anything on your hard drive but not in
onboot.lst)  

By default it lists your TCE/optional directory, double click on the one
you want...

</p>

(If it isn't onboot and it isn't "installed" by above then it's not on
your tinycore yet!)

</p>

OR File -\> AppsBrowser ... when you choose to install something from
the "repository" be prepared to wait for about 5 minutes for it to load
the hundreds of packages...

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - -  

RANDOM TINYCORE NOTES:

</p>

Right Click -\> Shells -\> Shell Dark or funny icon on the bottom left
(terminal with prompt)

</p>

Right Click -\> Control Panel -\> System Stats OR funny icon in the
middle with screwdriver = Panel -\> System Stats

</p>

dmesg TAB shows you the b43 stuff  

cpu is cpu type  

mem is RAM free  

net is network devices installed...

</p>

loadkmap < /usr/share/kmap/uk.kmap

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Linux][]

</div>
</p>

  [http://wiki.tinycorelinux.com/tiki-index.php]: http://wiki.tinycorelinux.com/tiki-index.php
  [http://kittyandbear.net]: http://kittyandbear.net
  [Linux]: http://john-pfeiffer.com/category/tags/linux
