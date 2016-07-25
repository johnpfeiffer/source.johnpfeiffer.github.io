Title: Systeminfo hardware diagnostic listing ram processor ubuntu version ps top iotop lshw dmidecode
Date: 2009-11-11 21:42:50
Tags: linux, systeminfo, hardware, diagnostic, listing, ram, processor, ubuntu, version, top, iotop, lshw dmidecode

[TOC]

It is often critical to know exactly what is going on with your system.  
Linux is the defacto winner of the server world in large part because there are so many good tools.
Especially since open source often needs to detect and reverse engineer drivers and compatibility for manufacturer hardware.

## higher level utilities for process

    ps
> processes with their virtual memory size

    top
> processes and cpu usage, type q to quit

       q = quit
       s = change interval of refresh (default is 3 seconds)
       u = type a User and only show processes from that User
       > = choose to sort by the next column
       < = choose to sort by the previous
    
    ps -a
> tree of all processes
    
    ps -ef
> full output of all processes including start time, uptime, cmd
    
    
    ps -eo pid,ppid,rss,vsize,pcpu,pmem,cmd -ww --sort=pid
    
    ps -eo pid,ppid,rss,vsize,pcpu,pmem,cmd -ww --sort=rss
    
    rss = ram usage
    vsize = virtual memory include swap as well
    
    
    ps -eo rss,vsz,pid,cmd,cputime | sort -n | tail -20
    	(this will show you possible memory leaks)
    
    
    ps guxca
    
