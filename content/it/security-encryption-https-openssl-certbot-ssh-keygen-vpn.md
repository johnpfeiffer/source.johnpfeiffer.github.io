Title: Security Encryption HTTPS OpenSSL SSH Keygen VPN Letsencrypt Certbot
Date: 2017-02-16 23:34
Tags: security, encryption, aes, https, openssl, certbot, ssh, keygen, openvpn, vpn, letsencrypt, certbot

[TOC]

As our lives become increasingly monitored and digital the privacy of being unobserved or having a private conversation that we used to be able to take for granted now requires extra effort.  The more people who choose to use these easy and readily available tools the more privacy will become the standard rather than the exception.

# Symmetric and Asymmetric Encryption

Using a shared secret key is generally the simplest way to encrypt, both parties use the same key to encrypt and decrypt.

Asymmetric encryption (aka "public and private key") allows for a message to be encrypted without the parties having to meet or exchange a secret.

Both are often used together in a complementary fashion.

- <https://en.wikipedia.org/wiki/Public-key_cryptography>
- <https://en.wikipedia.org/wiki/Transport_Layer_Security>

Codes and the ability to communicate in secret have a very long history which many others have documented and thanks to the amazing efforts of many many people we have the ability to communicate our billions of messages with relative privacy.

- <https://en.wikipedia.org/wiki/History_of_cryptography#Modern_cryptography>
- <https://www.goodreads.com/book/show/984428.Crypto> (Steven Levy)

It is important to understand that good encryption depends on randomness to make it as hard as possible for an "attacker" to reverse engineer or guess the key, i.e. <https://en.wikipedia.org/wiki//dev/random>

The following is my summary of some of the most common and useful tools...

## Pretty Good Encryption for Pretty Good Privacy

While there is a lot of value in leveraging the GPG public and private keys for authenticity checking this is just about encrypted data...

### GPG Encryption

    gpg -c example.tar.gz
> prompts for a password to access the keyring and leverages existing (or automatically generates) public and private keys, and outputs example.tar.gz.gpg

**Note: encrypting before compressing is meaningless since encrypted data is random and compression depends on repetition/patterns**

    gpg --yes --passphrase=password -c example.txt
> non interactive encryption (if the private key is password protected), outputs example.txt.gpg

    echo "password" | gpg --yes --no-tty --batch --passphrase-fd 0 --output encrypted.txt.gpg  --symmetric --cipher-algo AES256 plain.txt
> non interactive AES 256 symmetric cipher rather than public/private keypairs

## GPG Decryption

    gpg example.tar.gz.gpg
> enter the passphrase to access the private key to decrypt the file

    gpg --yes --passphrase=password example.txt.gpg
> non-interactively access the private key to decrypt the file

    echo "password" | gpg --yes --no-tty --batch --passphrase-fd 0 --output plain.txt --decrypt encrypted.txt.gpg
> non interactively decrypt with symmetric encryption

*Do not pick password as your password ;p*

<https://www.gnupg.org/gph/en/manual/x110.html>

## AES 256 Encryption

AdvancedEncryptionStandard is one of the US and world standards as an encryption algorithm.

Security benefits from transparency in that if you provide the algorithm and source code in plain sight and attackers are still unable to decrypt/crack/manipulate the data then you are probably in good shape.

Perhaps one of the most well known projects (open source and free!) to advance the practice of encryption is <https://www.openssl.org/>

Here we encrypt and decrypt a text file:

    openssl aes-256-cbc -in plain.txt -out message.encrypted
> prompted for a password (symmetric key) to encrypt the file with AES 256

    openssl aes-256-cbc -d -in message.encrypted -out plain.txt
> prompted for a password to decrypt the message

    openssl aes-256-cbc -in plain.txt -out message.encrypted -pass pass:YOURPASSWORD
> non-interactively provide the password to encrypt the file with AES 256

    openssl aes-256-cbc -d -in message.encrypted -out plain.txt -pass pass:YOURPASSWORD
> non-interactively provide the password to decrypt the file with AES 256

*an incorrect password will create a zero byte file*

    openssl aes-256-cbc -a -d -in message.encrypted -out plain.txt
