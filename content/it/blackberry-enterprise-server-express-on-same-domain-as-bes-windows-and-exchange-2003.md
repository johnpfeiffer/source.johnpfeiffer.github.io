Title: Blackberry Enterprise Server Express on same domain as BES (windows and exchange 2003)
Date: 2010-05-03 13:41
Tags: blackberry, bes, besx, windows server, exchange server 2003

[TOC]

Goal: Blackberry Express Server install: Windows 2003 with Exchange Server 2003 with BES 5 already installed

### Why Blackberry Express? 

Well it's the core Blackberry experience (email + contacts + calendar) but only requires a data plan, not a special (expensive) Blackberry plan.

The big item missing: Wireless activation is only available with BES dataplan.

<http://crackberry.com/blackberry-101-lecture-2-bes-and-bis-whats-difference>

### The dilemma, if you already have a BES installation, can you setup a BESX too?

"the two BES servers cannot be in the same BES Domain, but can be in the same AD tree and access the same exchange server."

"provided BlackBerry Enterprise Server Express is introduced as a new deployment with its own BlackBerry domain, as defined by the BlackBerry configuration database... the BlackBerry Enterprise Server and BlackBerry Enterprise Server Express can run independently in the same Microsoft Exchange environment in a Microsoft Windows Domain and would be managed from separate BlackBerry Administration Service consoles."


Apparently there is a difference between a BES Domain and a windows domain... 

Basically a BES Domain SHOULD only be the BES installation and Database, therefore you should be
able to have multiple BES installations in the same Windows Domain (e.g. a large corporation with
many exchange servers all in the same Windows Domain?).

I will try it with my own twist - Not only a separate BESX installation on a windows 2003 server BUT also creating a separate BESADMIN for the new BESX installation.

<http://supportforums.blackberry.com/t5/BlackBerry-Professional-Software/Installing-BESX-when-BES-5-exists/m-p/488112>


### Windows Server and Exchange Server Setup

1. Setup a Windows 2003 Server SP2 in the Domain (exchange sys mgmr must match version to exchange server!)

    > NEEDS at least 1GB RAM - but give it more if you suffer performance issues!

2. Install Exchange 2003 SP2 System Manager (Requires Exchange Install CD -> Deployment Tools)

    - exch2k3\setup\i386\setup.exe => Action = Custom
    - Action = Install (next to MS Exch System Management Tools) ... NEXT... 112MB required, NEXT

3. Download and Install Exchange Service Pack 2 (E3SP2ENG.exe for an old Exchange 2k3 cd)  

    - <http://www.microsoft.com/downloads/details.aspx?FamilyID=535bef85-3096-45f8-aa43-60f1f58b3c40&displaylang=en>
    - E3SP2ENG\setup\i386\update.exe (goes from version 6.5 to ? requiring 2 & 13 MB space)

4. Ensure TCP port 3101 (outgoing) is open on your firewall
5. Ensure your anti-spam is not blocking "blackberry.net"


### Permissions for a service account for BlackBerry Enterprise Server for Microsoft Exchange

<http://www.blackberry.com/btsc/viewContent.do?externalId=KB02276>

1. CREATE a user BESADMIN for the Domain (in Active Directory Users and Computers)  

    - On the exchange server with the Mailbox enabled user creation `dsa.msc` -> right click = new user

2. PERMISSION SEND AS: On the domain, `dsa.msc`

    - From the Active Directory "View" option choose Advanced Features

3. Right click on the root of the domain for Properties -> Security -> Advanced  

    - Add BESADMIN and Apply Onto = User Objects (dropdown) , Allow = Send As (checkbox)

4. Maybe? more secure: only right click on each OU or user that will be using Blackberry and  
give the BESADMIN "Send As" permission

5. PERMISSIONS Exch 2k3 System Manager -> Administrative Groups right click the Group for your BES  

    - (e.g. First Administrative Group) -> Delegate Control -> Add  Browse -> Role = Exchange View Only Administrator

6. PERMISSIONS Exchange Server: Start -> Programs -> Microsoft Exchange -> System Manager  

    Administrative Groups -> First Administrative Group -> Servers -> right click SERVERNAME (properties) Security -> find the BESADMIN and enable checkboxes:

    - Administer Information Store
    - Send As
    - Receive As

    (Click on Advanced and ensure that "Allow inheritable permissions" is checked)

7. PERMISSIONS Local Admin: each server that will have Blackberry Enterprise Server Express components

    - My Computer right click -> Manage -> Local Users and Groups -> Groups -> Administrators  
    - Add = BESADMIN

8. My Computer right click -> Properties -> Remote -> Enable Remote Desktop -> Select RemoteDesktop Users => Add = BESADMIN

9. PERMISSIONS Log on Locally and Log on as a Service  

    - Start -> Administrative Tools -> Local Security Settings => Local Policies -> User Rights Assignment
    - double click Log on Locally & Log on as a Service and add BESADMIN


### Installing Blackberry (and Database)

1. BLACKBERRY warn that you need the Microsoft hotfixes 823343 and 894470 , <http://support.microsoft.com/kb/823343> , <http://support.microsoft.com/kb/894470>

    > Verify by c:\exchsvr\bin\cdo.dll 708KB right click Version 6.5.7232 or later

2. REBOOT the server (ok, just an old habit)  

    - Log in as the BESADMIN user  
    - `C:\Research In Motion\BlackBerry Enterprise Server 5.0.1\setup.exe`

