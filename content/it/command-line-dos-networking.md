Title: Command Line DOS Networking
Date: 2010-11-29 16:37
Tags: DOS

[TOC]

Disk Operating System is still quite useful even in Windows XP/2003/Vista/7 if you know the commands (and parameters).

### Diagnostic and Networking Commands

`systeminfo.exe` 
> uptime, OS, originall install, ram, domain, logonserver, nic's  

> (note that window98 had a gui, winipcfg from the Run prompt)  

    systeminfo.exe /s computername /u domain\\username /p password
    ipconfig /all
    ipconfig /renew
    ipconfig /flushdns
    ping  
    tracert  
    pathping  
    netstat
    
    net view \\10.0.0.13  
    net use x: \\10.0.0.13
    net use /delete x:  
    net use /delete \\10.0.0.13\share
    net use * \\fileservername\share
    net user username newpassword /domain
    
    net localgroup /add administrators "domain users"
    
    # prompts for new password  
    net user username * /domain
    
    # Note: If you type these commands on a member server or workstation and  
    # you don't add the /domain switch, the command will be performed on the  
    # local SAM and NOT on the DC SAM.
    
    # Note: Non-administrators receive a "System error 5 has occurred. Access is denied"  
    # error message when they attempt to change the password.
    
    nbtstat -a 127.0.0.1  
    
`nbtstat [-a RemoteName] [-A IPAddress] [-c] [-n] [-r] [-R] [-RR] [-s] [-S] [Interval]`

- -a RemoteName : Displays the NetBIOS name table of a remote computer, where RemoteName is the NetBIOS computer name of the remote computer.
- The NetBIOS name table is the list of NetBIOS names that corresponds to NetBIOS applications running on that computer.

- -A IPAddress : Displays the NetBIOS name table of a remote computer, specified by the IP address (in dotted decimal notation) of the remote computer.

- -c : Displays the contents of the NetBIOS name cache, the table of NetBIOS names and their resolved IP addresses.

- -n : Displays the NetBIOS name table of the local computer. 
The status of Registered indicates that the name is registered either by broadcast or with a WINS server.

- -r : Displays NetBIOS name resolution statistics. 
On a Windows XP computer that is configured to use WINS, this parameter returns the number of names that have been resolved and registered using broadcast and WINS.

- -R : Purges the contents of the NetBIOS name cache and then reloads the #PRE-tagged entries from the Lmhosts file.

- -RR : Releases and then refreshes NetBIOS names for the local computer that is registered with WINS servers.

- -s : Displays NetBIOS client and server sessions, attempting to convert the destination IP address to a name.

- -S : Displays NetBIOS client and server sessions, listing the remote computers by destination IP address only.

- Interval : Redisplays selected statistics, pausing the number of seconds specified in Interval between each display. Press CTRL+C to stop redisplaying statistics. If this parameter is omitted, nbtstat prints the current configuration information only once.

<http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/nbtstat.mspx>

### Windows Logon Ids

- 2 interactive  
- 3 network  
- 4 batch  
- 5 service  
- 7 unlock  
- 8 network cleartext  
- 9 RunAs  
- 10 RemoteInteractive  
- 11 CachedInteractive

### Monitor Logon Script

Create your logon script and place it in the %SystemRoot%\System32 folder.  

Run Regedt32.exe and go to the following value:  

> HKEY_LOCAL_MACHINE\Software\Microsoft\WindowsNT\CurrentVersion
> \Winlogon\Appsetup

After the last entry in the Appsetup value, place a comma and a space and then enter the name and extension of the logon script you placed in the %SystemRoot%\System32 folder. 

For example, if the value of Appsetup is:  

`Usrlogon.cmd, Rmvlinks.exe`

After adding an entry for Termlogon.cmd, the value would look like:  

`Usrlogon.cmd, Rmvlinks.exe, Termlogon.cmd`

`echo %computername% %username% %date% %time% >> %homedrive%\%homepath%\log\log.txt`

### Net Use

`net use /help`

    NET USE [devicename | *] [\\computername\sharename[\volume] [password | *]]
    [/USER:[domainname\]username]
    [/USER:[dotted domain name\]username]
    [/USER:[username@dotted domain name]
    [/SMARTCARD]
    [/SAVECRED]
    [[/DELETE] | [/PERSISTENT:{YES | NO}]]
    
    NET USE {devicename | *} [password | *] /HOME
    
    NET USE [/PERSISTENT:{YES | NO}]
    
    NET USE connects a computer to a shared resource or disconnects a
    computer from a shared resource. When used without options, it lists
    the computer's connections.
    
    [devicename] Assigns a name to connect to the resource or specifies the 
    device to be disconnected. There are two kinds of
    devicenames: disk drives (D: through Z:) and printers
    (LPT1: through LPT3:). Type an asterisk instead of a
    specific devicename to assign the next available     devicename.

    \\computername Is the name of the computer controlling the shared
    resource. If the computername contains blank characters,
    enclose the double backslash (\\) and the computername
    in quotation marks (" "). The computername may be from 1 to 15 characters long.

    \sharename Is the network name of the shared resource.

    \volume Specifies a NetWare volume on the server. You must have
    Client Services for Netware (Windows Workstations)
    or Gateway Service for Netware (Windows Server)
    installed and running to connect to NetWare servers.
    password Is the password needed to access the shared resource.

    * Produces a prompt for the password. The password is
    not displayed when you type it at the password prompt.

    /USER Specifies a different username with which the connection is made.
    domainname Specifies another domain. If domain is omitted,
    the current logged on domain is used.
    username Specifies the username with which to logon.

    /SMARTCARD Specifies that the connection is to use credentials on a smart card.

    /SAVECRED Specifies that the username and password are to be saved.
    This switch is ignored unless the command prompts for username
    and password.

    /HOME Connects a user to their home directory.

    /DELETE Cancels a network connection and removes the connection
    from the list of persistent connections.

    /PERSISTENT Controls the use of persistent network connections.
    The default is the setting used last.
    YES Saves connections as they are made, and restores
    them at next logon.
    NO Does not save the connection being made or subsequent
    connections; existing connections will be restored at
    next logon. Use the /DELETE switch to remove persistent connections.
    
`NET HELP command | MORE` displays Help one screen at a time.

<http://en.wikipedia.org/wiki/Net_use>
<http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/net_use.mspx>