> if it's base64 encoded do not forget the -a

- <https://en.wikipedia.org/wiki/Advanced_Encryption_Standard>
- <https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation>
- <https://www.openssl.org/docs/manmaster/man1/openssl.html>

# Generating SSL Certificates and Private and Public Keys

Perhaps the most common use of TLS/SSL are the keys used to encrypt communication with a web server, these examples use a "self signed certificate" which most libraries and browsers will not trust.

> "Root Certificate Authorities" are the ones you send a "Certificate Signing Request" to generate a certificate that can be mathemetically trusted by the existing software libraries and browsers

## More Private and Public Key basics for SSL Certificates
The private key contains a series of numbers. Two of those numbers form the "public key", the others are part of your "private key".

The "public key" bits are also embedded in your Certificate (we get them from your CSR - certificate signing request).

### Verify the SSL Certificate and Private Key match
    (openssl x509 -noout -modulus -in server.pem | openssl md5 ; openssl rsa -noout -modulus -in server.key | openssl md5) | uniq
> outputs a single hash if matching, if two hashes are output then it is not unique and the key and cert do not match

To check that the public key in your cert matches the public portion of your private key:

    openssl x509 -noout -text -in server.crt
    openssl rsa -noout -text -in server.key

But since the public exponent is usually 65537 and it's challening to compare a long modulus you can use the following approach:

    openssl x509 -noout -modulus -in server.crt | openssl md5
    openssl rsa -noout -modulus -in server.key | openssl md5
> the "modulus" and the "public exponent" portions of the cert and key ... aka the two md5sum hashes should match

### Verify the Cert and Intermediate match and then Verify
    openssl verify -purpose sslserver -CAfile intermediate.pem -verbose server.pem
> ensure the intermediate certificate matches the SSL certificate (if it does not SSL trust will not work correctly)

### Verify a CSR matches the Key and Certificate
To check to which key or certificate a particular CSR belongs you can compute

    openssl req -noout -modulus -in server.csr | openssl md5

## Creating keys and certificates and certificate requests

### openssl New Key and Cert One Liner

    openssl req -subj '/CN=example.com/O=My Company Name LTD./C=US' -new -newkey rsa:2048 -days 365 -nodes -x509 -keyout server.key -out server.crt
> one liner to generate a self signed SSL key and certificate, since SSL certs are rotated regularly we can use 2048 instead of 4096 bits

### openssl certificate commands

    openssl req -out CSR.csr -new -newkey rsa:2048 -nodes -keyout privateKey.key
> create 2048 bit nopass key + csr (certificate signing request - usually sent to a Certificate Authority that is in the root chain bundled with major browsers and libraries)

    openssl x509 -req -days 365 -in CSR.csr -signkey privateKey.key -out cert.crt 
> self sign a CSR and generate a self signed SSL certificate

    openssl rsa -in mykey.pem -pubout
> display the public key generated from the private key

    openssl rsa -in mykey.pem -pubout -out mykey.pub
> use the private key to generate and save the public key to a file

    openssl req -text -noout -verify -in CSR.csr
>  Verify a CSR certificate request

    openssl rsa -check -in cert.key
>  Verify a key

    openssl x509 -text -in cert.crt
> View INFO about a cert and see the cert

    openssl x509 -noout -issuer -subject -dates -in cert.crt
> View specific items in the certificate (and do not print out the full certificate)

    openssl req -out CSR.csr -key privateKey.key -new
> Generate a certificate signing request (CSR) for an existing private key

    openssl x509 -x509toreq -in certificate.crt -out CSR.csr -signkey privateKey.key
> Generate a certificate signing request based on an existing certificate and private key


### Creating an RSA certificate with a password

    openssl genrsa -des3 -out domainname.key 2048
> Create a 2048 bit private key with passphrase

    openssl req -new -key domainname.key -out domainname.csr
> CREATE A CSR, CEERTIFICATE SIGNED REQUEST

Common Name (domain name) = fully qualified domain name

    openssl x509 -req -days 365 -in CSR.csr -signkey privateKey.key -out cert.crt
