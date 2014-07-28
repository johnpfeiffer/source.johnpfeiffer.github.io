Title: 365-3 PHP is mad cool with CSS
Date: 2010-01-17 22:02
Author: John Pfeiffer
Slug: 365-3-php-is-mad-cool-with-css

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
PHP is similar to C which makes it easy for me to do interesting things.
The php manual webpage is brilliant! Don't you wish everybody had a full
public API, easy menus, working examples, searchable and with the best
user comments that really flesh out the bugs?

</p>

CSS is so much better than HTML tables - it really revolutionizes the
simplicity, maintainability, and power of displaying things on the web.

</p>

Put them together and you have miracles like Drupal.

</p>

The following project took a little more time than usual and it might
even be useful one day, but I what I really like about it is that it's
FUN...

</p>

< html\> < head\> < /head\>  

< body\>  

This page takes a list of objects, one object per page, and displays
them in a list using css.  

< br /\> < br /\>  

Please fill in the box below:  

< br /\> < br /\>  

< ?php  

//The POST variable is an array with each form item as an item in the
index  

//if the object list variable is not filled out then we ask the user to
fill it in

</p>

/\* Clicking the submit button does the form action: the same page again
with the POST data the ' quotations will ignore the " quotations which
is useful when outputing HTML but sometimes very hard to read (or debug,
along with spaces between HTML options) the " quotations allow the \\n
newline to be output to the HTML code spacing  

\*/  

print '< form action="' . $\_SERVER['PHP\_SELF'] . '" method="post"\>';  

print "\\n"; //making extra spacing obvious improves readability and
debugging  

print '< textarea name="objectlist" cols="40" rows="20"\>';

</p>

if( !isset($\_POST['objectlist']) || empty($\_POST['objectlist'] ) )  

{  

print "\\n < /textarea\>< br /\>";  

print "\\n";  

print '< input type="submit" /\>< /form\>';  

print "< br /\>";

</p>

/\* The else allows the user to see what they typed in last time BUT for
security no slashes! \*/  

}  

else{  

print stripslashes($\_POST['objectlist']);  

print "< /textarea\>< br /\>";  

print '< input type="submit" /\>< /form\>';  

print "< br /\>";

</p>

$object\_list = $\_POST['objectlist']; //one string for all of the user
entered items  

$object\_lines = explode("\\n", $object\_list); //break the string into
lines

</p>

print\_r($object\_lines); //dump the array for debugging

</p>

print "< br /\> < br /\>";

</p>

/\* the for loop takes each item in the array and copies it into the
$value variable and it assigns the index to the $key variable. rtrim()
removes the newline the user entered in the form.  

\*/  

foreach( $object\_lines as $key=\>$value)  

{  

print '< div style="position: absolute; left: ' . (40+$key) . '%; top: '
. ($key+2) . 'em;"\>'; print $value;  

print "< /div\>\\n";  

}

</p>

} //end of if-else user filled in textarea  

?\>

</p>

< /body\>  

< /html\>

</p>

[http://kittyandbear.net/john/web-tutorials/php-list-to-diagram.php][]  

I apologize about the poor formatting of the above source code, I'll see
if I can find a nicer way to enter into the Blog or break it up into
"this is how you do" sections...

</p>

Many thanks to my debugger Bobby!

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Programming][]

</div>
</p>

  [http://kittyandbear.net/john/web-tutorials/php-list-to-diagram.php]: http://kittyandbear.net/john/web-tutorials/php-list-to-diagram.php
  [Programming]: http://john-pfeiffer.com/category/tags/programming
