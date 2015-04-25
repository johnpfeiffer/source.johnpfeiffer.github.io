Title: Windows CE Programming - writing text to the display: 365 programming project day forty one
Date: 2010-03-21 09:44
Tags: windows, win ce

[TOC]

### Building a program properly requires a lot of discipline

1. define goals (what functionality will be achieved?) 
2. write up a high level flow/state chart 
3. create modular parts from the flow chart (e.g.functions) 
4. create tests - e.g. know what input goes in and what should come out 
5. fill in the functions with dummy information (e.g. always return constants) 
6. integrate and ensure that your "demo" version achieves your goal 

*Note that all of this ignores the tools to be used, estimating time and cost, scheduling, etc.*

BUT you could just as easily use the above for your "Life Plan for Success"... 

### Real life example of "programming" for success

1. Goal: I want to play professional soccer 
    - find the position I am best at
    - go to at least 3 tryouts
2. Flow: `fitness -> skills -> recognition`
3. Modular Parts:
    - physical fitness
    - skills
    - networking and agent 
    - tryout special training camps + video of playing 
    - feedback from experts on my best position
4. Tests: 
    - Must run 5km in under 18 minutes.
    - Must sprint 40 yards in 5 seconds.
    - Must be able to shoot the ball from 30 yards out into top quarter of the goal 10 out of
10 times
    - Agent must have history of signing players to contracts
    - Tryouts must show a history of players being brought into the team
5. Sample Info:
    - run 5km in 16 minutes
    - sprint in 4.7 seconds
    - 10 for 10 on shooting
    - signed a contract with an agency who manages 100's of professional players
    - scheduled 3 tryouts where players have been signed onto the first team every year
6. Integration: 

    If I attend a special training camp and give some professional coaches tapes of me playing in different positions I will receive suggestions on what is my best position (and possibly tips on
how to improve at that position).

Based on total "dummy" information + extra edge from sub goal (networking + expert advice)...

YES, very high probability of success. 

### Plan for a Successful Win CE Program

Whew, let's get back to some programming! 

1. Goal: to put text on the screen 
2. Flow: `WinMain -> get the text -> draw the screen -> draw the text`
3. Modular: 
    - drawtext function 
    - char to wchar function 
4. Tested: 
    - program ran with just quit button
    - drawing text to the screen direct from Main using a wchar L"string" constant string 
    - drawing text to the screen from Main using a wchar[] array populated by a wsprintf 
    - moving the above to a function and calling it from main 
    - passing a char string to the conversion function and printing the resulting wchar string 
5. the "dummy" info was the use of constant wchar L"string" but I also printed the sizeof and strlen and wcstrlen numbers I defined some sub functions so that I could use the char string functions instead of constantly referring to the Windows functions... 

I'd hoped it would be more portable but that's something I discuss at the end... Anyways, 