> Generate a self signed cert

### Remove a passphrase to install a private key on a server
    openssl rsa -in domainname-passphrase.key -out domainname-server.key

OR

    openssl rsa -in privateKey.pem -out newPrivateKey.pem


## Use openssl's built in webserver

    openssl s_server -cert server.pem -key server-nopass.key
> start a TCP server with the provided certificate and key on the default port of 4433

    openssl s_server -cert server.pem -accept 4433 -www
> start an HTTPS server with the cert and key combined in a .pem on the specific port (e.g. 4433)

    telnet localhost 4433
> verify basic network connectivity

    wget https://localhost:4433 --no-check-certificate
> verify basic network connectivity and download the contents without validating the SSL certificate

    openssl s_client -showcerts -connect localhost:4433
> show the ciphers and certificates of a server, "18 (self signed certificate)

    openssl s_client -connect ldaps.example.com:10636 -CAfile intermediate.crt
> show the ciphers and certificates of a server while providing client-side the Root + Intermediate Chain certificates

### Get a remote server ssl certificate using openssl and sed

    echo | openssl s_client -connect ${REMOTEHOST}:${REMOTEPORT} 2>&1 | sed -ne '/-BEGIN CERTIFICATE-/,/-END CERTIFICATE-/p'



### Getting and verifying an Intermediate Certificate

Popular web browsers will often have lock symbols or other ways for you to see (and download) a certificate)

1. startup vm with webserver (tomcat) + current certificate
1. chrome browse to the https://10.10.10.199
1. Click on the lock (certificate) symbol => Certificate information  "Issued to: example.com"
1. Click on the Certification Path (tab) ... see the root CA + intermediates + cert.
1. click on "GeoTrust" (or the top level Certificate listed in the path) -> View Certificate
1. Details (tab) -> Copy to File -> Save Base-64 encoded x.509 (.cer)
1. Verify that it is different than your original cert.crt
1. Copy paste that file into a place where you have openssl installed (i.e. ubuntu linux)
1. Hostfile (/etc/hosts) so that your openssl command can use the DNS name
1. `openssl s_client -showcerts -connect example.com:443`
1. Without the intermediate you should receive "Verify return code: 21 (unable to verify the first certificate)"
1. `openssl s_client -showcerts -connect example.com:443 -CAfile geotrust-intermediate.crt`
1. With the intermediate in the command above:   "Verify return code: 0 (ok)"

Finally, if the DNS name is publicly available, you can verify: <https://www.sslshopper.com/ssl-checker.html>

- - -
# Other certificate formats

## CONVERT FROM WINDOWS (IIS) PKCS12 OR PFX TO PEM

    openssl pkcs12 -info -in keystore.p12

    openssl pkcs12 -in original.pfx -out cert.pem -nodes
> This creates both the key and the cert

You can copy and paste the certificate portion into cert.crt

Also copy and paste the private key portion into the cert.key

## Configure an existing key + certificate into PKCS12

    openssl pkcs12 -export -inkey cert.key -in cert.pem -out keystore.p12

- - -
# KEYTOOL AND JAVA KEY STORES

Java, just like web servers, have public and private encryption keys in order to enable cryptography and encryption from within the applications.

    keytool -list -v -keystore /usr/lib/jvm/java-6-sun-1.6.0.24/jre/lib/security/jssecacerts
> hit enter as it has no password

    keytool -list -v -keystore /etc/java-6-sun/security/cacerts
> default password is changeit

    keytool -list -v -keystore /etc/java-6-sun/security/cacerts -alias alpha.domain.net  -storepass changeit
    keytool -list -v -keystore jssecacerts -storepass changeit | grep atmos -n4
    
    
    Keystore type: JKS
    Keystore provider: SUN
    
    Your keystore contains 76 entries
    
    Alias name: digicertassuredidrootca
    Creation date: Jan 7, 2008
    Entry type: trustedCertEntry

### Import a signed primary certificate to an existing Java keystore

