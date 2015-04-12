Title: Replace Windows XP SP3 notepad with notepad2
Date: 2010-02-02 13:41
Tags: windows, notepad, notepad2

Each XP service pack seems to make the process of replacing notepad.exe with notepad2.exe even more complex (somebody at Microsoft really likes the original notepad)...

**Updated steps for SP3:**

Download a replacement text editor: <http://www.flos-freeware.ch/notepad2.html>

> (If you have the \servicepackfiles\i386 folder...)

`rename C:\WINDOWS\ServicePackFiles\i386\notepad.exe C:\WINDOWS\ServicePackFiles\i386\notepad.exe.bak`

Now rename notepad2.exe notepad.exe and copy it into:

    C:\WINDOWS\ServicePackFiles\i386\
    C:\WINDOWS\system32\dllcache
    C:\WINDOWS\system32\notepad.exe
    C:\WINDOWS


Check that your new notepad is in place (the filesize change from 68k to 243k)...

(In service pack 2 it would complain with 2 popups and you would just hit cancel both times... as \system32 files were immediately replaced by the "original" from dllcache)

ADDITIONALLY, the "file type" may get messed up so you might have to have notepad2.exe in the C:\ and when you double click a .txt from windows explorer you'll have to choose Open With other -> Browse -> c:\notepad2.exe
