Title: firewall iptables ufw ssh https nat forwarding redirect
Date: 2009-01-01 00:00:00
Tags: linux, iptables, firewall, NAT, ufw

[TOC]

iptables is the tool to create a firewall in linux (manipulate the tables provided by the kernel firewall aka the netfilter)
<https://en.wikipedia.org/wiki/Netfilter>

    which iptables
    sudo /sbin/iptables --version

## Most common commands

    iptables -nvL
> output the rules in the default "FILTER" table (INPUT, OUTPUT) in numeric , verbose, List all rules

<http://ipset.netfilter.org/iptables.man.html>

    iptables -nvL --line-numbers
> numeric so no hostname lookups, verbose, List the rules in the chain

## Interactive commands

    iptables -D INPUT 5
> delete the 5th line

*don't forget chmod +x firewall-script-filename.sh and /sbin/service iptables save*

### iptables allow ping with a ratelimit

    iptables -A INPUT -p icmp -m limit --limit 10/second -j ACCEPT
    iptables -A OUPUT -p icmp -j ACCEPT
    > allow 10 inbound icmp packets (not tcp nor udp) per second and allow all icmp traffic outbound

    iptables -A INPUT -p icmp --icmp-type echo-request -j ACCEPT
    > echo-request = 8 in numeric

    iptables -A OUTPUT -p icmp --icmp-type echo-reply -j ACCEPT
    > Allow outgoing ping replies, echo reply = 0 in numeric


### Clean out the old iptables - very insecure settings

    iptables -F
    iptables --delete-chain
    iptables -t nat -F
    iptables -t mangle -F

    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT
> Flush out all of the iptables and delete all of the chains (including the nat and mangle tables)
> Set the default policies to accept all packets


### Allow SSH, ping, and Established but block all by default

    :::bash
    #!/bin/sh
    iptables -I INPUT 1 -i lo -j ACCEPT
    iptables -I OUTPUT 1 -o lo -j ACCEPT
    > Always allow the loopback device
      
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT
    > allow SSH server to accept connections
    
    iptables -A INPUT -i eth1 -p tcp --dport 22 -j ACCEPT
    iptables -A OUTPUT -o eth1 -p tcp --sport 22 -j ACCEPT
    > ssh server on eth1 on port 22
    
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT DROP
    > default to block all traffic
    
    iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
    > Accept packets belonging to established and related connections
    
    iptables -A INPUT -i eth1 -p icmp --icmp-type echo-request -j ACCEPT
    > Allow incoming ping requests from eth1 , echo-request = 8 in numeric
    
    iptables -A OUTPUT -o eth1 -p icmp --icmp-type echo-reply -j ACCEPT
    > Allow outgoing ping replies to eth1 , echo reply = 0 in numeric
    
- - -

    cat /proc/sys/net/ipv4/ip_forward
    echo 1 > /proc/sys/net/ipv4/ip_forward
> enable packet forwarding by the kernel, required to enable routing (especially with dual nics)


### bash script to set iptables during init.d

    :::bash
    #!/bin/bash
    # script to set the initial firewall state as very restrictive
    # chmod +x SCRIPTNAME.sh
    # cd /etc/init.d
    # sudo update-rc.d SCRIPTNAME.sh defaults
    # sudo update-rc.d -f SCRIPTNAME.sh remove
    # or add it to /etc/rc.d/rc.local (which runs once after all other scripts)
    
    # clear any existing firewall
    iptables -F
    iptables -X
    iptables -F -t mangle
    iptables -F -t nat
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT DROP
    
    # Protect against SYN flood attacks (see http://cr.yp.to/syncookies.html).
    echo 1 > /proc/sys/net/ipv4/tcp_syncookies
    
    # Allow loopback
    iptables -A INPUT -i lo -j ACCEPT
    iptables -A OUTPUT -o lo -j ACCEPT
    
    # Allow DNS queries
    iptables -A OUTPUT -p udp --dport 53 -m state --state NEW -j ACCEPT
    iptables -A INPUT -p udp --sport 53 --dport 1024:65535  -m state --state ESTABLISHED -j ACCEPT
    
    # Allow NTP (query time server)
    iptables -A INPUT -p udp --dport 123 -j ACCEPT
    iptables -A OUTPUT -p udp --sport 123 -j ACCEPT
    
    # Allow SSH on port 22
    iptables -A INPUT -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -A OUTPUT -p tcp --sport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
    
    # Allow incoming HTTPS
    iptables -A INPUT -p tcp -s 0/0 --sport 1024:65535 --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -A OUTPUT -p tcp -s 0/0 --sport 443 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT
    
    # Allow outgoing HTTPS (note state for INPUT is only ESTABLISHED)
    iptables -A OUTPUT -p tcp --dport 443 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -A INPUT -p tcp -s 0/0 --sport 443 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT

