Title: 365-? Windows CE programming: A win32 api button
Date: 2010-03-16 20:27
Author: John Pfeiffer
Slug: 365-windows-ce-programming-a-win32-api-button

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Win CE uses a subset of the win32 API which is neat because technically
anything written for it can be compiled for a "full" windows as well.   

  

Even though the Win32 API is very outdated I prefer the concept of
building blocks and getting your hands dirty with implementation -
that's how you really learn how things work. C\# and .Net, especially
with a super GUI IDE, make it easy to quickly build something but also
obscure why performance might be slow, why different parts aren't
integrating together, and really require you to build based on the
vision of the platform designers - for better or for worse.  

  

This is probably why many programs written in C that are speed critical
have important parts hand written in assembly. So here's a Windows API
button for Win CE...  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -  

Don't forget the batch file:  

\\pgcc\\cc1plus \\pgcc\\source-code.txt -o \\pgcc\\cwms.s -I
\\pgcc\\include -include \\pgcc\\fixincl.h -fms-extensions \\pgcc\\as
\\pgcc\\cwms.s -o \\pgcc\\cwmo.o \\pgcc\\ld \\pgcc\\cwmo.o -o
\\pgcc\\cwme.exe -L \\pgcc\\lib -l cpplib -l corelibc -l coredll -l
aygshell -l runtime -l portlib  
[Download the pocketgcc binaries][]

</p>
<p>
    /* 2010-03-06 john pfeiffer wince quit button*/#define WIN32_LEAN_AND_MEAN#include <windows.h>/* these three are included for pocketgcc compatibility */#include <windowsx.h>#include <commctrl.h>#include <aygshell.h>/* not only do we have those complex included Windows headersbut we have to define a special numeric ID for our buttons */#define  IDC_ExitButton      40099#define  IDC_clearScreen    40098/* HDC = handle to device context - a logical buffer of the screen. You "write" things to it and then it can write to the display in a chunk.A paint structure contains the info about the area being painted.Direct from MSDN...typedef struct tagPAINTSTRUCT {  HDC  hdc;  BOOL fErase;  RECT rcPaint;  BOOL fRestore;  BOOL fIncUpdate;  BYTE rgbReserved[32];} PAINTSTRUCT, *PPAINTSTRUCT;*/VOID APIENTRY initializeBackground(  HWND hwnd ){  HDC  hdc;    PAINTSTRUCT ps;  hdc = BeginPaint(hwnd, &ps);    /* prepares the window for painting */   EndPaint(hwnd, &ps);            /* done painting */}/* This is the prototype to the "do everything" window messageprocessing switch function */LRESULT CALLBACK MenuWndProc( HWND hwnd,   UINT message, WPARAM wParam,   LPARAM lParam); int APIENTRY WinMain(    HINSTANCE hInstance,    HINSTANCE hPrevInstance,    LPTSTR lpCmdLine, int ncmdshow ){     HWND hwnd = NULL;      HWND ExitButton = NULL;         /* each button gets a window handle */    HWND clearScreenButton = NULL;         MSG msg;       WNDCLASS wc;    RECT rc;    wc.style = CS_HREDRAW | CS_VREDRAW;             wc.lpfnWndProc = (WNDPROC)MenuWndProc;     wc.cbClsExtra = 0;    wc.cbWndExtra = 0;    wc.hInstance = hInstance;    wc.hIcon = 0;    wc.hCursor = 0;    wc.hbrBackground = (HBRUSH) GetStockObject(WHITE_BRUSH);    wc.lpszMenuName = NULL;    wc.lpszClassName = (LPTSTR) L"Menu App";      if(!  RegisterClass (&wc)){     MessageBox(NULL, TEXT("errors "),  L"IMPORTANT", MB_OK);     return 0; }/* create our main window letting windows decide the placement & size */    hwnd = CreateWindow (L"Menu App", L"quit button app", WS_VISIBLE,        CW_USEDEFAULT, CW_USEDEFAULT,        CW_USEDEFAULT, CW_USEDEFAULT,                (HWND)NULL, NULL, hInstance, (LPSTR)NULL);/* ----------- ----------- ----------- ----------- *//* here we get the coordinate dimensions of the main window */    GetWindowRect(hwnd, &rc);/* this makes a quit button at the bottom of the screen */    ExitButton = CreateWindow(       L"BUTTON", L"Quit", WS_CHILD |       WS_VISIBLE | BS_PUSHBUTTON,      0, (rc.bottom - (rc.top + (rc.right/6) )),       /* button top left corner x,y */     rc.right/6 , rc.right/6 , /* width & height */       hwnd, (HMENU)IDC_ExitButton,         hInstance, NULL);     clearScreenButton = CreateWindow(        L"BUTTON", L"Clear", WS_CHILD |      WS_VISIBLE | BS_PUSHBUTTON,      /* button top left corner x,y */     50, (rc.bottom - (rc.top + (rc.right/6) )),      /* width & height */     rc.right/6 , rc.right/6 ,        hwnd, (HMENU) IDC_clearScreen,       hInstance, NULL);     ShowWindow(hwnd, ncmdshow);  UpdateWindow(hwnd);   while(GetMessage(&msg, NULL, 0, 0))  {               TranslateMessage(&msg);                          DispatchMessage(&msg);    }       return msg.wParam;} /* end WinMain *//* ----------- ----------- ----------- ----------- */LRESULT CALLBACK MenuWndProc( HWND hwnd,  UINT message, WPARAM wParam,  LPARAM lParam ) {         /* here we test for what events happened/the user might have done */    switch (message)     {         case WM_CREATE:          initializeBackground( hwnd );   /* draw the main window */        break;              case WM_DESTROY:             PostQuitMessage(0);            break;           case WM_LBUTTONDOWN:    /* left button pressed / tap on screen */        break;     case WM_MOUSEMOVE:      /* mouse pointer is moving */            /*     if(wParam & MK_LBUTTON)*/       break;       case WM_COMMAND:                       switch(LOWORD(wParam))               {                    case IDC_ExitButton:        /* quit button pressed */                     PostQuitMessage(0);                 break;               case IDC_clearScreen:     /* clear button pressed */                 InvalidateRect( hwnd, NULL, TRUE);               break;      /* wipe the main window */               default:             break;                   }/* end case command */              break;       case WM_PAINT:           initializeBackground( hwnd );        break;              default:                  return DefWindowProc(hwnd, message, wParam, lParam);     break;          }/*  end case message */    return 0;} 

As you can see a button is just a predefined "window" object... but
hopefully I'll figure out how to design my own button infrastructure so
that I better understand the challenges, have increased portability, and
maybe even enhanced functionality! ...  

  

Further research when compiling using GCC on Windows XP gave warnings
about the "long" formatting of some text,  

  

e.g. the "L" **MessageBox(NULL, TEXT("errors "), L"IMPORTANT",
MB\_OK);**  

  

If you don't remove the "L" designation then your buttons won't appear
in your binary compiled for Windows XP...   

  
**clearScreenButton = CreateWindow( L"BUTTON", L"Clear", WS\_CHILD**  

  

Should be: clearScreenButton = CreateWindow( "BUTTON", "Clear",
WS\_CHILD  

  

If you forget to remove the L from wc.lpszClassName = (LPTSTR)
L"AppClass"; Then your program will have "undefined behavior" =)  

</p>
<p>
</div>
</div>
</div>
</p>

  [Download the pocketgcc binaries]: http://kittyandbear.net/john/c-programming-guides/pocketgcc.zip
