Title: Xubuntu hotkey shortcuts and Zoom (also for xfce)
Date: 2014-10-08 16:00

[TOC]

Interacting with the computer is so much faster with keyboard hotkey shortcuts and other tricks, these are applicable as of Xubuntu 14.04

### Xubuntu Zoom (magnifier)

Alt + scrollwheel up to Zoom in 
> or on a laptop with a touchpad two finger swipe up

Alt + scrollwheel down to Zoom out
> or on a laptop with a touchpad two finger swipe down


### Hotkey Application Shortcuts

**Mouse (start button) -> Settings -> Settings Manager -> Keyboard -> Application Shortcuts**

`Add -> sh -c "sleep 1 && xset dpms force off" -> OK (will open another popup)`

`press control + alt + q on the keyboard (the popup will go away and the hotkeys will be saved)`

Double click on the command in the Command column to edit the command

Double click on the hotkeys in the Shortcut column to modify the hotkey combination

- sleep 1 && xset dpms force off		control + alt + q
- exo-open --launch TerminalEmulator	control + alt + t
- gnome-calculator			control + alt + g			
- /usr/bin/galculator			control + alt + g
- /usr/bin/leafpad --tab-width=4		control + alt + f  

- > vi /usr/share/applications/leafpad.desktop  Exec=leafpad --tab-width=4 %f

- /usr/bin/chromium-browser		control + alt + a

- /usr/bin/filezilla			control + alt + i
- /opt/pycharm/bin/pycharm.sh		control + alt + p
- xfce4-screenshooter -r			printscreen
- > select region (-f fullscreen , -w active window)

- amixer set Master 5%- -q   		Alt + Down
- amixer set Master 5%+ -q  		Alt + Up
- xflock4  				control + alt + delete
- retext					control + alt + r


**/home/ubuntu/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-keyboard-shortcuts.xml**

**/etc/xdg/menus/xfce-applications.menu**


### XFCE Keyboard Shortcuts

Settings Editor -> xfce4-keyboard-shortcuts

commands -> custom... New

/commands/custom/<Control><Alt>f
leafpad

/xfwm4/custom/<Control><Alt>d

show_desktop_key

/commands/custom/<Super>e

mousepad

exo-open --launch FileManager


### Ubuntu Keyboard Shortcuts

ubuntu 12.04 keyboard shortcuts

System Settings -> Keyboard (may not be visible so type it in the search box) -> Shortcuts 

Either modify an existing shortcut (i.e. disable one that is annoying)

OR Custom Shortcuts -> + (add a new one)

e.g.

    name: chromium
    command: /usr/bin/chromium-browser

Then highlight the row (clicking on the right area where it's "disabled") and type the key combination desired to trigger the shortcut (e.g. control + alt + a)


HINTS: `sudo find / -iname "*chromium*"`

`sudo which chromium-browser`