One of the most common tasks is adding a certificate to trust

    keytool -import -trustcacerts -alias mydomain -file mydomain.crt -keystore /etc/java-6-sun/security/cacerts -storepass changeit
    Trust this certificate? [no]:
    
    type "yes"
    
    keytool -list -v -keystore /etc/java-6-sun/security/cacerts -storepass changeit
    
    keytool -printcert -v -file mydomain.crt
    
    keytool -import -trustcacerts -alias root -file geotrust.intermediate.crt -keystore /etc/java-6-sun/security/cacerts -storepass changeit
    
    keytool -delete -alias mydomain.com -keystore cacerts -storepass changeit


### EXTRACT A CERTIFICATE FROM A JKS INTO A .DER, THEN CONVERT IT INTO A .PEM AND IMPORT INTO THE JVM cacerts

    keytool -export -alias zanzibar -keystore zanzibar.jks > zanzibar.der
    openssl x509 -in zanzibar.der -inform DER -out zanzibar.crt -outform PEM
    
    keytool -import -trustcacerts -alias zanzibar -file zanzibar.crt -keystore /etc/java-6-sun/security/cacerts -storepass changeit

- <http://www.openssl.org/docs/HOWTO/certificates.txt>
- <http://www.sslshopper.com/article-most-common-java-keytool-keystore-commands.html>



- - -
# SSH Encryption

Secure Shell is for network access over an insecure network <https://en.wikipedia.org/wiki/Secure_Shell>

## Create a public/private key pair for SSH

Backup any existing ~/.ssh/id_rsa  (cp -a ~./ssh ~./ssh-bak)
Backup any existing ~/.ssh/id_rsa.pub

    ssh-keygen -t rsa -C "your_email@example.com"
    chmod 400 /path/to/id_rsa*
> id_rsa and id_rsa.pub  *e.g. in /home/USERNAME/.ssh , <https://en.wikipedia.org/wiki/Ssh-keygen>
> chmod to modify permissions (to the "only the owner can read") since if the private key is not restricted in security the ssh client will not run but instead return an error

**id_rsa  IS YOUR PRIVATE KEY, GUARD IT!**
> id_rsa.pub IS THE PUBLIC PORTION WHICH YOU ADD TO REMOTE SERVERS

> if you add a passphrase to your SSH key (to prevent hackers from simply copying the file)

    ssh-keygen -y
>  prompted for the path to the file, then prompted for the password to outpout a public signature (.pub)

    ssh-keygen -t dsa
> RSA is generally preferred, protocol 2, I only include the DSA command for completeness <http://security.stackexchange.com/questions/5096/rsa-vs-dsa-for-ssh-authentication-keys>


### output a .pub from a private key
    ssh-keygen -y -f id_rsa

### generate a fingerprint for verification of a host
    ssh-keygen -lf id_rsa.pub

### AMAZON ec2 instances have a different method, ec2-add-keypair
    openssl pkcs8 -in myec2key.pem -nocrypt -topk8 -outform DER | openssl sha1 -c

### ec2-import-keypair:
    openssl pkey -in ~/.ssh/ec2/primary.pem -pubout -outform DER | openssl md5 -c


## Adding a Public Key to a remote server
ON THE REMOTE SERVER IT SHOULD ONLY HAVE THE public key from .ssh/authorized_keys

    mkdir /home/username/.ssh
    sudo vi /home/username/.ssh/authorized_keys
    > or  cat .ssh/id_rsa.pub | ssh username@123.45.56.78 "cat >> ~/.ssh/authorized_keys"

    chmod 400  /home/username/.ssh/authorized_keys

Don't forget to modify:

    sudo nano /etc/ssh/sshd_config
    #AuthorizedKeysFile     %h/.ssh/authorized_keys

    /etc/init.d/ssh force-reload
    /etc/init.d/ssh restart


ON THE SERVER:  `ssh-agent sh -c 'ssh-add < /dev/null && bash'`
OPTIONAL?  `exec ssh-agent sh -c 'ssh-add </dev/null && exec /usr/local/bin/wmaker'`


### Connecting with SSH client to a remote server

    ssh -v -i id_rsa username@123.45.56.78
>  verbose, use identity from private key

    ssh -vvvv -i id_rsa username@example.com  
