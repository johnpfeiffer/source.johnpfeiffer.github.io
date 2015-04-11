Title: C programming command line clock continued (winclockv2): 365 programming project day thirty one
Date: 2010-02-01 14:15
Tags: c, time, clock

Slowly working towards the final product, indeed I do see that I have a working executable at every stage (even if the steps are small and the tests are numerous)...

(The looping part does not quite work yet...)

    :::c
    /* 
    2010-01-31 john pfeiffer, MS windows clock
    
    PROGRAM DESIGN
    	MS window with X, quit button, and current system time displayed
    	Hour:minute:second  (hh:mm:ss)
    
    HIGH LEVEL FUNCTIONS	
    	
    	update current time
    	see if user clicked button
    		quit if button clicked
    
    	display current time on window
    
    
    ORGANIC ITERATIVE BUILDS
    	1. build a program to show current time (in c/dos) then exits immediately
    		*TEST: should show correct system time 
    		each time user presses enter show new current time (ctrl+c to exit)
    		TEST: should show correct system time on each click
    
    	2. build a windows "quit button app" (can reuse previous work)
    		TEST: program should quit cleanly
    
    	3. windows with current time (once) and quit button
    		TEST: program should show correct system time and when button clicked quit
    
    	4. windows with current time constantly updating and quit button
    		(will the processor be overloaded while waiting?  need semaphores?)
    */
    
    
    
    #include <stdio.h>
    #include <time.h>
    #include <string.h>
    
    /*	
    	stdio.h is for displaying output to command line
    	time.h is for time()
    	string.h is to help format any strings created
    */
    
    /* returns a string with the current time */
    void get_current_time( char current_time[] );
    
    void display_time( char current_time[] );
    
    void clear_current_time( char current_time[] );
    
    int main(int argc, char* argv[])
    {
        	char c = 'n';
        	char current_time[128];
        
        /* show that the string has garbage that is cleaned out */
        	printf("\nDISPLAY current time variable (initial garbage)\n");
        	display_time( current_time );
        	
        /*
        	Loop depending on the user to continue updating
        */
        	do{	
        	
        		printf("\nEMPTY current time variable.\n");
        		clear_current_time( current_time );
        		
        		printf("\nDISPLAY current time variable:\n");
        		display_time( current_time );
        
        		printf("\nUPDATE current time variable.\n");
        		get_current_time( current_time );
        
        		/* DEBUGGING
        		printf("%s\n", current_time);
        		*/
        
        		printf("\nDISPLAY current time variable:\n");
        		display_time( current_time );
        
        	
        		c = 'n';	/* ensure that the user must force a continuance */
        		printf("\nPRESS y to update the current time variable again:\n");
        		c = getchar();
        	
        	}while( c == 'y' );
        
        	return 0;
    }/* end main */
    
    /* begin function definitions */
    
    /* Get the current time from the system and update the time string */
    void get_current_time( char current_time[128] )
    {
        	time_t tempTime;
        
        	/* initialize the variable, otherwise only returns 1970 date */
        	tempTime = time(NULL);
        
        	/* DEBUGGING
        	printf("%s\n", asctime(localtime(&tempTime)));
        	*/
        	strcpy(current_time, asctime(localtime(&tempTime)));
        
        	/* DEBUGGING
        	printf("%s\n", current_time);
        	*/
    }
    
    /* output the current time string ... to the command line */
    void display_time( char current_time[128] )
    {
        	printf("CURRENT TIME: %s\n",current_time);
    }
    
    void clear_current_time( char current_time[128] )
    {
        	memset( current_time, 0, sizeof(current_time));
    }
    
To Be Continued...
