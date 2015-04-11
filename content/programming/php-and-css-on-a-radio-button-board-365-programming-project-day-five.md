Title: PHP and CSS on a radio button board: 365 programming project day five
Date: 2010-01-19 22:28
Tags: php, css, code structure

[TOC]

### Overview

I'm a little sick so this one took longer than it should have. Futher exploration of the theme of PHP + CSS + HTML as a very simple way to get user input and then do something fun with it.

The beginnings of trying to "modularize" code into functions earlier in the process (in later, more complex programs it is a necessity).

You may be asking, "How is this useful?" but I think it's a popular misconception that Programs should be useful...

I will try to break the code into chunks (that you will have to re-assemble) but with better piece by piece explanation:


### Defining CSS Style in the Head

Best practice is to have many php or html pages linked to a single CSS
definition file so that a single update is more efficient. Efficiency in this case means all of the code in one easily visible file.

The CSS here removes the anchor (hyperlink) underline and makes it black BUT if hovered the text will turn red.  

    :::html
    <html><head>  
    
    <style type="text/css">  

    <!-- removing text decoration removes the underlines -->  

    #chosen a{  
        text-decoration:none;  
        color:black;  
    }  

    #chosen a:hover{  
        text-decoration:none;     
        color: red;
    }  

    </style></head>


### Body of PHP functions

If you have an HTML head then you should have a body. The majority of the body is the definition of a custom function called "display_board".

Again I'm using the trick that if the user has entered data (and therefore something's in the $_POST) then we get to show the user that we've done something fun with what they gave us.

PHP functions are easy to define and have the usual parameters and return value responsibilities (though parameters don't need any typing which allows the programmer to focus on the concepts, not the implementation - hopefully not confusing the variables up in the process).

Much like a CSS you can have a file with the definitions of your php functions and include it somewhere with **include("footer.php");**

On one hand you remove the implementation details which can make prototyping and modularization faster and easier, on the other hand you have to search through/open a number of different files (or even include definitions to functions you don't use) and of course, it's great to ignore the implentation details right until something goes wrong.

### function display_board

    :::php
    <body>Click on one square, then submit, then hover your choice!<br /> <br />
    
    <?php
        function display_board($chosen_square) {
        print '<form action="' . $_SERVER['PHP_SELF'] . '" method="post">';
        print "\n";  //newline character in the HTML code for readability
        print '<div id="chosen" align="center"\>';  
        print "\n";


I don't think the indentations show up well in the blog but the nested loops and formula are just a fancy way of counting from 1 to 64 with 8 items per line.  

The magic "redefined css anchor" is buried in there if the user has chosen a square.  

### nested for loops

    :::php
    for($x=0; $x<8; $x++)
    {
        for($y=0; $y<8; $y++)  
        {  
            if( ((8*$x) + $y+1) == $chosen_square )
            {  
                print '<input type="radio" name="board_square" value="';
                print ((8*$x) + $y+1) . '">';
                print '<a href="#"> ';
                print ((8*$x) + $y+1);
                print "</a>\n";
                //the nested for loops formula creates 64 consecutive values  
            } else {
                print '<input type="radio" name="board_square" value="';
                print ((8*$x) + $y+1) . '"> ' . ((8*$x) + $y+1) . "\n";
            }
        }
        print "<br \>\n";
    }
    print '</div><input type="submit" value="Press Me" /></form>';


### user input

stripslashes is best practice when dealing with user data though I'm not sure how a $_POST of a radio button value could end up as a root command; better safe than sorry.

The ever present "if the $_POST variable is set AND the $chosen_square variable is NOT EMPTY" allows to only print something that exists (instead of foolishly printing non-existent stuff).

Finally we call our function (with a parameter). So if the CSS and PHP function definition were other files this "program" would be very compact and very easy to read (but then again you wouldn't know what the program did unless you had those other files).  

    :::php
    $chosen_square = stripslashes( $_POST['board_square'] );
    if( !empty( $chosen_square ) && isset( $chosen_square ) )
    {
        print $chosen_square;
    }

    display_board( $chosen_square );  
    ?>

    </body>
    </html>

</p>