> if errors like (nil) verify permissions and ownership (whoami=username)

*Don't forget you sometimes have chmod 400*


### SSH ignore strict hosts checking 
(i.e. developing against an FQDN with a dynamic ip, this does expose you to the improbable risk of an imposter "man in the middle" server)

    ssh -i /usr/local/bamboo/bamboo_id_rsa -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no
> this command line parameter will not store nor verify the remote server's signature

A more permanent configuration change:

    vi ~/.ssh/config

    IdentityFile ~/.ssh/id_rsa

    Host example.com
            StrictHostKeyChecking no
            UserKnownHostsFile=/dev/null

### SSH Agent Forwarding

It can be insecure to forward your SSH access through a jumpbox to a machine deeper in your network, though it is generally worse to leave SSH keyson a jumpbox.

    ssh-add ~/.ssh/example.pem
> add a specific key to the ssh agent
    ssh-add -L
> an optional step to list the keys that ssh-agent has loaded in memory

    ssh -At user@1.2.3.4
> SSH and explicitly forward the key so that the second shell session (ssh-agent) has access to it

        ssh user@5.6.7.8
> the extra indentation is to indicate that from the jumpbox you are able to ssh to the internal machine


A more permanent configuration change by using ~/.ssh/config

    Host 1.2.3.4
        ForwardAgent yes
        IdentityFile ~/.ssh/example.pem

<https://linux.die.net/man/1/ssh-add>

### SSH TCP tunnel

In this example the SSH tunnel could be used for a SOCKS proxy for the browser...

    ssh -ND 9999 user@example.org
> connect via ssh to a remote server, after the password prompt the process will stay open for connections locally via port 9999

#### Use a docker container to isolate the VPN software and instead only allow an SSH tunnel as a web proxy

An alternative to a remote machine as the SSH target for the tunnel you can instead target a docker container running locally.
- This allows you to package everything required (i.e. vpn software) into the container
- Has a security benefit that only the container (and its filesystem) are directly exposed to the VPN
> Note that for an even more limited security profile the container could run as an HTTP proxy as it will only handle HTTP traffic (rather than all TCP)

    docker run --detach --rm --privileged --publish 2222:2222 ubuntu-xenial-vpn
> the container is running SSHD

    ssh -p 2222 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@localhost
    openconnect https://vpn.example.com
> SSH into the container and start the openconnect vpn connection and authenticate

    ssh -ND 9999 -p 2222 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no root@localhost

#### Configure Firefox to use the SOCKS Host

    Firefox -> Edit -> Preferences -> Advanced -> Network -> Connection -> Settings
    Manual Proxy configuration: SOCKS Host: localhost, Port 9999
> firefox sends requests to the server over the ssh encrypted connection

#### Configure Firefox to use the socks5 proxy for DNS

    about:config
    network.proxy.socks_remote_dns
> use the address bar to access the advanced configuration option and set socks_remote_dns true

This ensures the browser will use the SOCKS proxy domain name server rather than the local machines


### SSH tunnel for Windows RDP

    ssh -L 3389:172.24.32.40:3389 172.24.32.100 -l sshusername -N

- L = local port is forwarded to the remote host and port
- l = login_name
- .40 = the windows rdp server
- .100 = the remote ssh server which has access to the windows rdp server
- N = do not execute a remote command (port forwarding only)


### ssh tunneling in general

local port:host:remote-port

#### ssh tunnel on port 9090 (cherokee-admin)

    sudo vi /etc/sysctl.conf
        net.ipv6.conf.all.disable_ipv6=1

** On the remote server start the admin UI (which only allows access via 127.0.0.1 by default for security reasons)**
    sudo cherokee-admin

        Cherokee Web Server 1.2.101 (Jan 30 2012): Listening on port 127.0.0.1:9090,
        TLS disabled, IPv6 enabled, using epoll, 4096 fds system limit, max. 2041
        connections, caching I/O, single thread
        
        Login:
          User:              admin
          One-time Password: xoKmLN0aISztVMFs
        
        Web Interface:
          URL:               http://127.0.0.1:9090/


    ssh -L 9090:localhost:9090 -p 22 user@host.com -N
