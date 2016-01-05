Title: Fix Byobu infinite scroll bug on Ubuntu 12.04 Precise Pangolin
Date: 2013-02-15 17:36
Slug: fix-byobu-infinite-scroll-bug-on-ubuntu-1204-precise-pangolin
Tags: byobu, linux, ubuntu

[TOC]

After installing Ubuntu Server 12.04 (Precise Pangolin) I was disappointed to see that one of my favorite utilities, byobu (an improvement on the classic screen = multi ssh screen with status and hotkeys), had an infinite scroll problem. 

(Quick, type exit before your screen disappears entirely!)

Amazingly this bug shipped in the official Ubuntu Release even though byobu 5.17 lists it as a fixed.

## Easy workaround is:

1. `byobu-config`
1. Toggle status notifications
1. Use the arrow keys to scroll down and space bar to disable the logo 
1. Tab and Enter to Apply -> then Exit 

Now you can safely use "byobu" on the command line in Ubuntu 12.04! (apparently not persisting in 12.04.2?)

p.s. Control + a (screen mode) and then Control + a , then c ... 
now you've got multiple screens! 

(Control + a + 0 to go to screen 0, control + a + a to jump to the last used screen)

<https://help.ubuntu.com/community/Byobu>

Of course you can always use normal BASH navigation: <http://www.gnu.org/software/bash/manual/html_node/Commands-For-Moving.html>

A fix for Windows Putty users ... Window -\> Translation -\> UTF8 (the ISO-8859 + byobu UTF8 logo = ugh)

(An untested alternate workaround: .byobu/status::tmux_left : "logo" -> "\#logo" )

## UPDATE for 12.04.2!

byobu in Ubuntu 12.04 uses tmux as the backend. You can change this by running byobu-select-backend and selecting screen

Thanks for the tip Eric!

ALTERNATE:
    .byobu/status::tmux_left : "logo" -> "#logo" )

## byobu installation and basics

### installing a better tmux (multiple remote virtual console screens)

BYOBU = BETTER GUI FOR SCREEN + CPU/RAM USAGE + DATETIME <https://help.ubuntu.com/community/Byobu>

(an improvement on the classic "screen" = multi ssh screen with status and hotkeys)

    sudo apt-get install byobu
    byobu-config
>    Toggle status notifications -> spacebar to disable logo -> Apply -> Exit

    byobu

- F2 ... or control + a , then c to create a new screen
- F3 to move to a previous screen
- F4 to move to the next screen
- control + a , then 0 = to go to screen zero, etc.
- control + a , then a = to go to the last used screen

    byobu-enable
> will have it start on every ssh connection

    byobu-disable
> stops auto-starting of byobu


### If byobu seems stuck when using vi

try Control + Q  (or Control + S)

### Moving the cursor in byobu (f7 and beyond)
F7 = scrollback mode , vi like commands to search and copy paste

    h - Move the cursor left by one character
    j - Move the cursor down by one line
    k - Move the cursor up by one line
    l - Move the cursor right by one character
    0 - Move to the beginning of the current line
    $ - Move to the end of the current line
    G - Moves to the specified line (defaults to the end of the buffer)
    / - Search forward
    ? - Search backward
    n - Moves to the next match, either forward or backword


## screen - the previous generation of remote virtual console utility

    sudo apt-get install screen

SSH into your machine and type:

    screen           //to start your screen session.
    ctrl + a + c     //to create a new session
    ctrl + a + d     //to disconnect from the screen session, then log out of your SSH session
    when you get disconnected/dropped by the network then log back in using SSH

    screen -ls          //shows current screen sessions

    There is a screen on:
            19894.pts-1.servername    (Attached)
    1 Socket in /var/run/screen/S-username.


    screen -r    //When you're ready to reconnect to the last screen session

    screen -d 19894         //detach the screen from the other ssh session
    screen -r 19894         //connect to the screen to see everything's ok

    ctrl-a-d                //detach from the screen

    who -u                  //find the id of the "lost" ssh session
    sudo kill sessionid     //kill off the disconnected ssh session

    screen -r 19894         //resume work

    screen -r -d                //force detach an existing and attach a session


setting the config for no visual bell!

in your /home/USERNAME (or /root) directory

    touch .screenrc

    vbell off

