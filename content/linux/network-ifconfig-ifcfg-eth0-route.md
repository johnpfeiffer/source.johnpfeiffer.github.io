Title: Network ifconfig ifcfg static and dhcp eth0 route wifi wpa
Date: 2009-08-06 19:22:07
Tags: linux, network, ifconfig, ifcfg, eth0, route, wifi, wpa, dhcp

[TOC]

Networking usually has 3 critical configuration components:

1. IP address config
1. Default route (to the gateway)
1. DNS (Domain Name System)

> I am skipping installing physical network cards and network drivers because we're "all in the cloud" now (or at the very least virtualized)

## Quick Awesome Tips

    ifconfig | grep Bc
> get the ip addresses of all cards

    ip route get 8.8.8.8 | awk 'NR==1 {print $NF}'
> badass internet tip on how to get the ip address of the outbound network card

    /sbin/ifconfig | grep 'inet' | tr -s ' ' | cut -d ' ' -f3 | cut -d ':' -f2
> one liner to get just the ip addresses


## Hardware

    lspci | grep -i ethernet
> displays ethernet hardware

    dmesg | grep eth
> displays ethernet devices registered during bootup

## Diagnostics

### View current configuration and Loopback 

    ifconfig
> simples way to see the current interfaces and configurations

    ifconfig lo    

    lo Link encap:Local Loopback
    inet addr:127.0.0.1 Mask:255.0.0.0
    UP LOOPBACK RUNNING MTU:16436 Metric:1
    RX packets:787 errors:0 dropped:0 overruns:0 frame:0
    TX packets:787 errors:0 dropped:0 overruns:0 carrier:0
    collisions:0 txqueuelen:0
    RX bytes: TX bytes:
> see a specific interface, the loopback interface is the simple test of your tcp/ip stack     

    ifconfig -a
> you will most likely see eth0 for wired interfaces and wlan0 for wireless
> and the will include the following line with the interrupt IRQ and memory access address

    Interrupt:11 Base address:0x1820

> You may also see any network bridges

###  Current Network Connections with netstat

    netstat -i
> displays active interfaces

    netstat -an --inet
> numeric and internet protocols only

## Configuring the Network

    /etc/init.d/networking restart
> after making config file changes you should restart the network service (this will reset any manual configuration)

    dhcpcd eth0
> runs the DHCP client on eth0 to attain an IP address in the 192.168.1.x range

### Permanent persistent configuration

#### /etc/network/interfaces

the "old" tried and true way of configuring interfaces <https://wiki.debian.org/NetworkConfiguration>

    auto lo
    iface lo inet loopback
    
    auto eth0
    iface eth0 inet dhcp
> sets eth0 to be a dhcp client at boot or "ifup eth0"

    sudo vi /etc/network/interfaces
        auto eth0
        iface eth0 inet static
        	address 172.24.32.123
        	netmask 255.255.254.0
        	network 172.24.32.0
        	broadcast 172.24.32.255
        	gateway 172.24.32.1

        	# dns-* options are implemented by the resolvconf package, if installed
        	dns-nameservers 172.24.32.10 172.24.32.11
        	dns-search example.com

> permanently configure to a static ip address which survives reboot or sudo /etc/init.d/networking restart

> network and broadcast are often optional (e.g. for /24 networks)


#### IEEE 802.1x WPA Supplicant

- <https://wiki.archlinux.org/index.php/WPA_supplicant>
- <https://help.ubuntu.com/community/Network802.1xAuthentication>

    sudo apt-get install wpasupplicant
> install the wpa supplicant binary

Example wpa_suplicant configuration file:

    /etc/wpa_supplicant/wpa_wired.conf
        network={
        key_mgmt=IEEE8021X
        eap=PEAP
        phase2="auth=MSCHAPV2"
        identity="MYUSERNAME"
        password="MYPASSWORD"
      }

To manually run wpa_supplicant for a wired connection: `wpa_supplicant -D wired -i enp0s25 -c /etc/wpa_supplicant/wpa_wired.conf`

To incorporate this into your /etc/network/interfaces file...

    # interfaces(5) file used by ifup(8) and ifdown(8)
    auto lo
    iface lo inet loopback
    
    auto enp0s25
    iface enp0s25 inet dhcp
        wpa-driver wired
        wpa-conf /etc/wpa_supplicant/wpa_wired.conf
        dns-nameservers 172.28.4.120 172.24.0.180

> as of 16.04 ubuntu uses a different method of determining the ethernet interface names (so not eth0, instead enp0s25)

If you wish to obfuscate with a hash (instead of plaintext in the conf file)

    echo -n MYPASSWORD | iconv -t utf16le | openssl md4
        (stdin)= db3236251234123412341234