> - L = local port is forwarded to the remote host and port, so ssh binding the localhost to port 9090
> - ssh the remote server on port 22
> - ssh with the specified user to the hostname (assuming DNS is correct)
> - N = do not execute a remote command (port forwarding only)

    ssh -L 9090:localhost:9090 remote_IP
> assumes the ssh port is 22 and the remote user is the same as the local user, not a good assumption

On your browser access http://localhost:9090 to see the Cherokee Admin UI

Future ideas: iptables 9090? forwarding?


- - -
# Virtual Private Networks and openVPN

## Docker OpenVPN
Using Docker is one of the easiest ways to leverage all of the open source tools (assuming for security you inspect the upstream source code, clone the Dockerfile, build your own docker image/container ;)

    # https://github.com/kylemanna/docker-openvpn
    # https://openvpn.net/index.php/open-source/documentation/howto.html
    export FQDN="example.com"
    export OVPN_DATA="ovpn-data"
    docker volume create --name $OVPN_DATA
    # generate the initial configuration in the volume
    docker run -v $OVPN_DATA:/etc/openvpn --rm kylemanna/openvpn ovpn_genconfig -u udp://$FQDN
    # generate the certificate in the volume (you must choose a passphrase)
    docker run -v $OVPN_DATA:/etc/openvpn --rm -it kylemanna/openvpn ovpn_initpki
    # start the openvpn service
    docker run -v $OVPN_DATA:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN kylemanna/openvpn
    
    # generate the client certificate without the passphrase
    docker run -v $OVPN_DATA:/etc/openvpn --rm -it kylemanna/openvpn easyrsa build-client-full $FQDN nopass
    # export the client config with embedded certificates
    docker run -v $OVPN_DATA:/etc/openvpn --rm kylemanna/openvpn ovpn_getclient $FQDN > $FQDN.ovpn
    
## Digital Ocean OpenVPN

### Dedicated SSH User

- create a new ssh key (ops sec best practice)
- Setup a free Firewall with ports tcp 22 and udp 1194
- Create and Deploy a new droplet ($5 in a region near you for lower latency, with your newly created SSH key)
- Once it has finished booting use the Digital Ocean web ui: Networking -> Firewalls -> FirewallName -> Droplets to add the Droplet to the firewall
- ssh -i ~/.ssh/your-new-ssh-key root@1.2.3.4
- reset the root password: passwd
- Use the WebUI from Digital Ocean to verify you can access local console with the root user (and the new password)
- harden the machine by adding a dedicated ssh user (not root!)
- - useradd -s /bin/bash -m NEWUSERNAME
- - usermod -a -G admin NEWUSERNAME
- - passwd NEWUSERNAME
- - verify this with: cat /etc/passwd | grep NEWUSERNAME ; cat /etc/group | grep NEWUSERNAME
- - give the new user sudo permissions: visudo 
- - - UPDATE THE LINE TO: %admin ALL=(ALL) NOPASSWD:ALL
- - - MOVE THE LINE BELOW: %sudo	ALL=(ALL:ALL) ALL
- - - VERIFY: cat /etc/sudoers
- - mkdir -p /home/NEWUSERNAME/.ssh
- - vim /home/NEWUSERNAME/.ssh/authorized_keys (paste the public key that matches the new ssh key)
- - /etc/init.d/ssh force-reload
- - /etc/init.d/ssh restart
- - BE SURE that /home/NEWUSERNAME/.ssh and authorized_keys is owned by the new user (chown)
- - VERIFY WITH VERBOSE the new user can SSH with: ssh -v -i ~/.ssh/your-new-ssh-key NEWUSERNAME@1.2.3.4
- - VERIFY PERMISSIONS ONCE LOGGED IN WITH SSH: sudo su

### More Hardening
- disable root user from using SSH access and harden with a non-standard port
- - vim /etc/ssh/sshd_config
- - - Port 22222
- - - PermitRootLogin no
- - - ADD TO THE END OF THE FILE: AllowUsers NEWUSERNAME
- - service sshd restart
- - VERIFY: netstat -antp  # should see 0.0.0.0:22222