### Web Server

    :::bash
    #!/bin/sh
    iptables -F
    iptables --delete-chain
    iptables -t nat -F
    iptables -t mangle -F
    
    iptables -P INPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -P OUTPUT ACCEPT
    
    # LOOPBACK 127.0.0.1
    iptables -I INPUT 1 -i lo -j ACCEPT
    iptables -I OUTPUT 1 -o lo -j ACCEPT
    
    # SSH
    iptables -A INPUT -p tcp --dport 22 -j ACCEPT
    iptables -A OUTPUT -p tcp --sport 22 -j ACCEPT
    
    # NTP
    iptables -A INPUT -p udp --dport 123 -j ACCEPT
    iptables -A OUTPUT -p udp --sport 123 -j ACCEPT
    
    # DNS
    iptables -A OUTPUT -p udp --dport 53 -m state --state NEW -j ACCEPT
    iptables -A INPUT -p udp --sport 53 --dport 1024:65535  -m state --state ESTABLISHED -j ACCEPT
    
    # HTTP
    iptables -A INPUT -p tcp --dport 80 -j ACCEPT
    iptables -A OUTPUT -p tcp --sport 80 -j ACCEPT
    
    
    # DROP ALL UNDEFINED PACKETS
    iptables -P INPUT DROP
    iptables -P FORWARD DROP
    iptables -P OUTPUT DROP
    
    # PING
    # iptables -A INPUT -p icmp -m limit --limit 6/second -j ACCEPT
    # iptables -A OUPUT -p icmp -j ACCEPT


### Web and XMPP Server

`vi /etc/iptables.rules.xmpp`

    :::bash
	*filter
	:INPUT DROP [3:572]
	:FORWARD DROP [0:0]
	:OUTPUT ACCEPT [10:1744]
	-A INPUT -i lo -j ACCEPT
	-A INPUT -p tcp -m tcp ! --tcp-flags FIN,SYN,RST,ACK SYN -m state --state NEW -j DROP
	-A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
	-A INPUT -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
	-A INPUT -p tcp -m tcp --dport 80 -m state --state NEW -j ACCEPT
	-A INPUT -p udp -m udp --dport 161 -m state --state NEW -j ACCEPT
	-A INPUT -p tcp -m tcp --dport 443 -m state --state NEW -j ACCEPT
	-A INPUT -p tcp -m tcp --dport 5222 -m state --state NEW -j ACCEPT
	-A INPUT -p tcp -m tcp --dport 5223 -m state --state NEW -j ACCEPT
	-A INPUT -p udp -m udp --dport 137 -j ACCEPT
	-A INPUT -p udp -m udp --dport 138 -j ACCEPT
	-A INPUT -p icmp -m icmp --icmp-type 8 -j ACCEPT
	-A INPUT -p icmp -m icmp --icmp-type 11 -j ACCEPT
	-A OUTPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
	-A OUTPUT -o lo -j ACCEPT
	-A OUTPUT -p tcp -m tcp --dport 22 -m state --state NEW -j ACCEPT
	-A OUTPUT -p udp -m udp --dport 53 -m state --state NEW -j ACCEPT
	-A OUTPUT -p udp -m udp --sport 161 -m state --state NEW -j ACCEPT
	-A OUTPUT -m state --state NEW -j LOG
	COMMIT

`iptables-restore < /etc/iptables.rules.xmpp`

- - -
### NTP
*Getting the time and date synchronized through a restricted firewall*

    #!/bin/bash
    # ntpdate port 123
    iptables -A INPUT -p udp --dport 123 -j ACCEPT
    iptables -A OUTPUT -p udp --sport 123 -j ACCEPT

    # variation where rules are inserted as first items in the Tables
    # iptables -I INPUT 1 -p udp --dport 123 -j ACCEPT
    # iptables -I OUTPUT 1 -p udp --sport 123 -j ACCEPT


> Installing NTP...

    sudo apt-get install ntp
    nano /etc/ntp.conf
    server ntp.ubuntu.com
    server pool.ntp.org

    /etc/init.d/ntp restart
    ls -ahl /etc/cron.daily   > verify that ntp is +x executable
    ntpq -p                   > verify the service is working

    > MANUAL = ntpdate pool.ntp.org will now return socket 123 is in use


