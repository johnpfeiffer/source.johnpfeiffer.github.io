Title: 365-6 A Simple Windows Button
Date: 2010-01-20 15:01
Author: John Pfeiffer
Slug: 365-6-a-simple-windows-button

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Windows programming is a bit ugly - you have to selectively ignore the
stuff "you know". On the positive side I've figured out how to insert
code as preformatted (Drupal Input Filter -\> extending the "safe HTML")
so this should be easier to copy paste.  

Also, Notepad2 has a handy "turn tabs into spaces" that I shall start
using more often...

</p>

I've built on the previous Windows Program that put some text on the
screen so most of it should look familiar.

</p>

Remember, this was compiled with a gcc port (see earlier post for the
link to the binary)  

gcc.exe -o %1.exe %1 -Iinclude -Llib -Wall -ansi -mwindows

</p>

OK, here's the code for an exit button, some of the old comments (which
you've "learned" have been removed)...

</p>
<p>
    /* john pfeiffer basic MS windows program with button 2009-01-20 */#include <windows.h>#define  IDC_MyExitButton 40001 /* case sensitive! random high number to keep windows happy *//* This function is called by the Windows function DispatchMessage( ) */LRESULT CALLBACK WindowProcedure(    HWND hwnd,      /* Handle of window that received the msg */ UINT message,   /* The message */    WPARAM wParam,  /* Extra parameter (e.g. mouse x) */ LPARAM lParam)  /* Extra parameter (e.g. mouse y) */{    PAINTSTRUCT ps;       /* a structure for a paint job (see below */    RECT rect;           /* a structure to hold rectangle values (e.g. x,y coordinates) */    HDC hdc;            /* handle to a DC (buffer) for the screen */    switch (message)                  /* handle the messages */    {     case WM_COMMAND:         switch(LOWORD(wParam))    /* find out what's been clicked */        {            case IDC_MyExitButton:                    PostQuitMessage(0);                break;                                                default:                break;            }        break;  case WM_PAINT:       GetClientRect( hwnd, &rect );       /* get the size of our window */     hdc = BeginPaint( hwnd, &ps );      /* begin painting to the buffer */       DrawText( hdc, TEXT("Press button to quit"), -1, &rect, DT_CENTER | DT_VCENTER | DT_SINGLELINE);     EndPaint( hwnd, &ps);        return 0; case WM_DESTROY:     PostQuitMessage(0);        /* send a WM_QUIT */        break;        default:                   /* for messages that we don't deal with */ return DefWindowProc(hwnd, message, wParam, lParam);    }    return 0;}int WINAPI WinMain(  HINSTANCE hThisInstance,    /* Handle to the current instance */ HINSTANCE hPrevInstance,    /* Handle to the previous instance */    LPSTR lpszArgument,         /* pointer to command line arguments */  int ncmdshow)               /* show state of the window */{    HWND hwnd;           /* The handle for our window */    HWND ButtonPushed = NULL;    MSG messages;        /* Messages to the application  */    WNDCLASS wc;         /* Data structure for our defined windowclass */    wc.style = 0;    wc.lpfnWndProc = WindowProcedure;         /* This function is called by windows */    wc.cbClsExtra = 0;                        /* No extra bytes after the window class */    wc.cbWndExtra = 0;                        /* structure or the window instance */    wc.hInstance = hThisInstance;             /* handle to the owner */    wc.hIcon = NULL;                        /* no special application icon */    wc.hCursor = LoadCursor(NULL, IDC_ARROW); /* default cursor */    wc.hbrBackground = (HBRUSH) GetStockObject(LTGRAY_BRUSH);        wc.lpszMenuName = NULL;                /* No menu */    wc.lpszClassName = "WindowsApp";        /* the name of the windows class */            /* Register the window class, if fail quit the program with an error value */    if( RegisterClass(&wc) ==0 ){ return -1;  }    /* The class is registered, let's instantiate our window */    hwnd = CreateWindowEx( 1, "WindowsApp", "Windows Title",       WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,     NULL, NULL, hThisInstance, NULL ); /* create button and store the handle */  ButtonPushed = CreateWindow(         "button",                       /* class name */        "Push Button",               /* button caption */        WS_CHILD |WS_VISIBLE | BS_PUSHBUTTON,  /* the styles */        0,0,                            /* the left and top coordinates */        150,50,                         /* width and height */        hwnd,                           /* parent window handle */        (HMENU)IDC_MyExitButton,        /* the ID of your button */        hThisInstance,                  /* the instance of your application */        NULL) ;                         /* unnecessary extra */    ShowWindow(hwnd, ncmdshow);       /* Make the window visible on the screen */  UpdateWindow(hwnd);             /* update with changes */    /* Run the message loop. It will run until GetMessage( ) returns 0 */    while( GetMessage(&messages, NULL, 0, 0) )    {            TranslateMessage(&messages); /* Translate virtual-key messages into character messages */        DispatchMessage(&messages);  /* Send messages to WindowProcedure */    }    /* The program return-value is 0 - The value that PostQuitMessage( ) gave */    return messages.wParam;}

</div>
</div>
</div>
</p>

