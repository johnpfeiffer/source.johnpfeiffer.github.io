Title: Windows MessageBox: 365 programming project day two
Date: 2010-01-16 13:07
Tags: Win32, gcc

[TOC]

## Overview

Programming in Windows is like building with legos. 
It can be easy and fun but at the same time very few of us have houses or cars made of legos. 
Of course, if you're writing an application for 90% of the computer users it will probably have to run on Windows.

I've programmed with Borland, Mingw, Visual Studio and my favorite, GCC.

The story of the GNU C Compiler (and Richard Stallman) is fascinating and reading "Free as in Freedom" really opened my eyes to the details of the shoulders of the giants that I'm standing upon.

This tiny program opens up a message box that you can immediately close.
While not very useful it very often inspires new programmers with the power that they can quickly wield to get their ideas into a working program.

Anyways, here's the win32 source code...  

## Windows Text Editor

Open up your favorite text editor (I very much like [Notepad2](http://www.flos-freeware.ch/notepad2.html) or Bluefish)...


## Windows MessageBox

    /* include all of the prebuilt Windows librarys to the fun stuff like GUI */
    #include
    
    /* the "main" will return a 1 or 0 depending on how the application terminates
    */
    
    int WINAPI WinMain(
    HINSTANCE hThisInstance, /* Handle to the current instance */
    HINSTANCE hPrevInstance, /* Handle to the previous instance */
    LPSTR lpszArgument, /* pointer to command line arguments */
    int ncmdshow) /* show state of the window */
    
    {
    /* call the messagebox function, no "parent", text to include, title bar text, and ? */
    MessageBox(NULL, "Yet another program by John Pfeiffer", "Close by clicking X or OK", NULL);
    return 0; /* the "main" function now returns a good result, 0 */
    }
    
As you can see, lots of nice comments.  

I compiled the above with a windows port of GCC that I like because I can zip and move it around and it still always works.

## gcc compile windows app

I DID have to come up with the funny batch file to actually make the GCC compile it on windows:

`gcc.exe -o %1.exe %1 -Iinclude -Llib -Wall -ansi -mwindows`
