Title: Customize your linux bash console: bashrc, aliases, colors, hotkeys, history length
Date: 2010-02-10 16:00
Tags: linux, bash, bashrc, bash alias, bash history

[TOC]

The hidden file **.bashrc** in each user's home directory (~ or or /home/username or /root) controls the configuration of how the console (and certain commands) behave.

NOTE CENTOS/REDHAT also uses **.bash_profile**

The shell is the program that interfaces between the user and the Linux kernel. There are different shells with different features.

Ash is a reimplementation of the System V shell  May 6, 1989

GNU Bourne Again Shell  Bash is an sh-compatible command language interpreter that
 executes commands read from the standard input or from a file. Bash also incorporates
  useful features from the Korn and C shells (ksh and csh)

June 18, 1999
Zsh is a command interpreter which mostly resembles the Korn shell. Includes a
 command-line editor and many other enhancements over the other shells. 

### Favorite Aliases

Here are my favorite aliases that are in my .bashrc:

|command|explanation|
|---|---|
|`alias ls='ls --color=auto'`|color highlighting of a directory listing|
|`alias ll='ls -ahlF --color=auto'`|directory listing: all, hidden too, long format, show type with symbols: dir/|
|`alias la='ls -A'`|directory listing almost all so exclude . and ..|
|`alias l='ls -CF'`|list in columns with trailing type symbols: dir/|
|`alias free='free -m'`|free RAM in megabytes|
|`alias df='df -h'`|disk free in human sizes|
|`alias nano='nano -c -S -u'`|simple editor with cursor position, smooth scroll, and undo|
|`alias gp='git pull'`|pull remote changes with less typing|
|`alias gt='git status'`|current git status with less typing|
|`alias gw='git whatchanged'`|git history with less typing|
|`alias gd="GIT_PAGER='' git diff"`|git history with less typing|
|`alias rm='rm -i'`|extra prompt before deleting a file or directory|
|`alias cp='cp -i'`|extra prompt before overwriting a file or directory with a copy|
|`alias mv='mv -i'`|extra prompt before overwriting a file or directory with a move|
|`export PATH=$PATH:~/bin`|your own local scripts are loaded in the console|
|`set bell-style none`|no more annoying bash beeps!|
|`xset -b`|no more annoying bash beeps for x windows|

`alias ssh='ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'`
> ssh will not check nor store remote server signatures: insecure!

`unalias free` or `\free`
> NOTE to escape or override the alias


To enable the new aliases immediately go to the directory type one of the following:
`. ./bashrc` or `source ~/.bashrc`

> nano /home/username/.bashrc or /root/.bashrc
> export PATH=$PATH:~/bin


- - -

.bashrc or .profile are where your shell (BASH) gets it's initial settings:

    :::bash
    root:~# ls -al
    total 20
    drwxr-xr-x  2 root root 4096 Mar 29 21:56 .
    drwxr-xr-x 21 root root 4096 Mar 29 22:26 ..
    -rw-------  1 root root  183 Mar 29 22:31 .bash_history
    -rw-r--r--  1 root root 2225 Mar 29 22:31 .bashrc
    -rw-r--r--  1 root root  141 May 15  2007 .profile

> if a lot of commands start failing try a cat /etc/passwd and see if you are using **/sbin/bash** or **/bin/sh** - the older and less functional shell

|command|explanation|
|---|---|
|`whoami`|display what user is logged in or is being impersonated by su|
|`echo $HOME`|display the current user's home directory (which should match what's in /etc/passwd)|
|`echo $PATH`|list what binary executable directories are accessible by default|
|normal centos user has|**/usr/local/bin:/bin:/usr/bin:/home/username/bin**|
|changing to root with: `su -`|**/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin**|

NOTE that if you simply use "su" you will only get the normal user path...

### increasing bash history length

.bash_profile allows you to customize your command history size... (sometimes it's a section in .bashrc)

if it doesn't exist (e.g. ubuntu can't find it ".bash_profile doesn't exist"), create it and make it executable and then add the following lines...  

    echo "#defaults are 500" >> .bash_profile
    echo "HISTFILESIZE=10000" >> .bash_profile
    echo "HISTSIZE=10000" >> .bash_profile    
    chmod 700 ~/.bash_profile
    

HISTFILE is where the history saves to (/dev/null = no history file), the default is: ~/.bash_history.

HISTFILESIZE how many commands to keep in HISTFILE (default 500)

