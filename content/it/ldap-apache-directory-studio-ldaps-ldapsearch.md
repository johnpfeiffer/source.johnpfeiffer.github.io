Title: LDAP and LDAPS with Apache Directory Studio and the Java Keystore
Date: 2012-03-29 21:44:51
Tags: linux, ldap, apache, directory, studio, ldaps, ldapsearch, java keystore, keystore, keytool

The popularity of LDAP for directory service/lookup means Apache Directory Services + Apache Directory Studio is an excellent combination for getting started with identity and user management.

<http://directory.apache.org/apacheds/>
> on windows it requires a 32bit JRE =(

Download then install: `dpkg -i  apacheds-1.5.7.deb`
> later on uinstall is possible via: `dpkg -r apacheds`

By default Apache DS listens on **10389** and **10636** (SSL)

You can connect to it with Apache Dir Studio with "LDAP -> New Connection -> hostname , port = 10389"

    BindDN or user (click on Check Authentication)
    uid=admin,ou=system
    password= secret
    
    ldapsearch -v -H ldap://ldap.domain.com:10389 -x -D "uid=admin,ou=system" -w "secret" "(objectclass=*)" -b "ou=system"

### Self Signed Java Keystore
A Java Keystore is different from a normal cert + key combo. Example "self signed" java keystore, key, certificate combo

NOTE: CN should really be ldap.domain.com , not Zanzibar!!!!

    keytool -genkey -keyalg "RSA" -dname "cn=zanzibar, ou=ApacheDS, o=ASF, c=US"  -alias zanzibar -keystore zanzibar.jks -storepass secret -validity 730
> Press Enter to use the same password for certificate as we already entered above for the keystore

    keytool -list -v -keystore zanzibar.jks -storetype jks -storepass secret


### ApacheDS Config File
SSL is enabled by default but needs to be modified to use a separate certificate:

`sudo vi /var/lib/apacheds-1.5.7/default/conf/server.xml`

     <ldapServer id="ldapServer"
    
                allowAnonyn mousAccess="false"
                saslHost="ldap.example.com"
                saslPrincipal="ldap/ldap.example.com@EXAMPLE.COM"
                searchBaseDn="ou=users,ou=system"
                maxTimeLimit="15000"
                maxSizeLimit="1000"
       keystoreFile="/var/lib/ssl/zanzibar.jks"
       certificatePassword="secret">
    
        <transports>
          <tcpTransport address="0.0.0.0" port="10389" nbThreads="8" backLog="50" enableSSL="false"/>
          <tcpTransport address="0.0.0.0" port="10636" nbThreads="8" backLog="50" enableSSL="true"/>
        </transports>
    
- - -
### Start and verify the new config
    /etc/init.d/apacheds-1.5.7-default restart
    /etc/init.d/apacheds-1.5.7-default status
    
    netstat -an --inet
> start the service and check ports listening, established, time wait (especially 10636)

JXplorer or ApacheDirectoryStudio connection "LDAP -> New Connection -> hostname , port = 10636" (SSL or LDAPS)

    BindDN or user (click on Check Authentication)
    uid=admin,ou=system 
    password= secret     
    
SELF SIGNED CERTIFICATE WARNING - you can view the certificate and choose to manually accept...

> NOTE IF YOU SEE THE ERROR "The connection failed - Connection refused: connect (zanzibar:10636)"  
    javax.naming.CommunicationException: zanzibar:10636 [Root exception is java.net.ConnectException: Connection refused: connect]

ENSURE THAT YOUR TRANSPORT IS NOT ONLY ALLOWING localhost! (below is the locked down setting...)

    <tcpTransport address="localhost" port="10636" enableSSL="true"/>

### Modify the iptables firewall

Allow well known LDAP (389) and LDAPS (636) ports to work with ApacheDS

    iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 389 -j REDIRECT --to-port 10389
    iptables -A PREROUTING -t nat -i eth0 -p tcp --dport 636 -j REDIRECT --to-port 10636
    
### Test and verify connectivity from a remote machine
    ldapsearch -H ldap://ldap.domain.com:389 -x -D "uid=example,ou=system" -W -b "ou=system" "(uid=example)"

### Extract a Certificate from the Java Key Store
EXTRACT A CERTIFICATE FROM A JKS INTO A .DER, THEN CONVERT IT INTO A .PEM AND IMPORT INTO THE JVM cacerts
(this allows a java based app to connect to your self signed cert LDAP server)

    keytool -list -v -keystore zanzibar.jks -storetype jks -storepass secret
      Alias name: zanzibar
    
    keytool -export -alias zanzibar -keystore zanzibar.jks -storepass secret > zanzibar.der
    openssl x509 -in zanzibar.der -inform DER -out zanzibar.crt -outform PEM
    openssl x509 -text -in zanzibar.crt | head        //verify you have a valid cert
    
    openssl s_client -connect localhost:10636                           //Verify return code: 18 (self signed certificate)
    openssl s_client -connect localhost:10636 -CAfile zanzibar.crt      //Verify return code: 0 (ok)
    
    keytool -import -trustcacerts -alias zanzibar -file zanzibar.crt -keystore /etc/java-6-sun/security/cacerts -storepass changeit

### Test and Verify the LDAPS connection
    openssl s_client -connect ldap.domain.com:636
> Verify return code: 18 (self signed certificate)
    openssl s_client -connect ldap.domain.com:636 -CAfile zanzibar.crt
> Verify return code: 0 (ok)

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
### Use an existing certificate and key and create a Java Key Store
EXISTING CERTIFICATE AND KEY AND CREATE A .JKS

    openssl pkcs12 -export -in cert.crt -inkey cert.key -out keystore.p12 -name serveraliashostname -CAfile intermediatebundle.crt -caname root
    Enter Export Password: secret
    
    keytool -list -v -keystore keystore.p12 -storetype pkcs12

#### CONVERT THE PKCS12 TO JKS FORMAT
    keytool -importkeystore -srckeystore keystore.p12 -srcstoretype PKCS12 -deststoretype JKS -destkeystore keystore.jks
    
    keytool -list -v -keystore keystore.jks -storetype jks

    sudo vi /var/lib/apacheds-1.5.7/default/conf/server.xml 
          keystoreFile="/var/lib/ssl/keystore.jks"

still need to figure out how to include the intermediate CAcert root chain...!


### IMPORTING/REPLACING A JKS KEYSTORE
    keytool -importkeystore -deststorepass secret -destkeypass secret -destkeystore keystore.jks -srckeystore keystore.p12 -srcstoretype PKCS12 -srcstorepass secret -alias oldaliasname

GUI CONVERTER FROM PKCS12 to JKS (requires Java 1.6 or higher)
<http://portecle.sourceforge.net/>  (open the .p12 , Tools -> Keystore type to JKS)
(seems to have a funny message where it needed change the password to "password)")

    keytool -import -trustcacerts -alias ldap.domain.com -file cert.crt -keystore zanzibar.ks -storepass secret
    keytool -import -trustcacerts -alias root -file GeoTrust.crt -keystore zanzibar.ks
> Both self signed and third party certificates can be supported with ApacheDS LDAPS.

LDAP with SSL is a little tricky and it's useful to use openssl and ldapsearch to verify.

    
     <ldapServer id="ldapServer"
                allowAnonymousAccess="false"
                saslHost="ldap.example.com"
                saslPrincipal="ldap/ldap.example.com@EXAMPLE.COM"
                searchBaseDn="ou=users,ou=system"
                maxTimeLimit="15000"
                maxSizeLimit="1000"
                keystoreFile="/var/lib/ssl/zanzibar.jks"
                certificatePassword="secret">
    
        <transports>
          <tcpTransport address="0.0.0.0" port="10389" nbThreads="8" backLog="50" enableSSL="false"/>
          <tcpTransport address="0.0.0.0" port="10636" nbThreads="8" backLog="50" enableSSL="true"/>
        </transports>


`openssl s_client -connect domain.com:10636 -CAfile intermediate.crt`

- - -
    ldapsearch -H ldaps://ldap.domain.com:10636 -x -D "uid=example,ou=system" -w PASSWORD -b "ou=system" "(uid=example)"
> ERROR: ldap_sasl_bind(SIMPLE): Can't contact LDAP server (-1)

ON A REMOTE MACHINE IN ORDER TO USE LDAPSEARCH WITH LDAPS 636...

    sudo nano /etc/ldap/ldap.conf
    
    TLS_CACERT /var/lib/ssl/intermediate.crt
    TLS_CACERTDIR /var/lib/ssl/
    TLS_CERT /var/lib/ssl/cert.crt
    
NOW THE BELOW WILL WORK

    ldapsearch -H ldaps://ldap.domain.com:10636 -x -D "uid=example,ou=system" -w PASSWORD -b "ou=system" "(uid=example)"
    ldapsearch -H ldaps://ldap.domain.com:636 -x -D "uid=example,ou=system" -w PASSWORD -b "ou=system" "(objectclass=*)"

