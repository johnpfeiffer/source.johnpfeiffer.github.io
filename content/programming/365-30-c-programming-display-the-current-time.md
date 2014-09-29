Title: 365-30 C programming display the current time
Date: 2010-01-31 21:39
Author: John Pfeiffer
Slug: 365-30-c-programming-display-the-current-time

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
I am trying to follow best practice as I've learned from the Mythical
Man Month (Fred Brooks), the Cathedral and the Bazaar's (Eric
Raymond)...

</p>

C programming seems natural to me but I always want to stretch myself a
little bit so here's a "C Clock" program that will eventually evolve
into a "Windows Clock" program.

</p>

So here is a modular design, released early with plenty of comments,
debugging ability, and grown locally and organically:

</p>
<p>
    /* 2010-01-31 john pfeiffer, MS windows clockPROGRAM DESIGN  MS window with X, quit button, and current system time displayed Hour:minute:second  (hh:mm:ss)HIGH LEVEL FUNCTIONS get current time display current time on window   update current time  see if user clicked button       quit if button clickedORGANIC ITERATIVE BUILDS  1.  build a program to show current time (in c/dos) then exits immediately       TEST: should show correct system time        each time user presses enter show new current time (ctrl+c to exit)      TEST: should show correct system time on each click   2. build a windows "quit button app" (can reuse previous work)       TEST: program should quit cleanly 3. windows with current time (once) and quit button      TEST: program should show correct system time and when button clicked quit    4. windows with current time constantly updating and quit button     (will the processor be overloaded while waiting?  need semaphores?)*/#include <stdio.h>#include <time.h>#include <string.h>/*   stdio.h is for displaying output to command line time.h is for time() string.h is to help format any strings created*//* returns a string with the current time */void get_current_time( char current_time[] );void display_time( char current_time[] );void clear_current_time( char current_time[] );int main(int argc, char* argv[]){  char current_time[128];/* show that the string has garbage that is cleaned out */  printf("Current Time variable garbage:\n");  display_time( current_time );     clear_current_time( current_time );  printf("\nCurrent Time variable is EMPTY:\n");   display_time( current_time ); printf("\nCurrent Time variable is FULL:\n");    get_current_time( current_time ); return 0;}/* end main *//* begin function definitions */void get_current_time( char current_time[128] ){  time_t tempTime;  /* initialize the variable, otherwise only returns 1970 date */  tempTime = time(NULL);    printf("%s\n", asctime(localtime(&tempTime)));}void display_time( char current_time[128] ){  printf("CURRENT TIME: %s\n",current_time);}void clear_current_time( char current_time[128] ){    memset( current_time, 0, sizeof(current_time));}

If you're unable or unwilling to copy and paste the above and compile it
yourself I suppose you can try the binary:

</p>

[http://kittyandbear.net/john/blog-prog/winclockv1.c.zip][]

</p>

Of course this isn't a finished product - but its a solid foundation
that outlines what the next few posts will be about...

</p>
<p>
</div>
</div>
</div>
</p>

  [http://kittyandbear.net/john/blog-prog/winclockv1.c.zip]: http://kittyandbear.net/john/blog-prog/winclockv1.c.zip
