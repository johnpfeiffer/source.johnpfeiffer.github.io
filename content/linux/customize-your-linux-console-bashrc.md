Title: Customize your linux console: bashrc
Date: 2010-02-10 16:00
Author: John Pfeiffer
Slug: customize-your-linux-console-bashrc

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
The hidden file **.bashrc** in each user's home directory (\~ or or
/home/username or /root) controls the configuration of how the console
(and certain commands) behave.

</p>

NOTE CENTOS/REDHAT also uses .bash\_profile

</p>

Color is also enabled (to be added in a future edit of this post)...

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - - - - -

</p>

Here are my favorite aliases:

</p>

alias rm='rm -i'  

alias cp='cp -i'  

alias mv='mv -i'  

alias ls='ls --color=auto'  

alias ll='ls -ahl --color=auto'  

alias free='free -m'  

alias df='df -h'  

alias nano='nano -S -c'

</p>

//ls with all, hidden, long format  

//free ram in Megabytes  

//freespace on hard drive in human (Mega Giga)  

//nano text editor with smooth scroll and count of line numbers

</p>

//you can "unalias free" or you can use "\\free"

</p>

export PATH=$PATH:\~/bin

</p>

set bell-style none //no more annoying bash beeps!

</p>

xset -b //same for x windows

</p>

TO Enable it immediately go to the directory and type a period followed
by the name:  
**. .bashrc**  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - - - - -

</p>

whoami //should return what user is logged in  

echo $HOME //should return the current user's home directory, should
match what's in /etc/passwd  

echo $PATH //will list what binary executable directories are accessible
by default

</p>

e.g. normal centos user  

/usr/local/bin:/bin:/usr/bin:/home/username/bin

</p>

e.g. su -  

/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin

</p>

NOTE that if you simply use "su" you will only get the normal user
path...

</p>

.bash\_profile allows you to customize your command history size...  

(sometimes it's a section in .bashrc)

</p>

if it doesn't exist (e.g. ubuntu can't find .bash\_profile doesn't
exist)

</p>

touch \~/.bash\_profile  

chmod 700 \~/.bash\_profile

</p>

Create it and make it executable and then add the following lines...  

//defaults are 500  

HISTFILESIZE=10000  

HISTSIZE=10000

</p>
<p>
</div>
</div>
</div>
</p>