3. Create a Blackberry Configuration Database (aka BES Domain?)  
4. Blackberry Enterprise Server with all components  
5. preinstallation checklist will show you everything is ready (or will be auto installed)  
6. Install MS SQL Server 2005 Express SP3
7. note that the extracted setup folder is very similar to the target install folder  

    - `C:\Research In Motion\BlackBerry Enterprise Server 5.0.1`
    - `C:\Program Files\Research In Motion\BlackBerry Enterprise Server\`
    - enter BESADMIN password and the NAME of the Server where the SQL Express will be installed  
    - (e.g. the name of the server you are installed Blackberry Express!)

8. read the summary, click INSTALL ... watch and wait.

9. You are prompted to restart the computer - do so and then log in again with the BESADMIN user.  

10. Installation continues with the Database Information ... just click Next  

    - The database BESMgmt doesn't exist, would you like to create it ... YES

11. Enter Blackberry CAL Key e.g. besexp-123456-123456-123456-123456

    - SRP Host name: gb.srp.blackberry.com and port number: 3101 were already provided  
    - SRP identifier = (Serial Number from Blackberry download) S12345678
    - SRP authentication key = (Licence Key from Blackberry download)
    - 1234-1234-1234-1234-1234-1234-1234-1234-1234-1234

    CLICK VERIFY BUTTON 1 AND BUTTON 2 (should be successful and valid! NEEDS dashes - inbetween!)

12. Microsoft Exchange Server popup - type in the Exchange Server Name

13. Administration Settings (already filled in by default) CLICK NEXT

    > (no, I don't want to use SSL between the Blackberry Admin and my LAN browser)

14. Type in the BESADMIN password and click NEXT

15. Advanced Administration = leave as windows default click NEXT

16. click Start Services button

    - BlackBerry Router has successfully started.
    - BlackBerry Attachment Service has successfully started.
    - BlackBerry Dispatcher has successfully started.
    - BlackBerry MDS Connection Service has successfully started.
    - BlackBerry Alert has successfully started.
    - BlackBerry Administration Service - NCC has successfully started.
    - BlackBerry Administration Service - AS has successfully started.
    - BlackBerry Controller has successfully started.


17. Make a note of the Web Admin address(es)
    - <https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webconsole/login>
    - <https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webdesktop/login>

### Test your Blackberry Express Installation

1. Locally on the Server you can check services.msc (all BB services started) and eventvwr.msc (no Blackberry errors)
2. Use a browser (IE8?) <https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webconsole/login>

    - (don't worry about the Browser "Security Alert" as it will be a self signed SSL certificate, you can install the certificate and add it to Trusted Sites too...)
    - Install the RimWebComponents.cab

3. Create a user (you just need their email address - user should only be on one BES Domain so not on BES 5 and BES X at the same time!)
4. Create User with an Activation Password (e.g. something simple that times out in 4 hours)
5. Wait until it gives you the OK message that the user was created (and activation email sent)

### Assign a device to a User

<http://docs.blackberry.com/en/admin/deliverables/14334>

1. Using the Blackberry Administration Service (web)  <https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webconsole/login>

    - On the left there's a DEVICES area -> Attached Devices (if it doesn't expand?)
    - Connect the BlackBerry device to the computer.  
    - Click Manage current device -> Click Assign current device -> Search for a user account

2. Users can activate their BlackBerry devices by connecting them to computers using a USB cable or Bluetooth connection and logging in (with a browser) to the BlackBerry Web Desktop Manager.  

    - <https://SERVERNAME.DOMAIN.CO.LOCAL:3443/webdesktop/login>
    - When users complete the activation process, the BESX synchronizes through the BlackBerry Router.  
    - If a connection to the BlackBerry Router is interrupted, the data transfer continues over the  wireless network.

3. Blackberry Desktop Manager installed on a computer (and connected to their Outlook Profile)  

    - Attach/Connect to a Device

4. Not likely to be enabled but theoretically after sending the Activation Password the BlackBerry Enterprise Server sends an email message with an etp.dat

    - On the Device choose Options -> Advanced Options -> Enterprise Activation
    - "Activation request failed. A service connection is unvailable"


### Tips

1. Setup a default Password requirement

    - Policy -> Manage IT Policies -> Edit IT Policy (default) -> Device Only Tab

2. Increase the default synchronization of messages when activating

    - Servers and components -> BlackBerry Solution topology -> BlackBerry Domain -> Component view -> Email
    - Click on the "instance" (e.g. computername_EMAIL) -> click on Messaging tab  
    - Scroll down and click on "Edit Instance"
    - Change Message prepopulation settings to 14 days and 750 messages  
    - scroll down and click SAVE ALL

### Useless Steps from Blackberry

**Install SQL Express Service Pack 3 (already included in the Blackberry Express Install!)**

    - <http://www.microsoft.com/downloads/details.aspx?FamilyID=3181842a-4090-4431-acdd-9a1c832e65a6&displaylang=en>
    - OTHERWISE theoretically you could re-use an existing SQL database (maybe with old Blackberry data?)
    - Install CDO support (for Exch 2010) <http://support.microsoft.com/kb/917481>
    - Microsoft Exchange Server MAPI Client and Collaboration Data Objects 1.2.1  
    - <http://www.microsoft.com/downloads/details.aspx?FamilyID=4825F157-5816-4802-850D-67A0C5423770&displayLang=en>

**TEST your BESADMIN account access to User Accounts**

    - double click on the self extracting BESX_express_5.0.1.exe but DO NOT run setup.exe)
    - `C:\Research In Motion\BlackBerry Enterprise Server 5.0.1\tools\IEMSTest.exe`
    - The setup application configures the startup type for the BlackBerry Mail Store Service, BlackBerry Policy Service, and BlackBerry Synchronization Service to manual.
    - You cannot activate a BlackBerry device that is associated with the BlackBerry Internet Service over  the wireless network or over wifi.