- - -
### NAT forwarding

    iptables -A FORWARD -i eth1 -o eth0 -j ACCEPT
    iptables -A FORWARD -i eth0 -o eth1 -j ACCEPT
    iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

> assuming that eth0 is your WAN and eth1 is your LAN

> accept all forwarding from eth1 to eth0 and back

> enable "nat" so that packets are addressed properly

- - -
### CIFS
    iptables -A INPUT -p tcp -s 10.10.10.250 --sport 445 -d 0/0 -j ACCEPT
    iptables -A OUTPUT -p tcp -s 0/0 --sport 1024:65535 -d 10.10.10.250 --dport 445 -m state --state NEW,ESTABLISHED -j ACCEPT
    > CIFS has been simplified to just use 445 TCP first...

    netbios-ns - 137/tcp # NETBIOS Name Service
    netbios-dgm - 138/tcp # NETBIOS Datagram Service
    netbios-ssn - 139/tcp # NETBIOS session service
    microsoft-ds - 445/tcp # if you are using Active Directory

### Allow AD Lookups LDAP/LDAPS

    iptables -A INPUT -p tcp -s 0/0 --sport 1024:65535 --dport 389 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -A OUTPUT -p tcp -s 0/0 --sport 389 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT

    iptables -A OUTPUT -p tcp --dport 389 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -A INPUT -p tcp -s 0/0 --sport 389 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT

    iptables -A INPUT -p tcp -s 0/0 --sport 1024:65535 --dport 636 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -A OUTPUT -p tcp -s 0/0 --sport 636 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT

    iptables -A OUTPUT -p tcp --dport 636 -m state --state NEW,ESTABLISHED -j ACCEPT
    iptables -A INPUT -p tcp -s 0/0 --sport 636 --dport 1024:65535 -m state --state ESTABLISHED -j ACCEPT

- - -
### DMZ Setup with dual nic

- ATMOS = 10.10.254.195
- LAN (router?) =  10.10.254.1
- eth0 = LAN  10.10.254.254
- eth1 = WAN 172.16.255.254
- eth2 = DMZ  192.168.50.1
- Router 172.16.255.1

#### forward traffic between DMZ and LAN

    iptables -A FORWARD -i eth0 -o eth2 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
    iptables -A FORWARD -i eth2 -o eth0 -m state --state ESTABLISHED,RELATED -j ACCEPT

> forward traffic between DMZ and WAN servers SMTP, Mail etc

    iptables -A FORWARD -i eth2 -o eth1 -m state --state ESTABLISHED,RELATED -j ACCEPT
    iptables -A FORWARD -i eth1 -o eth2 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

> Route incoming SMTP (port 25 ) traffic to DMZ server 192.168.2.2
    iptables -t nat -A PREROUTING -p tcp -i eth1 -d 202.54.1.1 --dport 25 -j DNAT --to-destination 192.168.2.2

> Route incoming HTTP (port 80 ) traffic to DMZ server load balancer IP 192.168.2.3
    iptables -t nat -A PREROUTING -p tcp -i eth1 -d 202.54.1.1 --dport 80 -j DNAT --to-destination 192.168.2.3

> Route incoming HTTPS (port 443 ) traffic to DMZ server reverse load balancer IP 192.168.2.4
    iptables -t nat -A PREROUTING -p tcp -i eth1 -d 202.54.1.1 --dport 443 -j DNAT --to-destination 192.168.2.4

> End DMZ .. Add other rules

## Uncomplicated Firewall UFW

The uncomplicated firewall is a much simpler way to configure some basic rules and enable the firewall

    sudo su
    ufw status verbose
    ufw allow 22
    ufw allow 443
    ufw default deny incoming
    ufw default deny outgoing
    ufw enable
    ufw status verbose

> Allowing 22 (SSH) and 443 (HTTPS) and denying all other incoming and outgoing traffic

    ufw delete allow 443
    ufw show raw
    ufw disable

> removing a rule is as simple as prefixing the allow or deny command with delete
> disabling the firewall allows all traffic

Most unfortunately there are some basic gaps that make it not very production ready (i.e. if you know what you are doing just keep using iptables)
1. ping, also known as icmp, packets (even just outbound) have to be handled in a very complex way, really not much better than iptables
1. established connection traffic is not just easily allowed
1. attempting to do something more complex very quickly requires very complex commands including just using iptables (lolwut)
1. iptables -nvL becomes almost unreadable with the extra layer

<https://wiki.ubuntu.com/UncomplicatedFirewall>

