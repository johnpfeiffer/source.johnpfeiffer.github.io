Title: Is Programming Simple? Contrasting FizzBuzz Solutions: 365 programming project day forty two
Date: 2010-03-29 20:37
Tags: c, fizzbuzz, code style

[TOC]

### Simple Programming Challenge: FizzBuzz

The following is an example of a simple programming "challenge": 

    Write a program that prints the numbers from 1 to 100. 
    But for multiples of three print "Fizz" instead of the number and for the multiples of five print "Buzz". 
    For numbers which are multiples of both three and five print "FizzBuzz".
    
> Below I've thrown together a solution in less than 5 minutes, BUT, I thought to myself, experimentally, what would the code look like if I needed something more "Best Practice"...

### Quick and Dirty FizzBuzz Solution in C
    :::c
    /* 2010-03-29:1800 john pfeiffer  "simple programming" examples */
    #include <stdio.h>
    
    int main( int argc, char* argv[] ) {
        int i=0;
        for( i = 1; i <= 100; i++ ) {
            if(i % 3 == 0) {
                printf("Fizz");	
            }
            if(i % 5 == 0) {
                printf("Buzz");
            }
            if( (i % 3 != 0) && (i % 5 != 0) ) {
                printf( "%d" , i );
            }
            printf("\n");
        }
        return 0;
    } /* end main */

Imagine instead of a challenge it's a professional assignment, requiring scalability, portability, modular parts, future maintenance (by someone totally different who may not be very good at coding and/or not have a lot of time to understand the code)... 

Suddenly a simple answer transforms into the following:

### Complex "Enterprise" solution to FizzBuzz

    /* 2010-03-29 john pfeiffer  "simple programming" examples */
    
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #define BUFFERMAX 128
    
    /* prototyping of functions */
    void output( char text[ BUFFERMAX ] );
    
    void writeToBuffer( char buffer[ BUFFERMAX ], char text[ BUFFERMAX ] , int datasize );
    
    int isMultipleofThree( int i );
    
    int isMultipleofFive( int i );
    
    
    /* ------------ MAIN ------------------------------------ */
    int main( int argc, char* argv[] ) {
        int counter = 0;
        char buffer[ BUFFERMAX ];
        char temp[8];
    
        for( counter = 1; counter < 101; counter++ ) {
            /* clear the output buffer each time */
            memset( buffer, 0, sizeof(buffer) );
    
            if( isMultipleofThree( counter ) || isMultipleofFive(counter) ) {
                if( isMultipleofThree(counter) ) {
                    writeToBuffer( buffer, "Fizz", strlen("Fizz") );
                }
                if( isMultipleofFive(counter) ) {
                    writeToBuffer( buffer, "Buzz", strlen("Buzz") );
                }
            } else {
                sprintf( temp , "%d" ,counter);
                writeToBuffer( buffer , temp , strlen( temp ) );
            }
            output( buffer );
            printf("\n");
        } /* end for i=1 to 100 loop */
        return 0;
    }/* end main */
    
    
    /* ------------- FUNCTION DEFINITIONS ----------------------
    perhaps better to put all function definitions in an include file? 
    
    The modular abstraction of creating more functions allows us to swap out an existing
    implementation, e.g. if there's a faster way of determining "multiple of three"
    
    It also improves portability because most of the code would remain the same except 
    the output function writing to a win32 Device Context ... aka window
    
    Or we could quickly add functionality by calling a new "write to log" function...
    */
    
    
    /* display a string to the stdout */
    void output( char text[ BUFFERMAX ] ) {
        printf("%s",text);	
    }
    
    /* write data to the buffer */
    void writeToBuffer( char buffer[ BUFFERMAX ], char text[ BUFFERMAX ] , int datasize ) {
        int i=0;
        for( i=0;counter< datasize; i++ ) {
            buffer[i] = text[i];
        }
    }
    
    /* determine if the parameter is a multiple of three using "modulo",
    if true return 1, if false return 0 */
    int isMultipleofThree( intcounter ) {
        if( counter % 3 == 0 ) {
            return 1;   
        } else {
            return 0;
        }
    }
       
    /* determine if the parameter is a multiple of five using "modulo",
    if true return 1, if false return 0 */
    int isMultipleofFive( intcounter ) {
        if( counter % 5 == 0 ) {
            return 1;
        } else {
            return 0;
        }
    }
    
And that long convoluted giant isn't even modular enough! 

Obviously the two "isMultiple" functions could both rely on a common modulo wrapper function...

I guess at a certain point it will start looking like Java or C# ... 

Where if you want to do anything you have to look it up in the manual and change the parameters and hope the designer of the function didn't do anything buggy...

