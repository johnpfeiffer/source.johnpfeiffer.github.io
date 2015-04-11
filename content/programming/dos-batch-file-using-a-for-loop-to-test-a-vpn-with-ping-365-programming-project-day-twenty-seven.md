Title: DOS batch file using a for loop to test a vpn with ping: 365 programming project day twenty seven
Date: 2010-01-27 20:58
Tags: DOS, bat, for loop, map network drive, windows

Once again my work demands creative programming solutions. I have a new ISP with a brand new modem and I want to know if a VPN will stay connected overnight... BUT it's not a good test without some traffic...

Enter the DOS/Windows Batch file... like a linux script or VBS, a .bat file is a series of commands which allow a creative programmer to do quite a bit.

Using a text editor create your first .bat file: ping-test-vpn.bat  

(Yes, I realize we skipped the steps using echo "hello world", that a % sign means a variable, defining that a mapped network drive to a folder on another computer... oh well, break this one into little pieces if it's too much to swallow at once.)


    :::batchfile
    REM batch program to test and log the stability/uptime of a remote
    REM computer using ping and copying a file
    REM is a "remark" or a comment that the computer will ignore
    
    REM create a time stamp and append it to the end of the file
    echo %date% %time% >> ping-log.txt
    
    REM see if we can reach the remote computer and append to the log file
    ping -n 1 192.168.1.30 >> ping-log.txt
    
    REM Map network drive where we will copy files back and forth
    net use z: \192.168.1.30\groups\shared
    
    REM copy a 1.8 MB file to the remote computer (DOS overwrites by default)
    copy install_flash_player.exe z:\
    
    REM list the files in the remote directory (including timestamp) and log it
    dir z:\install* >> ping-log.txt
    
    REM remove our mapped network drive
    net use z: /delete
    
    echo "-------------------------------------------------------------" >> ping-log.txt
    
    REM ping 6 times takes about 5 seconds - like a (324/6) *5 = 4.5 mins "pause"
    REM redirect to NUL sends the output nowhere to not fill the screen
    ping -n 324 127.0.0.1 >NUL


Once you've saved your .bat file, rather than just double click it (which works), I prefer to use Start -> Run -> cmd.exe to open up a DOS command line prompt. From there I cd to c:\\directory\\ and find the .bat file... then I type in:  

`ping-test-vpn.bat`

Watching the output can be fascinating - programming (and debugging) is certainly the most engaging when it's interactive.

With the above file using the bandwidth of the VPN to copy a file and pause we then need to repeat this all night long.

    REM forloop counting variable IN (start,step,end) DO command  
    FOR /L %%i IN (1,1,2) DO ping-test-vpn.bat

`for-loop-counter.bat`
    
High level network testing is fundamentally the same, though they obviously want to introduce variables like large packets, lost packets,random intervals, and contention issues.

Wow, another day and another program (useful even!)