In the wpa supplicant config update the password line to be:

    password=hash:db3236251234123412341234


### Configure your IP Address Manually

Manual, ad-hoc network configuration - not stored permanently (lost at reboot/power off/network service restart)

    /sbin/ifconfig eth0 192.168.1.11 
> auto configures network to 192.168.1.0 and netmask 255.255.255.0, 10.0.0.1 is different!

    ifconfig eth0 10.0.0.1 
    ifconfig eth0 netmask 255.255.255.0 
    ifconfig eth0 broadcast 10.0.0.255
> ALTERNATIVELY you can specify each parameter

    ifconfig -a
> shows the results, run inbetween will show the incremental changes

    ifconfig eth0 10.0.0.1 netmask 255.255.255.0 broadcast 10.0.0.255 up
> or configure all of the parameters at once

    route add default gw 192.168.1.1
> ensures communication with our gateway/router/modem

    route add add -net 10.0.0.0 netmask 255.0.0.0 gw 10.10.10.1 dev eth0
> add another route send 10.x.x.x traffic to a different network gateway (10.10.10.1 via device/interface eth0)

    up route add -net 192.168.0.0 netmask 255.255.0.0 gw 10.10.10.1
> define a permanent, persistent static route

    ifdown eth0
> manually disables the eth0 device

    ifup eth0
> manually enables the eth0 device

 
#### ALTERNATIVELY the more "modern" commands with ip

    /bin/ip addr 192.168.1.11 dev eth0
    ip link show
    
    1: lo: <LOOPBACK,UP> ...
    2: eth0: <BROADCAST,MULTICAST> ...
        	link/ether 00:00:00:00:00:00


    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
## Wireless

Can be configured manually substituting wlan0 instead of eth0
    
    iwlist scan
    
    iwconfig
> sets up your wireless settings (e.g. wpa/wep and passwords/keys)

- <http://linux.die.net/man/8/iwconfig>


## DNS & NAME RESOLUTION
    
    /etc/resolv.conf
> the linux file for name resolution, can be filled automatically if using DHCP
    
    search name-of-domain.com  - Name of your domain or ISP's domain if using their name server
    nameserver XXX.XXX.XXX.XXX - IP address of primary name server
    nameserver XXX.XXX.XXX.XXX - IP address of secondary name server
    
    /etc/hosts
> old system for putting a name to an ip address on the local machine <https://en.wikipedia.org/wiki/Hosts_(file)>

> can fill in and supersede info on machines not covered by your DNS
    
    127.0.0.1         your-node-name.your-domain.com  localhost.localdomain  localhost 
    XXX.XXX.XXX.XXX   node-name
    
IF USING STATIC RESOLUTION (MANUAL UPDATING OF THE /etc/resolv.conf)

    sudo apt-get remove resolvconf   (this utility will automatically overwrite your changes above!)
    
    
HOSTNAME is how your computer is recognized on the (local) network
    
    hostname newhostname
> manually changes the hostname (not permanent)

    hostnamectl set-hostname NEWHOSTNAME
> convenient way to set the hostname dynamically AND persistently

    sysctl -w kernel.hostname="newhostname"
> low level alternative  <http://linux.die.net/man/8/sysctl>

## RED HAT AND CENTOS 5