HISTSIZE how many commands to keep in the current session (default 500)
 
HISTIGNORE Controls which commands to ignorea nd not save. The variable takes a list of colon separated patterns. Pattern & matches the previous history command.


`cut -f1 -d" " .bash_history | sort | uniq -c | sort -nr | head -n 30`
> what command you've typed the most

`cut -f1 -d" " /root/.bash_history | sort | uniq -c | sort -nr | head -n 30`
> what command root has typed the most

`cut -f1 /root/.bash_history | sort | uniq -c | sort -nr | head -n 30`
> what command + parameters root has typed the most

### Example default .bash_profile
    
    # Get the aliases and functions
    if [ -f ~/.bashrc ]; then
        . ~/.bashrc
    fi
    
    # User specific environment and startup programs
    PATH=$PATH:$HOME/bin
    export PATH
    
    # note this last command only exists in the /root/.bash_profile
    unset USERNAME			
    
- - -

`nano .bashrc`
> uncomment (remove the leading # from the two lines with --color=auto)

    # enable color support of ls and also add handy aliases
    if [ "$TERM" != "dumb" ]; then
        eval "`dircolors -b`"
        alias ls='ls --color=auto'
        #alias dir='ls --color=auto --format=vertical'
        #alias vdir='ls --color=auto --format=long'
    fi
    
    # ALSO, uncomment the following line to get a color prompt:

    # Comment in the above and uncomment this below for a color prompt
    #PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[$
    
And comment out the two lines above it...


### hotkeys

|command|explanation|
|---|---|
|ctrl-r| to search through your command history in reverse (newest to oldest)|
|ctrl-k| to clear all the text after cursor|
|ctrl-u| to clear all the text before cursor|
|ctrl-a| move to beginning of the current |
|ctrl-e| move to end of the current|
|ctrl-f| move forward one char|
|ctrl-b| move backward one word|


### Example recycle bin for root

Now you can do fun things like have a "recycle bin" for root:

`mkdir /recycle-bin`
`echo "mv $1 /recycle-bin" > del.sh`
`chmod 700 del.sh`

AND THEN VERIFY WITH: 

1. touch test.txt
1. ./del.sh test.txt
1. ls -al /recycle-bin

- - -

### bashrc - xterm - ANSI escape color codes

**.bashrc**

    alias xterm1='xterm -fg black -bg white'

nano /home/username/.icewm/toolbar
prog xterm xterm1 x-terminal-emulator

nano /home/username/.icewm/keys

key "Ctrl+Alt+j" xterm -fg black -bg white


FIRST print out what colors are available...

    dircolors -p > dircolors.txt

after reading through that and being thoroughly mystified...

    echo -e "\033[44;37;5m ME \033[0m COOL"

if you put the above into your bash shell you'll see that the ANSI 
control of colors is basically what controls BASH/TERMINALS...

    Attribute codes:
    00=none 01=bold 04=underscore 05=blink 07=reverse 08=concealed
    
    Text color codes:
    30=black 31=red 32=green 33=yellow 34=blue 35=magenta 36=cyan 37=white
    
    Background color codes:
    40=black 41=red 42=green 43=yellow 44=blue 45=magenta 46=cyan 47=white
    
    Black       0;30     Dark Gray     1;30
    Blue        0;34     Light Blue    1;34
    Green       0;32     Light Green   1;32
    Cyan        0;36     Light Cyan    1;36
    Red         0;31     Light Red     1;31
    Purple      0;35     Light Purple  1;35
    Brown       0;33     Yellow        1;33
    Light Gray  0;37     White         1;37
    
    echo -e "\e[1;34mThis is a blue text.\e[0m"
    
    so \e[attribute code; text color code0m
    
    framed by the [ --- 0m 
    note that the \033 in the first example has been replaced by \e
    
    echo -e "\e[30;470mtest"
    
    FOREGROUND WHITE (in case you accidentally set it to black on black)
    echo -e "\033[37m\]" 
    
    BACKGROUND WHITE
    echo -e "\033[47m\]"
    
    FOREGROUND BLACK
    echo -e "\033[1;30m\]"
    
    
    
    changing the foreground and background color of your bash shell
    (and font?)
    
    TEMPORARY SOLUTION
    
    xterm -fg *color* -bg *color*
    
    PERMENANT SOLUTION
    
    
    .Xdefaults file in your home directory
 