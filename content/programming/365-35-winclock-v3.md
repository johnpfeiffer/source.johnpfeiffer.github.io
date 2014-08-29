Title: 365-35 WinClock v3
Date: 2010-02-11 13:42
Author: John Pfeiffer
Slug: 365-35-winclock-v3

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
My windows clock is slowly progressing...

</p>

Now I can create a window with a QUIT button and display the current
system time (only once)...

</p>

If you want to know more about the project from the beginning search the
site for winclock (or click on the time.h tag).

</p>

I've stripped out most of the project header stuff - perhaps in the
future I'll just have it as an "include" so that it's in the project but
since it doesn't change much I only have to look at it when I refer back
to it (instead of at the top of the file ALL THE TIME!)

</p>

Ok, enough planning and review, here's the code:

</p>

gcwin.bat  

gcc.exe -o %1.exe %1 -Iinclude -Llib -Wall -ansi -mwindows

</p>

winclock-v3.c

</p>
<p>
    /* 2010-02-08  john pfeiffer, MS windows clock v3 (the windows)*/#include <time.h>#include <string.h>#include <windows.h>#define  IDC_MyExitButton 40001 /* case sensitive! random high number to keep windows happy */LRESULT CALLBACK WindowProcedure( HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);void get_current_time( char current_time[128] );int WINAPI WinMain( HINSTANCE hThisInstance, HINSTANCE hPrevInstance, LPSTR lpszArgument,            int ncmdshow)               {    HWND hwnd;           /* The handle for our window */    HWND ButtonPushed = NULL;    MSG messages;        /* Messages to the application  */    WNDCLASS wc;         /* Data structure for our defined windowclass */    wc.style = 0;    wc.lpfnWndProc = WindowProcedure;   /* This function is called by windows */    wc.cbClsExtra = 0;                   /* No extra bytes after the window class */    wc.cbWndExtra = 0;                   /* structure or the window instance */    wc.hInstance = hThisInstance;       /* handle to the owner */    wc.hIcon = NULL;                    /* no special application icon */    wc.hCursor = LoadCursor(NULL, IDC_ARROW); /* default cursor */    wc.hbrBackground = (HBRUSH) GetStockObject(LTGRAY_BRUSH);     wc.lpszMenuName = NULL;                /* No menu */    wc.lpszClassName = "WindowsApp";        /* the name of the windows class */            /* Register the window class, if fail quit the program with an error value */    if( RegisterClass(&wc) ==0 ){ return -1;  }    /* The class is registered, let's instantiate our window */    hwnd = CreateWindowEx( 1, "WindowsApp", "Windows Title",       WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,     NULL, NULL, hThisInstance, NULL ); /* create button and store the handle */  ButtonPushed = CreateWindow(         "button",                       /* class name */        "Push to Quit",                  /* button caption */        WS_CHILD |WS_VISIBLE | BS_PUSHBUTTON,  /* the styles */        0,0,                            /* the left and top coordinates */        150,50,                         /* width and height */        hwnd,                           /* parent window handle */        (HMENU)IDC_MyExitButton,        /* the ID of your button */        hThisInstance,                  /* the instance of your application */        NULL) ;                         /* unnecessary extra */    ShowWindow(hwnd, ncmdshow);       /* Make the window visible on the screen */  UpdateWindow(hwnd);             /* update with changes */    /* Run the message loop. It will run until GetMessage( ) returns 0 */    while( GetMessage(&messages, NULL, 0, 0) )    {                TranslateMessage(&messages);         DispatchMessage(&messages);      }    /* The program return-value is 0 - The value that PostQuitMessage( ) gave */    return messages.wParam;}/* This function is called by the Windows function DispatchMessage( ) */LRESULT CALLBACK WindowProcedure( HWND hwnd, UINT message,  WPARAM wParam, LPARAM lParam){    char current_time[128];    PAINTSTRUCT ps;       /* a structure for a paint job (see below */    RECT rect;      /* a struct to hold rectangle values (e.g. x,y coordinates) */    HDC hdc;            /* handle to a DC (buffer) for the screen */    switch (message)                  /* handle the messages */    {     case WM_COMMAND:         switch(LOWORD(wParam))    /* find out what's been clicked */        {            case IDC_MyExitButton:                    PostQuitMessage(0);                break;                                                default:                break;            }        break;  case WM_PAINT:       GetClientRect( hwnd, &rect );       /* get the size of our window */     hdc = BeginPaint( hwnd, &ps );      /* begin painting to the buffer */        get_current_time( current_time );     DrawText( hdc, TEXT(current_time), -1, &rect, DT_CENTER | DT_VCENTER | DT_SINGLELINE);              EndPaint( hwnd, &ps);        return 0; case WM_DESTROY:     PostQuitMessage(0);        /* send a WM_QUIT */        break;        default:                   /* for messages that we don't deal with */ return DefWindowProc(hwnd, message, wParam, lParam);    }    return 0;}/* Get the current time from the system and update the time string */void get_current_time( char current_time[128] ){  time_t tempTime;/* initialize the variable, otherwise only returns 1970 date */   tempTime = time(NULL);   strcpy(current_time, asctime(localtime(&tempTime)));}

For the binary executable (and the source code as .c file)  
[http://kittyandbear.net/john/blog-prog/winclock-v3.zip][]

</p>
<p>
</div>
</div>
</div>
</p>

  [http://kittyandbear.net/john/blog-prog/winclock-v3.zip]: http://kittyandbear.net/john/blog-prog/winclock-v3.zip
