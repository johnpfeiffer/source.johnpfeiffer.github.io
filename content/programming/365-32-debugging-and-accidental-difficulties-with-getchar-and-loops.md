Title: 365-32 Debugging and "Accidental Difficulties" with getchar and loops
Date: 2010-02-01 21:46
Author: John Pfeiffer
Slug: 365-32-debugging-and-accidental-difficulties-with-getchar-and-loops

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
So for fun I tried to "port" my code (of winclockv2.c) into Linux and
compile it with gcc.  

Remarkably easy since most Linux distributions come with GCC installed
(in case you need to build a new application from source code... it
sounds scary until you've done it once or twice and then it's easy).
Just open up a text editor, paste it in, save it (getchar-loop.c). The
only thing to change was my Windows "batch" file,  
<strong>  

touch gc.sh  

chmod +x gc.sh  
</strong>  
<strong>  

nano gc.sh  

\#!/bin/bash  

gcc -o $1.exe $1 -Wall -ansi  
</strong>  
<strong>  

./gc.sh getchar-loop.c  
</strong>  

So today's entry is an offshoot program I wrote to investigate why my
previous version loop control wasn't working correctly. A little
googling showed me that this particular "getchar() buffer problem" is a
classic...

</p>
<p>
    /* 2010-02-01 john pfeiffer   getchar() only takes one character from the buffer,  but when a user presses "enter"...  that's another character in the buffer...*/  #include <stdio.h>int main(){    char c='n';    char buffer;    printf("This program will take in one character you type");     printf(" and display it back to you.\n");    printf("GeekSpeak = Demo the extra \"\n\" in the");    printf(" getchar() from user \"loop dilemma\"\n");    do    {    printf("Please enter one character and press enter...");    printf("(y to quit)... Do not attempt to type in a word or else!\n");            c = getchar();        printf("%c\n",c);    }while( c != 'y');    /* we must clear the stdin buffer of extra char's and the \n for the y!*/    do    {        buffer = getchar();        }    while (buffer != '\n' );    printf("Ha ha, to quit press 'y' again");    printf"((this corrected version will only display the first char entered).\n");    do    {        printf("Press a key or enter a word, then press enter (use y to quit):\n");            c = getchar();                do        {        buffer = getchar();        }        while (buffer != '\n' );        printf("%c\n",c);    }while( c != 'y');    return 0;}/* end of main */

</div>
</div>
</div>
</p>