### Win CE code for writing text to the display

    :::c
    /* 2010-01 john pfeiffer writing text to the display */
    
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>
    #include <windowsx.h>
    #include <commctrl.h>
    #include <aygshell.h>
    #define IDC_ExitButton 40099 
    
    /* wchar[] must be cleared empty first! */ 
    void stringToWchar( char string[128], wchar_t longstring[128] ) {
        int i=0;
        for( i=0; i < strlen( string ); i++) {
            longstring[i] = (WCHAR)string[i]; 
        } 
    } 
    
    /* convert a char string to wchar and Display it on the screen */ 
    
    /* here we take the handle to device context (aka logical buffer about the 
    screen and begin painting it - we then draw a single line of text (windows 
    wide character format but first converting the character string to wchar string)...
    The end paint matches the begin paint and without them the text will flicker constantly */

    VOID APIENTRY drawText( HWND hwnd, char text[128], int x, int y ) {
        HDC hdc;
        PAINTSTRUCT ps;
        wchar_t outputtext [128];
        hdc = BeginPaint(hwnd, &ps);
        hdc = GetDC(hwnd);
        /* good practice to zero things before using them */
        memset( outputtext , 0, sizeof( outputtext ));
        stringToWchar( text, outputtext );
        ExtTextOut( hdc, x, y, NULL, NULL, outputtext , _tcslen(outputtext ), NULL);
        ReleaseDC(hwnd, hdc);
        EndPaint(hwnd, &ps);
    }
    
    VOID APIENTRY initializeBackground( HWND hwnd ) {
        HDC hdc;
        PAINTSTRUCT ps;
        hdc = BeginPaint(hwnd, &ps);
        EndPaint(hwnd, &ps);
    }
    
    /* our big message loop with all sorts of interrupt options */

    LRESULT CALLBACK MenuWndProc( HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) {
        switch (message) {
            case WM_LBUTTONDOWN:
                break;
            case WM_CHAR:
                break;
            case WM_KEYDOWN:
                break;
            case WM_COMMAND:
                switch(LOWORD( wParam )) {
                    case IDC_ExitButton:
                        PostQuitMessage(0);
                        break;
                    default:
                        break;
                }
                break;
            case WM_DESTROY:
                PostQuitMessage(0);
                break;
            case WM_PAINT:
                drawText( hwnd, "press quit button to quit", 40, 40 );
                break;
            case WM_CREATE:
                initializeBackground( hwnd );
                break;
            default:
                return DefWindowProc( hwnd, message, wParam, lParam );
                break;
            }
        return 0;
    } /* end function MenuWndProc */
    
    int APIENTRY WinMain( HINSTANCE hInstance, HINSTANCE hPrevInstance, LPTSTR lpCmdLine, int ncmdshow ) {
        HWND hwnd = NULL;
        HWND ExitButton= NULL;
        MSG msg;
        WNDCLASS wc;
        wc.style = CS_HREDRAW | CS_VREDRAW;
        wc.lpfnWndProc = (WNDPROC)MenuWndProc;
        wc.cbClsExtra = 0;
        wc.cbWndExtra = 0;
        wc.hInstance = hInstance;
        wc.hIcon = 0;
        wc.hCursor = 0;
        wc.hbrBackground = (HBRUSH)GetStockObject(WHITE_BRUSH);
        wc.lpszMenuName = NULL;
        wc.lpszClassName = (LPTSTR) L"App";
        if(! RegisterClass (&wc)) {
            MessageBox(NULL, TEXT("errors "), L"IMPORTANT", MB_OK);
            return 0;
        }
    
        /* Make sure the window uses the Menu App Class name defined above! */
        hwnd = CreateWindow (L"App", L"menu demo", WS_VISIBLE, CW_USEDEFAULT,
            CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, (HWND)NULL, NULL,
            hInstance, (LPSTR)NULL); 
            
        /* -------- -------- -------- -------- */
    
        ExitButton = CreateWindow( L"BUTTON", L"quit", 
            WS_CHILD | WS_VISIBLE | BS_PUSHBUTTON,
            0, 0, 30, 30, hwnd, (HMENU)IDC_ExitButton, hInstance, NULL); 
        ShowWindow(hwnd, ncmdshow);
        UpdateWindow(hwnd);
    
        while(GetMessage(&msg, NULL, 0, 0)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        } 
        return msg.wParam;
    } /* end WinMain */


### Convert to a Desktop Application

As always I try to give as much info as possible, therefore to convert this to a Windows Desktop application you must change the following: 

`Line 32: _tcslen( outputtext ), NULL);`

changed to: 

`wcslen( outputtext ), NULL);`

All of the explicit conversions to "Long" that are necessary for Win CE (16 bit) have to be removed... 

which just means getting rid of those pesky 'L' s 

wc.lpszClassName = (LPTSTR) L"App"; 

For this to really work in Windows Desktop you'd have to replace my custom char to wchar string conversion with Microsoft's MultiByteToWideChar OR...

you would probably prefer using wsprintf() to write any text to a wchar_t string and then ExtTextOut is very happy...

