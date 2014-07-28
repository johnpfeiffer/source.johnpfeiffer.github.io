Title: Blackberry Enterprise Server Express on same domain as BES (windows and exchange 2003)
Date: 2010-05-03 13:41
Author: John Pfeiffer
Slug: blackberry-enterprise-server-express-on-same-domain-as-bes-windows-and-exchange-2003

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Blackberry Express Server install: Windows 2003 with Exchange Server
2003 with BES 5 already installed

</p>

Why Blackberry Express? Well it's the core Blackberry experience (email
+ contacts + calendar) but  

only requires a data plan, not a special (expensive) Blackberry plan.

</p>

The big item missing: Wireless activation is only available with BES
dataplan.  
[http://crackberry.com/blackberry-101-lecture-2-bes-and-bis-whats-difference][]

</p>

The dilemma, if you already have a BES installation, can you setup a
BESX too?

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -  

"the two BES servers cannot be in the same BES Domain, but can be in the
same AD tree and access the same exchange server. "

</p>

"provided BlackBerry Enterprise Server Express is introduced as a new
deployment with its own  

BlackBerry domain, as defined by the BlackBerry configuration
database... the BlackBerry Enterprise  

Server and BlackBerry Enterprise Server Express can run independently in
the same Microsoft Exchange  

environment in a Microsoft Windows Domain and would be managed from
separate BlackBerry Administration  

Service consoles."

</p>

Apparently there is a difference between a BES Domain and a windows
domain... Basically a BES Domain  

SHOULD only be the BES installation & Database, therefore you should be
able to have multiple BES  

installations in the same Windows Domain (e.g. a large corporation with
many exchange servers all  

in the same Windows Domain?).

</p>

I will try it with my own twist - Not only a separate BESX installation
on a windows 2003 server BUT  

also creating a separate BESADMIN for the new BESX installation.

</p>

[http://supportforums.blackberry.com/t5/BlackBerry-Professional-Software/...][]

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -

</p>

\1. Setup a Windows 2003 Server SP2 in the Domain (exchange sys mgmr
must match version to exch server!)  

NEEDS at least 1GB RAM - but give it more if you suffer performance
issues!

</p>

A. Install Exchange 2003 SP2 System Manager (Requires Exchange Install
CD -\> Deployment Tools)  

exch2k3\\setup\\i386\\setup.exe =\> Action = Custom  

Action = Install (next to MS Exch System Management Tools) ... NEXT ...
112MB required, NEXT

</p>

B. Download & Install Exchange Service Pack 2 (E3SP2ENG.exe for an old
Exchange 2k3 cd)  
[http://www.microsoft.com/downloads/details.aspx?FamilyID=535bef85-3096-4...][]

</p>

E3SP2ENG\\setup\\i386\\update.exe (goes from version 6.5 to ? requiring
2 & 13 MB space)

</p>

C. Ensure TCP port 3101 (outgoing) is open on your firewall

</p>

D. Ensure your anti-spam is not blocking "blackberry.net"

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -  
[http://www.blackberry.com/btsc/viewContent.do?externalId=KB02276][]

</p>

\1. CREATE a user BESADMIN for the Domain (in Active Directory Users and
Computers)  

On the exchange server with the Mailbox enabled user creation dsa.msc
-\> right click = new user

</p>

\2. PERMISSION SEND AS: On the domain, dsa.msc  

From the Active Directory "View" option choose Advanced Features

</p>

A. Right click on the root of the domain for Properties -\> Security -\>
Advanced  

Add BESADMIN and Apply Onto = User Objects (dropdown) , Allow = Send As
(checkbox)

</p>

B. Maybe? more secure: only right click on each OU or user that will be
using Blackberry and  

give the BESADMIN "Send As" permission

</p>

\3. PERMISSIONS Exch 2k3 System Manager -\> Administrative Groups right
click the Group for your BES  

(e.g. First Administrative Group) -\> Delegate Control -\> Add  

Browse -\> Role = Exchange View Only Administrator

</p>

\4. PERMISSIONS Exchange Server: Start \> Programs \> Microsoft Exchange
\> System Manager  

Administrative Groups \> First Administrative Group \> Servers \> right
click SERVERNAME (properties)  

Security -\> find the BESADMIN and enable checkboxes:

</p>

\* Administer Information Store  

\* Send As  

\* Receive As

</p>

(Click on Advanced and ensure that "Allow inheritable permissions" is
checked)

</p>

\5. PERMISSIONS Local Admin: each server that will have Blackberry
Enterprise Server Express components

</p>

My Computer right click -\> Manage -\> Local Users & Groups -\> Groups
-\> Administrators  

Add = BESADMIN

</p>

\6. My Computer right click -\> Properties -\> Remote -\> Enable Remote
Desktop -\>  

Select RemoteDesktop Users =\> Add = BESADMIN

</p>

\7. PERMISSIONS Log on Locally & Log on as a Service  

Start -\> Administrative Tools -\> Local Security Settings =\> Local
Policies -\> User Rights Assignment  

double click Log on Locally & Log on as a Service and add BESADMIN

</p>

\8. BLACKBERRY warn that you need the Microsoft hotfixes 823343 and
894470  
[http://support.microsoft.com/kb/823343][] and
[http://support.microsoft.com/kb/894470][]  

Verify by c:\\exchsvr\\bin\\cdo.dll 708KB right click Version 6.5.7232
or later

</p>

\9. REBOOT the server (ok, just an old habit)  

Log in as the BESADMIN user  

C:\\Research In Motion\\BlackBerry Enterprise Server 5.0.1\\setup.exe

</p>

A. Create a Blackberry Configuration Database (aka BES Domain?)  

B. Blackberry Enterprise Server with all components  

C. preinstallation checklist will show you everything is ready (or will
be auto installed)  

D. Install MS SQL Server 2005 Express SP3

</p>

E. note that the extracted setup folder is very similar to the target
install folder  

C:\\Research In Motion\\BlackBerry Enterprise Server 5.0.1  

C:\\Program Files\\Research In Motion\\BlackBerry Enterprise Server\\  

enter BESADMIN password and the NAME of the Server where the SQL Express
will be installed  

(e.g. the name of the server you are installed Blackberry Express!)

</p>

F. read the summary, click INSTALL ... watch & wait.

</p>

G. You are prompted to restart the computer - do so and then log in
again with the BESADMIN user.  

H. Installation continues with the Database Information ... just click
Next  

The database BESMgmt doesn't exist, would you like to create it ... YES

</p>

I. Enter Blackberry CAL Key e.g. besexp-123456-123456-123456-123456  

SRP Host name: gb.srp.blackberry.com and port number: 3101 were already
provided  

SRP identifier = (Serial Number from Blackberry download) S12345678  

SRP authentication key = (Licence Key from Blackberry download)  

1234-1234-1234-1234-1234-1234-1234-1234-1234-1234  

CLICK VERIFY BUTTON 1 AND BUTTON 2 (should be successful and valid!
NEEDS dashes - inbetween!)

</p>

J. Microsoft Exchange Server popup - type in the Exchange Server Name  

K. Administration Settings (already filled in by default) CLICK NEXT  

(no, I don't want to use SSL between the Blackberry Admin and my LAN
browser)

</p>

L. Type in the BESADMIN password and click NEXT  

M. Advanced Administration = leave as windows default click NEXT  

N. click Start Services button  

BlackBerry Router has successfully started.  

BlackBerry Attachment Service has successfully started.  

BlackBerry Dispatcher has successfully started.  

BlackBerry MDS Connection Service has successfully started.  

BlackBerry Alert has successfully started.  

BlackBerry Administration Service - NCC has successfully started.  

BlackBerry Administration Service - AS has successfully started.  

BlackBerry Controller has successfully started.

</p>

O. Make a note of the Web Admin address(es)  
[https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webconsole/login][]  
[https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webdesktop/login][]

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -  

Test your Blackberry Express Installation

</p>

A. Locally on the Server you can check services.msc (all BB services
started)  

and eventvwr.msc (no Blackberry errors)

</p>

B. Use a browser (IE8?)
[https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webconsole/login][]  

(don't worry about the Browser "Security Alert" as it will be a self
signed SSL certificate,  

you can install the certificate and add it to Trusted Sites too...)

</p>

Install the RimWebComponents.cab

</p>

C. Create a user (you just need their email address - user should only
be on one BES Domain  

so not on BES 5 and BES X at the same time!)  

Create User with an Activation Password (e.g. something simple that
times out in 4 hours)

</p>

Wait until it gives you the OK message that the user was created (and
activation email sent)

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -  

ASSIGN A DEVICE TO A USER
([http://docs.blackberry.com/en/admin/deliverables/14334/][] )  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -

</p>

A. Using the Blackberry Administration Service (web)  
[https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webconsole/login][]

</p>

On the left there's a DEVICES area -\> Attached Devices (if it doesn't
expand?)

</p>

Connect the BlackBerry device to the computer.  

Click Manage current device -\> Click Assign current device -\> Search
for a user account

</p>

B. Users can activate their BlackBerry devices by connecting them to
computers using a USB cable  

or Bluetooth connection and logging in (with a browser) to the
BlackBerry Web Desktop Manager.  
[https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webdesktop/login][]

</p>

When users complete the activation process, the BESX synchronizes
through the BlackBerry Router.  

If a connection to the BlackBerry Router is interrupted, the data
transfer continues over the  

wireless network.

</p>

C. Blackberry Desktop Manager installed on a computer (and connected to
their Outlook Profile)  

Attach/Connect to a Device

</p>

Z. Not likely to be enabled but theoretically after sending the
Activation Password the  

BlackBerry Enterprise Server sends an email message with an etp.dat

</p>

On the Device choose Options -\> Advanced Options -\> Enterprise
Activation

</p>

"Activation request failed. A service connection is unvailable"

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -  

TIPS  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -

</p>

\1. Setup a default Password requirement

</p>

Policy -\> Manage IT Policies -\> Edit IT Policy (default) -\> Device
Only Tab

</p>

\2. Increase the default synchronization of messages when activating

</p>

Servers and components -\> BlackBerry Solution topology \> BlackBerry
Domain \> Component view \> Email  

Click on the "instance" (e.g. computername\_EMAIL) -\> click on
Messaging tab  

Scroll down and click on "Edit Instance"

</p>

Change Message prepopulation settings to 14 days and 750 messages  

scroll down and click SAVE ALL

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -  

USELESS STEPS FROM BLACKBERRY  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - -

</p>

A. Install SQL Express Service Pack 3 (already included in the
Blackberry Express Install!)  
[http://www.microsoft.com/downloads/details.aspx?FamilyID=3181842a-4090-4...][]

</p>

OTHERWISE theoretically you could re-use an existing SQL database (maybe
with old Blackberry data?)

</p>

Install CDO support (for Exch 2010)
[http://support.microsoft.com/kb/917481][]  

Microsoft Exchange Server MAPI Client and Collaboration Data Objects
1.2.1  
[http://www.microsoft.com/downloads/details.aspx?FamilyID=4825F157-5816-4...][]

</p>

TEST your BESADMIN account access to User Accounts  

(double click on the self extracting BESX\_express\_5.0.1.exe but DO NOT
run setup.exe)

</p>

C:\\Research In Motion\\BlackBerry Enterprise Server
5.0.1\\tools\\IEMSTest.exe

</p>

The setup application configures the startup type for the BlackBerry
Mail Store Service,  

BlackBerry Policy Service, and BlackBerry Synchronization Service to
manual.

</p>

You cannot activate a BlackBerry device that is associated with the
BlackBerry Internet Service over  

the wireless network or over wifi.

</p>
<p>
</div>
</div>
</div>
</p>

  [http://crackberry.com/blackberry-101-lecture-2-bes-and-bis-whats-difference]:
    http://crackberry.com/blackberry-101-lecture-2-bes-and-bis-whats-difference
  [http://supportforums.blackberry.com/t5/BlackBerry-Professional-Software/...]:
    http://supportforums.blackberry.com/t5/BlackBerry-Professional-Software/Installing-BESX-when-BES-5-exists/m-p/488112
  [http://www.microsoft.com/downloads/details.aspx?FamilyID=535bef85-3096-4...]:
    http://www.microsoft.com/downloads/details.aspx?FamilyID=535bef85-3096-45f8-aa43-60f1f58b3c40&displaylang=en
  [http://www.blackberry.com/btsc/viewContent.do?externalId=KB02276]: http://www.blackberry.com/btsc/viewContent.do?externalId=KB02276
  [http://support.microsoft.com/kb/823343]: http://support.microsoft.com/kb/823343
  [http://support.microsoft.com/kb/894470]: http://support.microsoft.com/kb/894470
  [https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webconsole/login]: https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webconsole/login
  [https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webdesktop/login]: https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webdesktop/login
  [http://docs.blackberry.com/en/admin/deliverables/14334/]: http://docs.blackberry.com/en/admin/deliverables/14334/
  [http://www.microsoft.com/downloads/details.aspx?FamilyID=3181842a-4090-4...]:
    http://www.microsoft.com/downloads/details.aspx?FamilyID=3181842a-4090-4431-acdd-9a1c832e65a6&displaylang=en
  [http://support.microsoft.com/kb/917481]: http://support.microsoft.com/kb/917481
  [http://www.microsoft.com/downloads/details.aspx?FamilyID=4825F157-5816-4...]:
    http://www.microsoft.com/downloads/details.aspx?FamilyID=4825F157-5816-4802-850D-67A0C5423770&displayLang=en
