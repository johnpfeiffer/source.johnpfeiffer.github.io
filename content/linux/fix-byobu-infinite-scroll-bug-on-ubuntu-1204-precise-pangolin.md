Title: Fix Byobu infinite scroll bug on Ubuntu 12.04 Precise Pangolin
Date: 2013-02-15 17:36
Slug: fix-byobu-infinite-scroll-bug-on-ubuntu-1204-precise-pangolin
Tags: byobu, linux, ubuntu

[TOC]

After installing Ubuntu Server 12.04 (Precise Pangolin) I was disappointed to see that one of my favorite utilities, byobu (an improvement on the classic screen = multi ssh screen with status and hotkeys), had an infinite scroll problem. 

(Quick, type exit before your screen disappears entirely!)

Amazingly this bug shipped in the official Ubuntu Release even though byobu 5.17 lists it as a fixed.

## Easy workaround is:

    byobu-config
    Toggle status notifications
    Use the arrow keys to scroll down and space bar to disable the logo  
    Tab and Enter to Apply -> then Exit  

Now you can safely use "byobu" on the command line in Ubuntu 12.04!

p.s. Control + a (screen mode) and then Control + a , then c ... 
now you've got multiple screens! 

(Control + a + 0 to go to screen 0, control + a + a to jump to the last used screen)

<https://help.ubuntu.com/community/Byobu>

A fix for Windows Putty users ... Window -\> Translation -\> UTF8 (the ISO-8859 + byobu UTF8 logo = ugh)

(An untested alternate workaround: .byobu/status::tmux_left : "logo" -> "\#logo" )

## UPDATE for 12.04.2!

byobu in Ubuntu 12.04 uses tmux as the backend. You can change this by running byobu-select-backend and selecting screen

Thanks for the tip Eric!
