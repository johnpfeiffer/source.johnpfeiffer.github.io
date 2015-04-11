Title: PHP User Input HTML Sanitization and Math: 365 programming project day twenty five
Date: 2010-01-25 22:08
Tags: php, security, htmlentities, input sanitization

HTML forms are quick way to get user data but PHP requires a PHP server. 

Luckily I have one and together it's quite easy to create a page that gets some info from a user and then does some calculations (in this case nothing fancy).

I've done a little more User Input Sanitization than usual - basically the rule is: "If you'll display it, clean up the HTML output, if you'll send it to a linux script, strip the slashes, and if you send it to a database, clean up any MySQL stuff"...


    :::php
    <html> <head> </head>
    <body>
    <?php
    if( !isset($_POST['startx']) || empty($_POST['startx']) || !isset($_POST['starty']) || empty($_POST['starty']) || !isset($_POST['endx']) || empty($_POST['endx']) || !isset($_POST['endy']) || empty($_POST['endy']) 
      )
    {
        	print '<form action="' . $_SERVER['PHP_SELF'] . '" method="post">';
        	print "\n<br \>"; 
        	print 'Starting X Point<input name="startx" type="text">';
        	print "\n<br \>"; 
        	print 'Starting Y Point<input name="starty" type="text">';
        	print "\n<br \>"; 
        	print 'End X Point<input name="endx" type="text">';
        	print "\n<br \>"; 
        	print 'End Y Point<input name="endy" type="text">';
        	print "\n<br \>"; 
        	print '<input type="submit" /></form>';
        	print "\n<br \>"; 
    }
    else{
        	$startx = (int) htmlentities( $_POST['startx'] );
        	$starty = (int) htmlentities( $_POST['starty'] );
        	$endx = (int) htmlentities( $_POST['endx'] );
        	$endy = (int) htmlentities( $_POST['endy'] );
        	print "\n<br />";
        	print $startx . "," . $starty . "  " . $endx . "," . $endy;
        	print "\n<br />";
        	print "width: " . ($endx - $startx); 
        	print "\n<br />";
        	print "height: " . ($endy - $starty); 
        	print "\n<br />";
        	print "acos(startx): " . acos($startx); 
        	print "\n<br />";
    	} //end of if-else user filled in textarea
    ?>
    
    </body></html>
    

Further reference about how easy it is to manipulate user numbers: <http://php.net/manual/en/book.math.php>