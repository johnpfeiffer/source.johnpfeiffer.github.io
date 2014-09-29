Title: Eclipse IDE C Wascana on Windows 7
Date: 2010-11-05 02:21
Author: John Pfeiffer
Slug: eclipse-ide-c-wascana-on-windows-7

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Unfortunately I was trying to install the 64 bit version of everything
below but could not find a reliable method of getting mingw 64 bit to
work with Eclipse... See the very end for the workaround.

</p>

(Note: having a 64 bit compiler should theoretically compile faster but
with gcc 32 bit you can compile / target both 32 and 64 applications.)

</p>

\1. install JRE (64 bit)  

\2. install Eclipse CDT (64 bit)  

\3. install Wascana (mingw for eclipse)  

\4. configure the path variable

</p>

A pre-requisite is to download the JRE (Java Runtime Environment, 5.0 or
higher, newer is often better).

</p>

FIRST, check if you have a 64 bit or older 32 bit system.

</p>

If you have a 64 bit system, use a "64 bit browser" to go to the java
page because otherwise it will keep giving you the 32 bit version to
download...

</p>

[http://www.java.com/en/download/faq/java\_win64bit.xml][]

</p>

The link and filename should be something like:
"jre-6u22-windows-x64.exe"

</p>

Otherwise in Eclipse you may get the Error exit code=13 or "failed to
load the JNI shared library"...

</p>

This will most likely install in C:\\Program Files\\Java (or some
variant). (with the \\bin\\javaw.exe)  

(Note on Windows 7 the C:\\Program Files (x86)\\ directory contains 32
bit installations / applications.)

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -  

The base Eclipse CDT supports integration with the GNU toolchain but may
not come with a compiler...

</p>

All Linux distributions include the GNU toolchain (but might not be
installed by default...)  

MinGW provides the best integration support with the CDT due to it's
direct support for the Windows environment.

</p>

If you download the Eclipse IDE for C/C++ you'll get the "CDT" plugins
along with the default Eclipse platform:

</p>

[http://www.eclipse.org/cdt/downloads.php][]

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -

</p>

The eclipse.ini file allows you to configure your program (e.g. specify
the JRE location)  

(Notedpad2 or notepad++ handle the linux versus windows line breaks
transparently...)  

e.g. insert the line to specify where your java run time environment is,
maybe you have two...

</p>

-vm  

C:\\Java\\jre6\\bin\\javaw.exe

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -

</p>

Double clicking the eclipse.exe icon will start it with an empty
Workbench (and use the default JRE)  

(The first time you will be given the opportunity to choose your
"Workspace" (aka directory where  

all of your files will be stored, I prefer to have it in the Eclipse
folder but obviously in a multi  

user setup the "My Docs" or Network Folder would also make sense... or
Oxygen Cloud / Dropbox?  

DropBox -\> Public might make Open Source Distribution even easier? )

</p>

File -\> New -\> C Project

</p>

Fill in the basics (you can choose the pre-made hello world app)  

Then click on the "Go To Workbench" so you can see the Project File
Explorer, Code Editor, Console  

(NOTE Window -\> Preferences allows you to customize Eclipse e.g.
disable usage statistics)

</p>

Click on the hammer symbol (Build) to ensure that you create an object
file (.o) before trying to test run  

an executable...

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -

</p>

Of course when you try to build you get an error...

</p>

Internal Builder: Cannot run program "gcc" (in directory "C:\\My
Dropbox\\workspace\\hello\\Debug"): CreateProcess error=2, The system
cannot find the file specified  

Build error occurred, build is stopped

</p>

Help -\> Install New Software (previously Software Installer)

</p>

Work With gets pasted the URL of the Wascana C/C++ compiler for Eclipse,
then click ADD  
[http://svn.codespot.com/a/eclipselabs.org/wascana/repo][]

</p>

Click on the Checkbox for "Wascana C/C++ Developer for Windows, then
NEXT  

(review items to be installed, e.g. wascana.core) NEXT, then Agree to
the License Terms...

</p>

After it downloads, installs, and restarts Eclipse you'll find the new
mingw and msys directories in  

your Eclipse folder.

</p>

Now you have to update the Path, in Windows it's usually under System
Properties \> Advanced System Settings  

Environment Variables -\> System Variables scroll area, highlight "Path"
(click on the edit button)

</p>

It should already have something like:  

%SystemRoot%\\system32;%SystemRoot%;%SystemRoot%\\System32\\Wbem;

</p>

Append a semi colon to continue the long list and add:  

c:\\eclipse\\mingw\\bin

</p>

(Apparently some people feel eclipse does not autodetect unless it's
c:\\mingw)

</p>

(Theoretically you could also try installing MingW directly from their
website, which I've done, but it again is not 64 bit).  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -

</p>

Unfortunately fundamental flaw - even when using Eclipse 64 bit the
Install New Software gets the Wascana 32 bit mingw gcc.

</p>

The Workaround is to use the Wascana Desktop as a single download /
install (which includes  

32 bit versions of: JRE 1.6.0 , Mingw 3.4.5 , Eclipse IDE)

</p>

[http://code.google.com/a/eclipselabs.org/p/wascana/][]

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Programming][]

</div>
</p>

  [http://www.java.com/en/download/faq/java\_win64bit.xml]: http://www.java.com/en/download/faq/java_win64bit.xml
  [http://www.eclipse.org/cdt/downloads.php]: http://www.eclipse.org/cdt/downloads.php
  [http://svn.codespot.com/a/eclipselabs.org/wascana/repo]: http://svn.codespot.com/a/eclipselabs.org/wascana/repo
  [http://code.google.com/a/eclipselabs.org/p/wascana/]: http://code.google.com/a/eclipselabs.org/p/wascana/
  [Programming]: http://john-pfeiffer.com/category/tags/programming
