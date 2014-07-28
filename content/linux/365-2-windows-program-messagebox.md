Title: 365-2 Windows Program MessageBox
Date: 2010-01-16 13:07
Author: John Pfeiffer
Slug: 365-2-windows-program-messagebox

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Programming in Windows is like building with legos. It can be easy and
fun but at the same time very few of us have houses or cars made of
legos. Of course, if you're writing an application for 90% of the
computer users it will probably have to run on Windows.

</p>

I've programmed with Borland, Mingw, Visual Studio and my favorite, GCC.

</p>

The story of the GNU C Compiler (and Richard Stallman) is fascinating
and reading "Free as in Freedom" really opened my eyes to the details of
the shoulders of the giants that I'm standing upon.

</p>

This tiny program opens up a message box that you can immediately close.
While not very useful it very often inspires new programmers with the
power that they can quickly wield to get their ideas into a working
program.

</p>

Anyways, here's the code...  

Open up your favorite text editor (I very much like Notepad2 or
Bluefish)...

</p>

/\* include all of the prebuilt Windows librarys to the fun stuff like
GUI \*/  

\#include

</p>

/\* the "main" will return a 1 or 0 depending on how the application
terminates  

\*/

</p>

int WINAPI WinMain(  

HINSTANCE hThisInstance, /\* Handle to the current instance \*/  

HINSTANCE hPrevInstance, /\* Handle to the previous instance \*/  

LPSTR lpszArgument, /\* pointer to command line arguments \*/  

int ncmdshow) /\* show state of the window \*/

</p>

{  

/\* call the messagebox function, no "parent", text to include, title
bar text, and ? \*/  

MessageBox(NULL, "Yet another program by John Pfeiffer", "Close by
clicking X or OK", NULL);  

return 0; /\* the "main" function now returns a good result, 0 \*/  

}

</p>

As you can see, lots of nice comments.  

I compiled the above with a windows port of GCC that I like because I
can zip and move it around and it still always works.

</p>

I DID have to come up with the funny batch file to actually make the GCC
compile it on windows:

</p>

gcc.exe -o %1.exe %1 -Iinclude -Llib -Wall -ansi -mwindows

</p>

Here's the binaries:  
[http://kittyandbear.net/c-programming-guides/gcc-2-9-5-windows.zip][]

</p>

[http://kittyandbear.net/c-programming-guides/windows-messagebox.zip][]

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

  [http://kittyandbear.net/c-programming-guides/gcc-2-9-5-windows.zip]: http://kittyandbear.net/c-programming-guides/gcc-2-9-5-windows.zip
  [http://kittyandbear.net/c-programming-guides/windows-messagebox.zip]:
    http://kittyandbear.net/c-programming-guides/windows-messagebox.zip
  [Programming]: http://john-pfeiffer.com/category/tags/programming
