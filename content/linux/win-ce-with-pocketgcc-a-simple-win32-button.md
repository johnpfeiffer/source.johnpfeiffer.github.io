Title: Win CE with PocketGCC a simple win32 button
Date: 2010-03-17 02:27
Author: John Pfeiffer
Slug: win-ce-with-pocketgcc-a-simple-win32-button

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Win CE uses a subset of the win32 API which is neat because technically
anything written for it can be compiled for a "full" windows as well.

</p>

Even though the Win32 API is very outdated I prefer the concept of
building blocks and getting your hands dirty with implementation -
that's how you really learn how things work. C\# and .Net, especially
with a super GUI IDE, make it easy to quickly build something but also
obscure why performance might be slow, why different parts aren't
integrating together, and really require you to build based on the
vision of the platform designers - for better or for worse.

</p>

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

/\* 2010-03-06 john pfeiffer wince quit button  

\*/

</p>

\#define WIN32\_LEAN\_AND\_MEAN  

\#include

</p>

/\* these three are included for pocketgcc compatibility \*/  

\#include  

\#include  

\#include

</p>

/\* not only do we have those complex included Windows headers  

but we have to define a special numeric ID for our buttons \*/

</p>

\#define IDC\_ExitButton 40099  

\#define IDC\_clearScreen 40098

</p>

/\* HDC = handle to device context - a logical buffer of the screen.  

You "write" things to it and then it can write to the display in a
chunk.  

A paint structure contains the info about the area being painted.

</p>

Direct from MSDN...  

typedef struct tagPAINTSTRUCT {  

HDC hdc;  

BOOL fErase;  

RECT rcPaint;  

BOOL fRestore;  

BOOL fIncUpdate;  

BYTE rgbReserved[32];  

} PAINTSTRUCT, \*PPAINTSTRUCT;

</p>

\*/

</p>

VOID APIENTRY initializeBackground( HWND hwnd )  

{ HDC hdc;  

PAINTSTRUCT ps;  

hdc = BeginPaint(hwnd, &ps); /\* prepares the window for painting \*/  

EndPaint(hwnd, &ps); /\* done painting \*/  

}

</p>

/\* This is the prototype to the "do everything" window message  

processing switch function \*/

</p>

LRESULT CALLBACK MenuWndProc(  

HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);

</p>

int APIENTRY WinMain(  

HINSTANCE hInstance,  

HINSTANCE hPrevInstance,  

LPTSTR lpCmdLine, int ncmdshow )  

{  

HWND hwnd = NULL;  

HWND ExitButton = NULL; /\* each button gets a window handle \*/  

HWND clearScreenButton = NULL;

</p>

MSG msg;  

WNDCLASS wc;  

RECT rc;

</p>

wc.style = CS\_HREDRAW | CS\_VREDRAW;  

wc.lpfnWndProc = (WNDPROC)MenuWndProc;  

wc.cbClsExtra = 0;  

wc.cbWndExtra = 0;  

wc.hInstance = hInstance;  

wc.hIcon = 0;  

wc.hCursor = 0;  

wc.hbrBackground = (HBRUSH) GetStockObject(WHITE\_BRUSH);  

wc.lpszMenuName = NULL;  

wc.lpszClassName = (LPTSTR) L"Menu App";

</p>

if(! RegisterClass (&wc))  

{ MessageBox(NULL, TEXT("errors "),  

L"IMPORTANT", MB\_OK);  

return 0;  

}

</p>

/\* create our main window letting windows decide the placement & size
\*/  

hwnd = CreateWindow (L"Menu App", L"quit button app", WS\_VISIBLE,  

CW\_USEDEFAULT, CW\_USEDEFAULT,  

CW\_USEDEFAULT, CW\_USEDEFAULT,  

(HWND)NULL, NULL, hInstance, (LPSTR)NULL);

</p>

/\* ----------- ----------- ----------- ----------- \*/  

/\* here we get the coordinate dimensions of the main window \*/  

GetWindowRect(hwnd, &rc);

</p>

/\* this makes a quit button at the bottom of the screen \*/  

ExitButton = CreateWindow(  

L"BUTTON", L"Quit", WS\_CHILD |  

WS\_VISIBLE | BS\_PUSHBUTTON,  

0, (rc.bottom - (rc.top + (rc.right/6) )),  

/\* button top left corner x,y \*/  

rc.right/6 , rc.right/6 , /\* width & height \*/  

hwnd, (HMENU)IDC\_ExitButton,  

hInstance, NULL);

</p>

clearScreenButton = CreateWindow(  

L"BUTTON", L"Clear", WS\_CHILD |  

WS\_VISIBLE | BS\_PUSHBUTTON,  

/\* button top left corner x,y \*/  

50, (rc.bottom - (rc.top + (rc.right/6) )),  

/\* width & height \*/  

rc.right/6 , rc.right/6 ,  

hwnd, (HMENU) IDC\_clearScreen,  

hInstance, NULL);

</p>

ShowWindow(hwnd, ncmdshow);  

UpdateWindow(hwnd);

</p>

while(GetMessage(&msg, NULL, 0, 0)) {  

TranslateMessage(&msg);  

DispatchMessage(&msg);  

}  

return msg.wParam;  

} /\* end WinMain \*/

</p>

/\* ----------- ----------- ----------- ----------- \*/

</p>

LRESULT CALLBACK MenuWndProc(  

HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam )  

{  

/\* here we test for what events happened/the user might have done \*/  

switch (message)  

{  

case WM\_CREATE:  

initializeBackground( hwnd ); /\* draw the main window \*/  

break;  

case WM\_DESTROY:  

PostQuitMessage(0);  

break;  

case WM\_LBUTTONDOWN: /\* left button pressed / tap on screen \*/  

break;  

case WM\_MOUSEMOVE: /\* mouse pointer is moving \*/  

/\* if(wParam & MK\_LBUTTON)\*/  

break;  

case WM\_COMMAND:  

switch(LOWORD(wParam))  

{  

case IDC\_ExitButton: /\* quit button pressed \*/  

PostQuitMessage(0);  

break;  

case IDC\_clearScreen: /\* clear button pressed \*/  

InvalidateRect( hwnd, NULL, TRUE);  

break; /\* wipe the main window \*/  

default:  

break;  

}/\* end case command \*/  

break;  

case WM\_PAINT:  

initializeBackground( hwnd );  

break;  

default:  

return DefWindowProc(hwnd, message, wParam, lParam);  

break;  

}/\* end case message \*/  

return 0;  

}

</p>

As you can see a button is just a predefined "window" object... but
hopefully I'll figure out how to design my own button infrastructure so
that I better understand the challenges, have increased portability, and
maybe even enhanced functionality! ...

</p>

Further research when compiling using GCC on Windows XP gave warnings
about the "long" formatting of some text,

</p>

e.g. the "L" MessageBox(NULL, TEXT("errors "), L"IMPORTANT", MB\_OK);

</p>

If you don't remove the "L" designation then your buttons won't appear
in your binary compiled for Windows XP...

</p>

clearScreenButton = CreateWindow( L"BUTTON", L"Clear", WS\_CHILD

</p>

Should be: clearScreenButton = CreateWindow( "BUTTON", "Clear",
WS\_CHILD

</p>

If you forget to remove the L from wc.lpszClassName = (LPTSTR)
L"AppClass"; Then your program will have "undefined behavior" =)

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

  [Download the pocketgcc binaries]: http://kittyandbear.net/john/c-programming-guides/pocketgcc.zip
  [Programming]: http://john-pfeiffer.com/category/tags/programming