### Prerequisites

    apt update
    apt install openvpn easy-rsa
    vim /etc/sysctl.conf
        net.ipv4.ip_forward=1
    sudo sysctl -p

Setting up the certificate authority (since OpenVPN uses keys)

    make-cadir ~/openvpn-ca
    cd ~/openvpn-ca

`vim vars`
> update the export KEY_NAME, KEY_ORG, KEY_EMAIL, KEY_OU to something more personalized

    source vars
    ./clean-all
    ./build-ca
> You can just press enter a bunch to use all the defaults that you preconfigured in the vars file previously

`./build-key-server KEY_NAME (i.e. server or myvpn)
> Just press enter to accept all the defaults again (no challenge password!) and press y at the end to Sign and then Commit the certificates

    ./build-dh
    openvpn --genkey --secret keys/ta.key

`./build-key client1`
> if you want to build another one later you must use: sudo su ; cd /root/openvpn-ca ; source vars ; ./build-key client2

### Configure openvpn

    cp ~/openvpn-ca/keys
    sudo cp ca.crt myvpn.crt myvpn.key ta.key dh2048.pem /etc/openvpn
    gunzip -c /usr/share/doc/openvpn/examples/sample-config-files/server.conf.gz | sudo tee /etc/openvpn/myvpn.conf

`vim /etc/openvpn/myvpn.conf`
    tls-auth ta.key 0 # Remove the preceding ; to uncomment this line
    key-direction 0
    cipher AES-256-CBC
    auth SHA256
    user nobody  # Remove the preceding ; to uncomment this line
    group nogroup
    push "redirect-gateway def1 bypass-dhcp"  # Remove the preceding ; to uncomment this line
    push "dhcp-option DNS 208.67.222.222"  # Remove the preceding ; to uncomment this line
    push "dhcp-option DNS 208.67.220.220"  # Remove the preceding ; to uncomment this line
    block-outside-dns
    cert myvpn.crt
    key myvpn.key

> some tweaks for more security https://community.openvpn.net/openvpn/wiki/Hardening (the ta.key = tls auth)
> 208.67.222.222 = opendns , https://openvpn.net/index.php/open-source/documentation/howto.html

`sudo systemctl start openvpn@myvpn`
`sudo systemctl status openvpn@myvpn`
`sudo systemctl enable openvpn@server`
> Should end with "ovpn-myvpn[21142]: Initialization Sequence Completed"
> "enable" means that the service will start at boot

`netstat -antup`
> Should list all the TCP and UDP listening services including port 1194, 0.0.0.0:1194

`ip addr show tun0`
> Should show the tunnel interface is created what the network range is (e.g. 10.8.0.1)


Consider updating myvpn.conf to use port 443 and proto tcp in order to assist clients traverse/reach the openvpn server in restricted environments

TODO: automate using packer and digital ocean apis to create an image

<https://www.digitalocean.com/community/tutorials/how-to-set-up-an-openvpn-server-on-ubuntu-16-04>

## Connect a client to the OpenVPN server

### OpenVPN client config infrastructure on the remote server

    mkdir -p /root/client-configs/files
    chmod 700 /root/client-configs/files   
    cp /usr/share/doc/openvpn/examples/sample-config-files/client.conf /root/client-configs/base.conf
    vim /root/client-configs/base.conf
        remote NEW-VPN-SERVER-IP-ADDRESS 1194
        user nobody
        group nogroup
        # ca ca.crt
        # cert client.crt
        # key client.key
        cipher AES-256-CBC
        auth SHA256
        key-direction 1

> if you have modified the port and protocol ensure that 1194 and udp are updated accordingly
> windows clients will not be able to downgrad the user and group to nobody/nogroup
> commenting out the files as they will be embedded in the .ovpn config file


`vim /root/client-configs/make_config.sh`
    KEY_DIR=/root/openvpn-ca/keys
    OUTPUT_DIR=/root/client-configs/files
    BASE_CONFIG=/root/client-configs/base.conf
    cat ${BASE_CONFIG} \
        <(echo -e '<ca>') \
        ${KEY_DIR}/ca.crt \
        <(echo -e '</ca>\n<cert>') \
        ${KEY_DIR}/${1}.crt \
        <(echo -e '</cert>\n<key>') \
        ${KEY_DIR}/${1}.key \
        <(echo -e '</key>\n<tls-auth>') \
        ${KEY_DIR}/ta.key \
        <(echo -e '</tls-auth>') \
        > ${OUTPUT_DIR}/${1}.ovpn

> This automates creating a config file via a script

    chmod 700 make_config.sh
    ./make_config.sh client1
    ls -ahl /root/client-configs/files/

### Once you have the configuration
`sudo apt-get install -y openvpn`
> For a linux client this installs the openvpn client software

`scp -i ~/.ssh/VPNKEY -P 22222  NEWUSERNAME@VPN-IP-ADDRESS:client1.ovpn .`
> of course no matter what we need the open vpn client configuration

Or... From a client computer SCP to download the $FQDN>ovpn and then connect to the openvpn server

    sudo openvpn --config client1.ovpn

    # verify with the following in the output: "/sbin/ip addr add dev tun0 local 192.168.255.6 peer 192.168.255.5"
    # ifconfig -a  "tun0 ... inet addr:192.168.255.6"  , as you send traffic: RX bytes:4145707 (4.1 MB)  TX bytes:319025 (319.0 KB)
    curl checkip.amazonaws.com  # should return the IP address of the VPN server (not your local Wifi/ISP)
    curl https://dnsleaktest.com/
    # https://whoer.net/#extended

### DNS Security

Moreover your DNS server can "leak" or be hijacked, here are some good alternatives to your snooping ISP or "big brother" evil corp.

- 185.121.177.177 or 169.239.202.202 (http://dnsrec.meo.ws/ part of opennic)
- 84.200.69.80 or 84.200.70.40 (dns.watch free, neutral, privacy)
- https://www.opennic.org/

`echo 185.121.177.177 >> /etc/resolvconf/resolv.conf.d/tail`

These are DNS providers that have been assimilated into the borg:

- 216.146.36.36 (Dyn DNS was acquired by Oracle)
- 209.244.0.4 (Level3 Communications telco was acquired by CenturyLink)
- 208.67.220.220 (OpenDNS was acquired by Cisco and they basically store your data)
- 8.8.8.8 (Google - so basically giving them even more data - especially when you use Chrome too)

A non standard protocol to encrypt DNS traffic: <https://en.wikipedia.org/wiki/DNSCrypt>

- - -
# Letsencrypt and certbot for free SSL Certificates

A relatively recent development has been a widespread effort to help secure more of everyone's communications by encouraing web sites to install SSL certificates (and automate renewals) for free...

Here is the tool that allows you to easily automate getting a free SSL certificate (trusted by libraries and browsers no less)

Once again Docker simplifies things slightly (as long as you trust the container ;)

Prerequisite: setup a DNS record for yourdomain.com to point to the server

    docker run -it --rm -p 443:443 --name certbot -v /etc/letsencrypt:/etc/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt quay.io/letsencrypt/letsencrypt certonly --standalone -d yourdomain.com

1. Starts a container with a web server that binds to port 443 
2. The same web server/tool sends a certificate signing request (from yourdomain.com) to letsencrypt.org
3. letsencrypt.org then attempts to contact the provided domain (DNS -> IP -> server -> docker container)
4. the web server/tool then securely downloads the new SSL certificate
5. all of the files used in the process are stored in /etc/letsencrypt (in this "simple" mode /etc/letsencrypt/live/yourdomain.com/

You can keep renewing the certificate (which lasts 90 days) for free and there are a number of other open source tools (which leverage the API/process)

- <https://letsencrypt.org/how-it-works/>
- <https://certbot.eff.org/docs/using.html#certbot-commands>
- <https://github.com/certbot/certbot/blob/master/Dockerfile>


# Cryptography Exercises
In order to really understand and enjoy cryptography you can dive deeper via some of these exercises

- <https://cryptopals.com/>

