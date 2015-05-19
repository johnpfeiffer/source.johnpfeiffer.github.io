Title: Eclipse IDE C Wascana on Windows 7
Date: 2010-11-05 02:21
Tags: eclipse, IDE, c, win7

[TOC]

> The Wascana IDE project was discontinued: <http://speedydeletion.wikia.com/wiki/Wascana_Desktop_Developer> which is probably why links no longer work

Unfortunately I was trying to install the 64 bit version of everything below but could not find a reliable method of getting mingw 64 bit to work with Eclipse... 

See the very end for the workaround. 

(Note: having a 64 bit compiler should theoretically compile faster but with gcc 32 bit you can compile / target both 32 and 64 applications.)

1. install JRE (64 bit)
2. install Eclipse CDT (64 bit)
3. install Wascana (mingw for eclipse)
4. configure the path variable

### Install the Java Runtime Environment (JRE)

A pre-requisite is to download the JRE (Java Runtime Environment, 5.0 or higher, newer is often better).

FIRST, check if you have a 64 bit or older 32 bit system.

If you have a 64 bit system, use a "64 bit browser" to go to the java page because otherwise it will keep giving you the 32 bit version to download...

<http://www.java.com/en/download/faq/java_win64bit.xml>

The link and filename should be something like: "jre-6u22-windows-x64.exe"

Otherwise in Eclipse you may get the Error exit code=13 or "failed to load the JNI shared library"...

This will most likely install in C:\Program Files\Java (or some variant). (with the \bin\javaw.exe)

> on Windows 7 the C:\Program Files (x86)\ directory contains 32 bit installations/applications

### Install Eclipse CDT (64 bit)

The base Eclipse CDT supports integration with the GNU toolchain but may not come with a compiler...

All Linux distributions include the GNU toolchain (but might not be installed by default...)  

MinGW provides the best integration support with the CDT due to it's direct support for the Windows environment.

If you download the Eclipse IDE for C/C++ you'll get the "CDT" plugins along with the default Eclipse platform:

<http://www.eclipse.org/cdt/downloads.php>

The eclipse.ini file allows you to configure your program (e.g. specify the JRE location)  

(Notedpad2 or notepad++ handle the linux versus windows line breaks transparently...)  

e.g. insert the line to specify where your java run time environment is, maybe you have two...

#### eclipse.ini

    -vm
    C:\Java\jre6\bin\javaw.exe


Double clicking the eclipse.exe icon will start it with an empty Workbench (and use the default JRE)  

The first time you will be given the opportunity to choose your "Workspace" (aka directory where all of your files will be stored).

I prefer to have it in the Eclipse folder but obviously in a multi user setup the "My Docs" or Network Folder would also make sense... or Dropbox?   (DropBox -> Public might make Open Source Distribution even easier?)

1. File -> New -> C Project
1. Fill in the basics (you can choose the pre-made hello world app)
1. Then click on the "Go To Workbench" so you can see the Project File Explorer, Code Editor, Console   
> Window -> Preferences allows you to customize Eclipse e.g. disable usage statistics)
1. Click on the hammer symbol (Build) to ensure that you create an object file (.o) before trying to test run an executable...

### gcc error

Of course when you try to build you get an error...
    
    Internal Builder: Cannot run program "gcc" (in directory "C:\My Dropbox\workspace\hello\Debug"): CreateProcess error=2, The system cannot find the file specified
    Build error occurred, build is stopped


**Help -> Install New Software** (previously Software Installer)

Work With gets pasted the URL of the Wascana C/C++ compiler for Eclipse, then click ADD  
<http://svn.codespot.com/a/eclipselabs.org/wascana/repo>

> seems to have moved to Google Code but does not allow access, maybe <http://sourceforge.net/projects/wascana/>

Click on the Checkbox for "Wascana C/C++ Developer for Windows, then NEXT  

(review items to be installed, e.g. wascana.core) NEXT, then Agree to the License Terms...

After it downloads, installs, and restarts Eclipse you'll find the new mingw and msys directories in your Eclipse folder.

Now you have to update the Path, in Windows it's usually under System Properties -> Advanced System Settings  

Environment Variables -> System Variables scroll area, highlight "Path" (click on the edit button)

It should already have something like:
    
    %SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;

Append a semi colon to continue the long list and add:
    
    c:\eclipse\mingw\bin

> Apparently some people feel eclipse does not autodetect unless it's c:\\mingw


(Theoretically you could also try installing MingW directly from their website, which I've done, but it again is not 64 bit).

### Always 32 mingw gcc (oops)

Unfortunately fundamental flaw - even when using Eclipse 64 bit the
Install New Software gets the Wascana 32 bit mingw gcc.

The Workaround is to use the Wascana Desktop as a single download/install (which includes 32 bit versions of: JRE 1.6.0 , Mingw 3.4.5 , Eclipse IDE)

### More info

<http://code.google.com/a/eclipselabs.org/p/wascana/>

> Apparently inaccessible due to strange Google Code permissions issues


Also try: <http://mclserver.eecs.ucf.edu/trac/courses/wiki/COP3402Spring2011/InstallEclipseCpp>
