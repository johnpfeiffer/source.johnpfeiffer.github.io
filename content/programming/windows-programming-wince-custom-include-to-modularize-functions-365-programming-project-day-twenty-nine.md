Title: WinCE Custom Include to Modularize Functions: 365 programming project day twenty nine
Date: 2010-01-30 13:57
Tags: win ce, win32, gcc, best practice

I've again used some "empty" time in the London Tube to stretch my brain a little bit by doing some more WinCE Windows Programming.
 
While it may not seem like much of an accomplishment, using my fingernail on the screen keyboard to eke out code on a moving underground train requires a certain zen attitude... wait... wait... hit the key... oh... the wrong thing showed up (because obviously I pressed the right key)...
 
ok, backspace and do it again... oh, that wasn't backspace, that was ]... and sometimes it looks like ]]]]].
 
I'm trying to not only read/learn best practice, but practice best practice.

Once again I am relying on PGCC (pocket GCC) though it does apparently have the limitation of only doing WinMain (not c's usual main); I suppose a "big goal" I might have for WinCE programming would be to one day use it to compile GCC on my IPAQ (overnight?). 

The ever mysterious "c.bat" (yes, the filename is very short for onscreen typing challenged fingernails)


    \pgcc\cc1plus \pgcc\cwm.txt -o \pgcc\cwms.s -I \pgcc\include 
     -include \pgcc\fixincl.h -fms-extensions \pgcc\as \pgcc\cwms.s 
     -o \pgcc\cwmo.o \pgcc\ld \pgcc\cwmo.o -o \pgcc\cwme.exe -L \pgcc\lib 
     -l cpplib -l corelibc -l coredll -l aygshell -l runtime -l portlib CWM.TXT

### CWM.TXT

    :::c
    #define WIN32_LEAN_AND_MEAN
    #include  #include "func.h"
    /*  MODULAR BY INCLUDE    Function definitions hidden in includesabove I've told the compiler to use the func.h file as well as windows.h */
    /* declare the function before main */
    int outputText();
    int APIENTRY WinMain( HINSTANCE hInstance, HINSTANCE hPrevInstance, 
        LPTSTR lpCmdLine, int ncmdshow )
    {
        printf("pre function \n");
        /* this is the big moment, calling a function defined in another file! */
        outputText();
        printf("post function \n");
        /* So that if I run it in the Windows Explorer I can still see the output */
        printf("Press return  to quit");
        getchar();
        return 0;
    }
    
    
### func.h

    :::c
    /* function definitions go here */
    int outputText() {
        printf("function include \n");
        return 0;
    }
