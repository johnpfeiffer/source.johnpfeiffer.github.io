Title: Fix Fn screen brightness Ubuntu 14.04 intel graphics
Date: 2014-08-26 22:36

I discovered post upgrade that Ubuntu 14.04 has a glaring bug with the Intel graphics card (which was working fine in 12.04), the Fn key no longer controlled the brightness.

`sudo su`

`ls /sys/class/backlight`

> if it lists intel_backlight then this solution of adding the following should work for you too...

`vi /usr/share/X11/xorg.conf.d/20-intel.conf`

    Section "Device"
        Identifier  "card0"
        Driver      "intel"
        Option      "Backlight"  "intel_backlight"
        BusID       "PCI:0:2:0"
    EndSection
    
Log out and log back in, function keys should now control the brightness again (no more glaring bug!)