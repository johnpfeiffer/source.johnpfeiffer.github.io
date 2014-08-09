Title: 365-22 Script Programming: Linux Expect Script passwd
Date: 2010-01-21 22:11
Author: John Pfeiffer
Slug: 365-22-script-programming-linux-expect-script-passwd

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Is writing a Script still programming? What the heck is a Script? A
script is a written set of instructions for a platform (usually an
Operating System) that makes the computer (or hardware) do something.
Sounds a lot like a Program.

</p>

Well... A computer software program is usually source code (written by a
human) that is then "compiled" into "machine code" which a machine can
understand - except that there's also a linker and loader to figure out
exactly what places in memory (and for what piece of hardware) the
Program will run - finally turning it into Object code and then an
Executable (usually called binary because it's in 1's and 0's directly
in the language of the hardware).

</p>

A script gives hardware a set of commands indirectly through another
piece of software (it's environment/platform, e.g. DOS, Python, Windows
OS, GNU Linux OS, etc.). The software then executes those commands
(which often then tell an Operating System which then tells Hardware to
to do something - like clearing the screen or adding some numbers).

</p>

So maybe html is even less Programming like than a script! Since it only
tells a browser (a specific application) how to format/display data!?!?!

</p>

Ah, enough semanticarating!

</p>

What happens if you're running a script and somewhere it requires user
input?

</p>

"Expect" is a piece of software that "waits" for input from the linux
operating system command line...

</p>

apt-get install expect //to install it on linux ubuntu  

yum install expect //to install it on linux centos/redhat

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - -

</p>

touch test-script.sh //create the file  

chmod +x test-script.sh //make the file an executable in linux  

nano test-script.sh //edit the file to enter our script commands

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - -

</p>

\#!/usr/bin/expect  

set timeout 1  

send "passwd USER\\n"  

expect "Password: "  

send "password\\n"  

sleep 1  

interact

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - -

</p>

\*First we tell the operating system what program (environment platform)
will actually be able to read and execute the instructions (normally
linux uses BASH but in this case it's EXPECT).

</p>

\*Setting the timeout means that we will wait at least and at most 1
second before a non responding command is skipped to execute the next
command.

</p>

\*Send tells the operating system something (e.g. we want to run the
change USER's password program)

</p>

\*The expect command tells the script to wait for the operating system
to prompt the user to type in a password.

</p>

\*Once the operating system responds (with exactly what we "expected")
the script continues by sending (just as if a user typed it in) some
predetermined password picked by the script writer.

</p>

\*Finally we tell our script to sleep for one second after all of it's
hard work.

</p>

\*Oh, and it's very important to "interact", which returns the command
prompt back to the user/operating system.

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - -

</p>

Whew... that's just the tip of the iceberg of how "expect" greatly
extends the functionality of Linux scripts!

</p>

Later I hope to demonstrate some VBScript (for windows) and maybe even a
script on how to run a "non interactive FTP session" (as most FTP
programs require "interaction" aka human at the keyboard)...

</p>
<p>
</div>
</div>
</div>
</p>

