Title: Windows programming in WinCE on an HP IPAQ: 365 programming project day twenty one
Date: 2010-01-21 13:26
Tags: win ce, win32, gcc, pocketgcc

As the number of portable computers (we might call them mobile phones or smart phones or pda's etc.) explodes they need software. 

One thing Microsoft got right is that Windows CE, the stripped down version of Windows for Mobile Devices, uses most of the same basic programming platform/language as "normal" desktop windows programming. 

The following is a very interesting learning experience I've had (and a useful way to pass otherwise idle waiting time in the "Tube") programming Windows Applications in WinCE.

### A Compiler for WinCE: pocketgcc

The first thing you need is a WinCE compiler - my choice was pocketgcc (even though it hasn't been updated since 2003), because a port of GCC to WinCE means a stable tool that I already know (sorta) how to use. 

<http://pocketgcc.sourceforge.net/>

The next hurdle after downloading and copying them onto my device (HP Ipaq) and double tapping (clicking) to install them was to use the CMD to cd \pgcc

Then I used a text editor (either Word or pocketnotepad) to create a batch file (yes, technically I suppose a batch file is a program too!) with the following cryptic lines... 

    \pgcc\cc1plus \pgcc\source-code.txt -o \pgcc\cwms.s -I \pgcc\include 
     -include \pgcc\fixincl.h -fms-extensions \pgcc\as \pgcc\cwms.s 
     -o \pgcc\cwmo.o \pgcc\ld \pgcc\cwmo.o -o \pgcc\cwme.exe -L \pgcc\lib 
     -l cpplib -l corelibc -l coredll -l aygshell -l runtime -l portlib

- The cc1plus.exe (compiler?) outputs the assembly code file but also includes the "fixincl.h" file and uses the -fms-extensions option (no, I haven't actually yet learned exactly why). 
- The as.exe program turns the assembly into object code. 
- Finally the loader turns the object code into an executable with the appropriate libraries. 

The following source code should look very familiar to my earlier Windows Programming examples.

I've added comments here that are not in my "production" IPAQ environment source code because the screen is too small with lots of scrolling already...


    :::c
    #define WIN32_LEAN_AND_MEAN
    #include <windows.h>
    #include <windowsx.h>
    #include <commctrl.h>
    #include <aygshell.h>
    #define  IDC_ExitButton	40099
    /* the IDC object requires a number, I just give them high unused ones */
    
    /* the above includes are a bit of a mystery to me but the program
    doesn't work without them and I figure they must be specific to WinCE */
    
    /* instead of function stubs, main, then function declarations I do them
    all before main() ... but of course I have to remember to always declare
    before using... so do as I say: always declare functions (and then remember
    to update them and the stub), not as I do... */
    
    VOID APIENTRY HandlePaint(  HWND hwnd  )
    {
        HDC hdc;			/* handle to device context */
        PAINTSTRUCT ps;		
        RECT rc;			/* rectangle structure */
        TCHAR tszOut[] = TEXT("hello!");
    
        hdc = BeginPaint(hwnd, &ps);
    
        GetClientRect (hwnd, (LPRECT)&rc);
    	
        /* the cryptic stuff below outputs a text string in a rectangle */
        DrawText (hdc,
            tszOut,
            _tcslen(tszOut),
            (LPRECT)&rc,
            DT_VCENTER | DT_CENTER | DT_SINGLELINE);
        EndPaint(hwnd, &ps);
    }
    
    /* below is the most important function after main() where the "large windows 
    switch" figures out what the user has done and responds */
    
    LRESULT CALLBACK MenuWndProc( HWND hwnd, UINT message, 
    	WPARAM wParam, LPARAM lParam )  /* w & l param's are extra data like x,y */
    {  
        switch (message)			  
        {   
            case WM_COMMAND:		 	/* there's a command from the user */
                switch(LOWORD(wParam))		/* to find out what command */
                {   case IDC_ExitButton:	/* the user pressed the button */   
                        PostQuitMessage(0);
                        break;
                    default:
                        break;		  
                }	  
                break;  
            case WM_DESTROY: 
                PostQuitMessage(0);	/* closes the program */
                break;   
            case WM_PAINT:
                HandlePaint(hwnd);	/* calls a "modular" drawing function */
                break;	  
    
            default:	  
                return DefWindowProc(hwnd, message, wParam, lParam);
                break;
        }
        return 0;
    }
    
        
    int APIENTRY WinMain( HINSTANCE hInstance, HINSTANCE hPrevInstance,
    	LPTSTR lpCmdLine, int ncmdshow )
    {
        HWND hwnd = NULL;
        HWND ExitButton= NULL;  	/* a handle to our button "window" */
        MSG msg;   
        WNDCLASS wc;
        HMENU hMenu;
    
        wc.style = CS_HREDRAW | CS_VREDRAW; 
        wc.lpfnWndProc = (WNDPROC)MenuWndProc; 
        wc.cbClsExtra = 0;
        wc.cbWndExtra = 0;
        wc.hInstance = hInstance;
        wc.hIcon = 0;
        wc.hCursor = 0;
        wc.hbrBackground = (HBRUSH) GetStockObject(WHITE_BRUSH);
        wc.lpszMenuName = NULL;
        wc.lpszClassName = (LPTSTR) L"Menu App";  
        /* WinCE seems to require strings cast as LONG? */
        	
        if(! RegisterClass (&wc))
        {
            MessageBox(NULL, TEXT("errors "), L"IMPORTANT", MB_OK);
            return 0;
        }
       
        /* the size and placement of our program window */
        hwnd = CreateWindow (L"Menu App", L"2nd prog hello", 
            WS_VISIBLE, 0, 30, 200, 150,
            (HWND)NULL, NULL, hInstance, (LPSTR)NULL);
    
        /* the size and placement of our button child of hwnd "window" */
        ExitButton = CreateWindow( 
            L"BUTTON", L"quit", WS_CHILD | 
            WS_VISIBLE | BS_PUSHBUTTON, 
            0, 30,100,100, hwnd, (HMENU)IDC_ExitButton, 
            hInstance, NULL);
    
        ShowWindow(hwnd, ncmdshow);
        UpdateWindow(hwnd);
    
        while(GetMessage(&msg, NULL, 0, 0))
        {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }
        	return msg.wParam;
    	
    } /* end WinMain */
    