so the free command is funny  ( http://kbase.redhat.com/faq/docs/DOC-1139 )
    
the amount +/- buffers/cache is the "real" amount available to the system 
(if the "lazy" kernel decided to free up something that's been buffered previously in order for a new app which needs the memory)
    
    <Physically Used Memory> = <Actual used memory> + <buffers> + <cache>
    
    <Physically Free Memory> = <Total Physical Memory> - <Actual used memory> - <buffers> - <cache>
    
    <Memory free for Applications> = <Total Physical Memory> - <Actual used memory>
    
    <Memory used  by Applications> = <Actual used memory> - <buffers> - <cache>


## OS Version
    cat /etc/issue
> just the version number of the OS, e.g. ubuntu shows 16.04

    cat /etc/debian_version
> only on debian/ubuntu... and shows squeeze/sid for natty 11.04, wheezy/sid for 11.10, jessie/sid
- <https://www.debian.org/releases/>

    cat /etc/lsb-release
> full ubuntu version    

    lsb_release -a
> a command to shows all of the ubuntu version information, e.g. cat /etc/lsb-release

    lsb_release -c
    Codename:	natty
> a command to just show the codename
    
## /proc is realtime info about the system
    
    cat /proc/version
    cat /proc/cpuinfo
> note: if there's "lm" (aka long mode) in the flags: fpu vme etc. area then you have 64bit capability...

    cat /proc/meminfo
    head -1 /proc/meminfo
    
    ls -ld /proc/somepid
> get some info about a specific process running via its pid number
  
## kernel information  
    uname -a
> kernel version, x64 or 32 bit, machine name , multi-processor SMP, etc.

    getconf -a
> another way to get info about your kernel

## Memory and disk space 

    free -m
>  free memory in megabytes including swap/buffer usage)

    vmstat
> /virtual memory stats

    df -h
> free disk space in human readable numbers

    du
> disk usage for a directory and subdirectories - needs parameters , like du -s (summary)

    stat -f / -c "%a * %s / 1024" | bc
> get the specific amount of free space available from the root file system, stat --help
> bc is a handy "built in calculator"
    
## hardware listing

    fdisk -l
> shows all of the hard disk devices available - what os, bootable, etc.

    lshw
> exhaustive info about the hardware (tree by CLASS)

    lshw -class network
> hardware listing focused identification of Physical Network Adapter to logical name like eth0/wlan0

    lshw -c video
> show the video hardware

    lspci
> lists devices connected to the PCI bus requires pciutils.deb depends on libpci3 , all the pci hardware including usb bridges,agp cards
> common usages are "lspci | grep vga" or "lspci | grep eth"	

    lsusb
> will show all the usb devices like mice, etc

    dmidecode
> listing of system hardware according to the BIOS (so not always reliable)
<http://www.nongnu.org/dmidecode/>
    
    lsmod
> installed driver modules

    xdpyinfo
> /xserver info
    
    ls -l /lib/libc-*.so /lib/libc.so*
    ldd --version
> version of linux glibc
    
    dmesg
> kernel messages = all the devices the kernel has found like hard disks,cdroms,etc

    dmesg | grep CPU
    dmesg | grep mem
    dmesg | tail
> shows the last 10 lines of the hardware boot up
    	

    /etc/modprobe.conf (kernel 2.6)

> fedora/redhat

    /etc/modules.conf (kernel 2.4)
    

    /etc/conf.modules (or for older systems)

## disk IO

    iotop
> like top but focused on I/O , <http://linux.die.net/man/1/iotop>
    
## network

    ifconfig -a
> shows all of the ethernet devices available
    
    ls -l /sys/class/net/eth0
    
    apt-get install bcm43xx-fwcutter
    mkdir -p /lib/hotplug/firmware; cp /lib/firmware/*.fw /lib/hotplug/firmware
        
## software inventory and listing

    dpkg --list
    dpkg -l | grep foo
    dpkg --get-selections
> debian/ubuntu listing of installed software packages 
    
    pip freeze
    pip freeze | grep foo
> python packaging manager listing of packages
    
    rpm -qa
> red hat installed software
    
    
    tail -f /var/log/secure         //login logs
    tail -f /var/log/maillog            //mail logs

    last
    last -f btmp
> last logins and then the last bad logins
    
    cat /proc/meminfo
    
> MemTotal = Total amount of physical RAM, in kilobytes.
>  MemFree  The amount of physical RAM, in kilobytes, left unused by the system. 
    
    note that MemTotal - MemFree should match what free and top show you...
    
    Slab The total amount of memory, in kilobytes, used by the kernel to cache data structures for its own use. 
    
    Mapped The total amount of memory, in kilobytes, which have been used to map devices, files, or libraries using the mmap command. 
    
    So all of your processes from TOP + Slab + Mapped
    
    free
                 total       used       free     shared    buffers     cached
    Mem:        262364      78424     183940          0       2412      37756
    -/+ buffers/cache:      38256     224108
    Swap:       524280          0     524280
    
    used + buffer + cached = 118,592
    143,772
    
    
    top - 20:39:34 up  2:19,  1 user,  load average: 0.00, 0.00, 0.00
    Tasks:  55 total,   1 running,  54 sleeping,   0 stopped,   0 zombie
    Cpu(s):  0.0%us,  0.0%sy,  0.0%ni, 99.2%id,  0.0%wa,  0.0%hi,  0.0%si,  0.8%st
    Mem:    262364k total,    78408k used,   183956k free,     2428k buffers
    Swap:   524280k total,        0k used,   524280k free,    37756k cached
    
    
     3899 root      20   0 68112 2984 2316 S    0  1.1   0:00.42 sshd
     3575 klog      20   0  5492 2260  420 S    0  0.9   0:00.06 klogd
     3903 root      20   0 17544 1796 1328 S    0  0.7   0:00.16 bash
     4490 root      20   0 18860 1200  932 R    0  0.5   0:00.04 top
     3596 root      20   0 50916 1164  680 S    0  0.4   0:00.00 sshd
     3856 Debian-e  20   0 43432 1000  616 S    0  0.4   0:00.00 exim4
        1 root      20   0  4020  944  656 S    0  0.4   0:00.36 init
     2300 root      16  -4 16832  932  372 S    0  0.4   0:00.46 udevd
     3874 root      20   0 18616  860  668 S    0  0.3   0:00.04 cron
     3550 syslog    20   0 12296  752  564 S    0  0.3   0:00.10 syslogd
     3510 root      20   0  3864  588  492 S    0  0.2   0:00.00 getty
     3513 root      20   0  3864  588  492 S    0  0.2   0:00.00 getty
     3516 root      20   0  3864  588  492 S    0  0.2   0:00.00 getty
     3572 root      20   0  8132  588  476 S    0  0.2   0:00.04 dd
     3509 root      20   0  3864  584  492 S    0  0.2   0:00.00 getty
     3512 root      20   0  3864  584  492 S    0  0.2   0:00.00 getty
     3898 root      20   0  3864  584  492 S    0  0.2   0:00.00 getty
    
                                17,996 + 15,832 + 3,552 = 37,380... so still short of 78,424
    TOP + Slab + Mapped
    
    
<http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/>
    
<http://backtrack.offensive-security.com/index.php/HCL:Wireless#Linksys_WPC54G_v3>
    
     Linksys WPC54G v3
    
        * Driver : bcm43xx/b43
        * Chipset : Broadcom Corporation BCM4318 [AirForce One 54g] 802.11g Wireless LAN Controller (rev 02)
        * Subsystem: Linksys WPC54G-EU version 3 [Wireless-G Notebook Adapter] 
    
Monitor mode currently supported but injection may or may not work with bcm43xx. Apparently a new driver is coming out dubbed as b43 and is only available in either kernel >=2.6.24 and/or wireless-2.6 git. Injection will work after patching b43 via mac80211 stack. bcm43xx driver will soon be deprecated and for this chipset it will not indicate PWR levels with airodump-ng. 
    
    http://linuxwireless.org/en/users/Drivers/b43
    lspci -vnn | grep 14e4
    
    0001:01:01.0 Network controller [0280]: Broadcom Corporation BCM4318 [AirForce One 54g] 802.11g Wireless LAN Controller [14e4:4318] (rev 02)
- - -    
    
    cat /proc/interrupts
> a file listing of all the interrupt IRQs used by your system
    
    e.g.
    
              CPU0
       0:  2707402473          XT-PIC  timer
       1:          67          XT-PIC  i8042
       2:           0          XT-PIC  cascade
       5:      411342          XT-PIC  eth1
       8:           1          XT-PIC  rtc
      10:     1898752          XT-PIC  eth0
      11:           0          XT-PIC  uhci_hcd
      12:          58          XT-PIC  i8042
      14:     5075806          XT-PIC  ide0
      15:         506          XT-PIC  ide1
    NMI:           0
    ERR:          43
    
if two devices try to use the same interrupts or memory access address they will be in conflict (won't work)
    
- - -
## dmidecode in depth example
DMI DECODE  for how much physical ram you COULD have...
    
    dmidecode > hw.txt
> dump the whole thing to a text file
    
    less hw.txt
> lots of info!
    
    System Information
            Manufacturer: HP
            Product Name: ProLiant ML310 G5
            Version: Not Specified
            Serial Number: 
            UUID: 
            Wake-up Type: Power Switch
            SKU Number: 
            Family: ProLiant
    
    Processor Information
            Socket Designation: Proc 1
            Type: Central Processor
            Family: Xeon
            Manufacturer: Intel
            ID: 77 06 01 00 FF FB EB BF
            Signature: Type 0, Family 6, Model 23, Stepping 7
    
    
            External Clock: 1333 MHz
            Max Speed: 4800 MHz
            Current Speed: 2500 MHz
            Status: Populated, Enabled
            Upgrade: ZIF Socket
            L1 Cache Handle: 0x0710
            L2 Cache Handle: 0x0720
            L3 Cache Handle: 0x0730
            Serial Number: Not Specified
            Asset Tag: Not Specified
            Part Number: Not Specified
            Core Count: 4
            Core Enabled: 4
            Thread Count: 4
            Characteristics:
                    64-bit capable
    
- - -
BECAUSE THERE IS SO MUCH INFORMATION PEOPLE USE TRICKS TO GET ONLY A CERTAIN PART

    dmidecode | perl -ne '$memory += $1 if /^\t+Size: (\d+)/ ; END { print "$memory\n" }'
    
    dmidecode | perl -ne '$num_procs += 1 if /^\t+Type: Central Processor/ ; END { print "$num_procs\n"}'
    
    decode, biosdecode, and vpddecode		//alternates to dmidecode?

- - -
DMI SHORT CODES MAKE IT EASIER TO GET A SPECIFIC CHUNK
    
    dmidecode --type 0
> get info on the bios
    
    dmidecode --type 16
    
    # dmidecode 2.9
    SMBIOS 2.4 present.
    
    Handle 0x1000, DMI type 16, 15 bytes
    Physical Memory Array
            Location: System Board Or Motherboard
            Use: System Memory
            Error Correction Type: Single-bit ECC
            Maximum Capacity: 8 GB
            Error Information Handle: Not Provided
            Number Of Devices: 4
    
    
    # Type	Short Description
    0	BIOS 
    1	System 
    2	Base Board 
    3	Chassis 
    4	Processor 
    5	Memory Controller 
    6	Memory Module 
    7	Cache 
    8	Port Connector 
    9	System Slots 
    10	On Board Devices 
    11	OEM Strings 
    12	System Configuration Options 
    13	BIOS Language 
    14	Group Associations 
    15	System Event Log 
    16	Physical Memory Array 
    17	Memory Device 
    18	32-bit Memory Error 
    19	Memory Array Mapped Address 
    20	Memory Device Mapped Address 
    21	Built-in Pointing Device 
    22	Portable Battery 
    23	System Reset 
    24	Hardware Security 
    25	System Power Controls 
    26	Voltage Probe 
    27	Cooling Device 
    28	Temperature Probe 
    29	Electrical Current Probe 
    30	Out-of-band Remote Access 
    31	Boot Integrity Services 
    32	System Boot 
    33	64-bit Memory Error 
    34	Management Device 
    35	Management Device Component 
    36	Management Device Threshold Data 
    37	Memory Channel 
    38	IPMI Device 
    39	Power Supply

