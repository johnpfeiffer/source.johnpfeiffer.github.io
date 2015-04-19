Title: C programming windows clock v4 (failure is only feedback): 365 programming project day thirty six
Date: 2010-02-12 14:47
Tags: c, windows, time,  clock

It seems I've bitten off more than I thought with regularly updating a Window every second...

I need to go back and learn more about how **WM_PAINT** works in windows because my current version is very funky... though it does work!

A couple of obvious other things: **WM_TIMER** and perhaps **strcpy** instead of **get_current_time** again...

The reason I've chosen the awkward system of getting the system time over and over instead of the "convenient" windows timer is that I'm trying to learn and understand what I can do with programming, not how to copy and paste someone else's function.

The "modular" aspect of **get_current_time** returning a string becomes very interesting as theoretically I could modify it to get time from an atomic clock or the internet and the application wouldn't know the difference.

Anyways, here's some source code that does compile (but I think it has a very slow memory leak so don't leave it running all night... LOL)


    :::c
    /* 2010-02-12  john pfeiffer, MS windows clock v4 (updating time)
    todo: wm_paint, wm_timer, strcpy instead of get_current?
    */
    
    #include <stdlib.h>
    #include <stdio.h>
    #include <time.h>
    #include <string.h>
    
    #include <windows.h>
    #define  IDC_ExitButton 40001 
    
    
    LRESULT CALLBACK WindowProcedure( HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam);
    
    void get_current_time( char current_time[128] );
    
    int WINAPI WinMain( HINSTANCE hThisInstance, HINSTANCE hPrevInstance, LPSTR lpszArgument, 	int ncmdshow)
    {
        char current_time[128];
        char temp_time[128];
    
        HWND hwnd;           /* The handle for our window */
        HWND ButtonPushed = NULL;
    
        MSG messages;        /* Messages to the application  */
        WNDCLASS wc;         /* Data structure for our defined windowclass */
    
        wc.style = 0;
        wc.lpfnWndProc = WindowProcedure;   /* This function is called by windows */
        wc.cbClsExtra = 0;                   /* No extra bytes after the window class */
        wc.cbWndExtra = 0;                   /* structure or the window instance */
        wc.hInstance = hThisInstance;		 /* handle to the owner */
        wc.hIcon = NULL;					 /* no special application icon */
        wc.hCursor = LoadCursor(NULL, IDC_ARROW); /* default cursor */
        wc.hbrBackground = (HBRUSH) GetStockObject(LTGRAY_BRUSH);	
        wc.lpszMenuName = NULL; 				  /* No menu */
        wc.lpszClassName = "WindowsApp";		  /* the name of the windows class */
        
        
        /* Register the window class, if fail quit the program with an error value */
        if( RegisterClass(&wc) ==0 )
        {
            return -1;	
        }
    
        /* The class is registered, let's instantiate our window */
        hwnd = CreateWindowEx( 1, "WindowsApp", "Windows Title", WS_OVERLAPPEDWINDOW,
                CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT, CW_USEDEFAULT,
                NULL, NULL, hThisInstance, NULL );
    
        /* create button and store the handle */
        ButtonPushed = CreateWindow( 
            "button",      					/* class name */
            "Push to Quit",  				/* button caption */
            WS_CHILD |WS_VISIBLE | BS_PUSHBUTTON,  /* the styles */
            0,0,                            /* the left and top coordinates */
            150,50,                         /* width and height */
            hwnd,                           /* parent window handle */
            (HMENU)IDC_ExitButton,        /* the ID of your button */
            hThisInstance,                  /* the instance of your application */
            NULL) ;                         /* unnecessary extra */
    
        ShowWindow(hwnd, ncmdshow);		/* Make the window visible on the screen */
        UpdateWindow(hwnd);				/* update with changes */
    	
        get_current_time( temp_time );	 /* get the current time initially */
    
        /* Run the message loop. It will run until GetMessage( ) returns 0 */
        while( GetMessage(&messages, NULL, 0, 0) )
        {
            /* nasty polling business, should be done with WM_TIMER */
            /* if strings aren't the same then update the window */
            get_current_time( current_time );
    
            if( strcmp(current_time, temp_time) )
            {   
                /* debugging - am I getting the time comparison? */
                MessageBox(hwnd, current_time, temp_time, 0);
    
                /* theoretically the rest of this forces the window to refresh */
                UpdateWindow(hwnd);
    			
                ShowWindow(hwnd, ncmdshow);
                /* update the new "old time" */
                get_current_time( temp_time );				 
            }
    
            TranslateMessage(&messages); 
            DispatchMessage(&messages);	 
        }
            
        /* The program return-value is 0 - The value that PostQuitMessage( ) gave */
        return messages.wParam;
    }
    
    
    /* This function is called by the Windows function DispatchMessage( ) */
    LRESULT CALLBACK WindowProcedure( HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam)
    {
        char current_time[128];
        PAINTSTRUCT ps;		/* a structure for a paint job (see below */
        RECT rect;	   /* a struct to hold rectangle values (e.g. x,y coordinates) */
        HDC hdc;			/* handle to a DC (buffer) for the screen */
    
        switch(message)                  /* handle the messages */
        {
            case WM_COMMAND:
                switch(LOWORD(wParam))    /* find out what's been clicked */
                {
                    case IDC_ExitButton:
                        PostQuitMessage(0);
                        break;                                
    
                    default:
                        break;
                }
                break;
    
            case WM_PAINT:
                GetClientRect( hwnd, &rect );		/* get the size of our window */
                InvalidateRect ( hwnd, NULL, TRUE );
                hdc = BeginPaint( hwnd, &ps );		/* begin painting to the buffer */
    
                get_current_time( current_time );
                DrawText( hdc, TEXT(current_time), -1, &rect, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
                EndPaint( hwnd, &ps);
                return 0;    
            case WM_DESTROY:
                PostQuitMessage(0);       
                break;
    
            default:                   /* for messages that we don't deal with */
                return DefWindowProc(hwnd, message, wParam, lParam);
        }
        return 0;
    }/* end of WinMain */
    
    
    /* Get the current time from the system and update the time string */
    void get_current_time( char current_time[128] )
    {
        time_t tempTime;
        /* initialize the variable, otherwise only returns 1970 date */
        tempTime = time(NULL);	
        strcpy(current_time, asctime(localtime(&tempTime)));
    }