You must modify the config files (but the changes will survive reboot =)

    sudo vi /etc/sysconfig/network-scripts/ifcfg-eth0
    
    DEVICE=eth0
    BOOTPROTO=                          //could be dhcp?
    IPADDR=192.168.1.59
    NETMASK=255.255.255.0
    BROADCAST=255.255.255.255
    NETWORK=192.168.1.0
    DNS1=192.168.1.30
    DNS2=192.168.1.3
    
    HWADDR=08:00:27:B4:79:93
    ONBOOT=yes
    DHCP_HOSTNAME=madics-vm
    GATEWAY=192.168.1.3
    TYPE=Ethernet
    
    /etc/init.d/network restart
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    AUTOMATIC CONFIGURATION OF YOUR IP ADDRESS
    
    // modify the file /etc/network/interfaces and then you can run ifup/ifdown
    // the default linux config file for setting up networking (at bootup)
    // EXAMPLE of the config file from ubuntu server (could be debian too)
    
    auto lo
    iface lo inet loopback
    
    #sets eth0 to be a dhcp client at boot or "ifup eth0"
    auto eth0
    iface eth0 inet dhcp
    
    auto ath0           //atheros chip based networking
    auto wlan0          //wireless chip based networking
    
    /etc/init.d/networking restart	//required to apply changes to the above files
    
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    net-setup eth0		//system rescue cd
    
    /etc/sysconfig/network		//redhat/fedora file to configure the network
    NETWORKING=yes
    HOSTNAME=my-hostname      - Hostname is defined here and by command hostname
    FORWARD_IPV4=true         - True for NAT firewall gateways and linux routers. 
                                False for everyone else - desktops and servers.
    GATEWAY="XXX.XXX.XXX.YYY" - Static IP configuration. Gateway not defined here for DHCP client.
    
    
    ifcfg-eth0		//file on fedora /etc/sysconfig/network-scripts autoconfigure on boot or ifup
    DEVICE=eth0
    BOOTPROTO=static			//could be set to =dhcp
    IPADDR=192.168.1.100			//unnecessary for dhcp 
    NETMASK=255.255.255.0			//unnecessary for dhcp
    ONBOOT=yes
    BROADCAST=192.168.1.255			//optional setting, unnecessary for dhcp
    NETWORK=192.168.1.0			//optional setting, unnecessary for dhcp
    
    
        * TYPE=Ethernet			//RHEL4/FC3 addition
        * HWADDR=XX:XX:XX:XX:XX:XX		//RHEL4/FC3 addition
        * GATEWAY=XXX.XXX.XXX.XXX		//RHEL4/FC3 addition
    
    
    /sbin/netconfig			//redhat console tool for configuring network
    
    /etc/rc.d/rc.local	//redhat place for custom boot up scripts - network config can be done here as well
    
    /etc/sysconfig/network
>     //change the hostname config file - hostname at boot


    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    MULTIPLE IP ADDRESSES ON A SINGLE NIC (VIRTUAL SUBINTERFACE or ALIAS)
    
    NOTE: it's not necessarily a good idea to have two network interfaces in the same network space
    
    IP Alias is standard in kernels 2.0.x and 2.2.x
    (if required to load into the kernel.../sbin/insmod /lib/modules/`uname -r`/ipv4/ip_alias.o)
    
    ifconfig wlan0 192.168.1.11 netmask 255.255.255.0 up
    ifconfig wlan0:0 192.168.1.111 netmask 255.255.255.0 up
    ifconfig wlan0:1 192.168.1.211 
    
    /etc/sysconfig/network-scripts/ifcfg-wlan0:0   	//file on fedora to manage virtual subint on boot
    DEVICE=wlan0:0
    ONBOOT=yes
    BOOTPROTO=static
    IPADDR=192.168.1.99
    NETMASK=255.255.255.0
    
    //using the above file can allow the easy enable/disable of device via
    ifup wlan0:0
    ifdown wlan0:0
    
    //Note that if the parent device is disabled (ifdown wlan0) all "aliases" or subint's are disabled

## ROUTING and DEFAULT GATEWAY
    
    netstat -rn
> shows the current routing table (numeric only so not trying to resolve each ip address to a hostname)
    
    /sbin/route add default gw 192.168.1.1 wlan0
> all unknown traffic will go through wlan0
    
    route add -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.1 wlan0		
> traffic for 10.0.0.0 network will be sent to ip address 10.0.0.1
    
    route add -net 127.0.0.0
    route add -net 192.168.1.0 dev eth0
    route add -host 192.168.1.11 dev eth0
    route add -host 192.168.1.111 dev eth0:0
    route add -host 192.168.1.211 dev eth0:1

### Removing a route

    /sbin/route del -net 192.168.2.0 netmask 255.255.255.0
    route del -net 10.0.0.0 netmask 255.255.255.0 gw 10.0.0.254
> remove a route
    
for some reason other variations don't work
    
THEN
    /sbin/route del -net default gw 192.168.2.1
    
THEN 
    route add default gw 192.168.1.3
    
    route -n

## EXAMPLE COMPLICATED STATIC ROUTE SYSTEM
    
     auto eth0 
     iface inet static
     address 10.10.64.190
     netmask 255.255.254.0
     
     gateway 10.10.64.1
     
     auto eth1
     iface inet static
     address 10.10.66.190
     netmask 255.255.254.0
     
     up route add -net 0.0.0.0 netmask 0.0.0.0 gw 10.10.64.1 eth0
     up route add -net 10.0.0.0 netmask 255.0.0.0 gw 10.10.66.1 eth1
     up route add -net 172.16.0.0 netmask 255.240.0.0 gw 10.10.66.1 eth1
     up route add -net 192.168.0.0 netmask 255.255.0.0 gw 10.10.66.1 eth1
     

## PPPoE CONFIGURATION

The PPPOE configuration will create a software-based virtual interface named ppp0 that will use the physical Internet interface eth0    
    
    rp-pppoe-3.5-8.i386.rpm 

