Title: 365-22 VBScript Windows Shell Script (Programming) For Loop
Date: 2010-01-22 21:56
Author: John Pfeiffer
Slug: 365-22-vbscript-windows-shell-script-programming-for-loop

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Programming obviously requires logic and discipline. Less well known but
just as important, it also requires creativity and elasticity.

</p>

Windows Script programming has a significantly different syntax (rules
of how the code must be written to be valid) than the previous Linux
Script, C Programming, HTML, or CSS. How many people do you know who
speak multiple languages, much less create functional artificial
constructs with them?

<!--break-->

You can copy and paste the text below into an empty notepad and save it
as test.vbs

*A .vbs file can be dangerous as it is executing commands on your
computer but in this case there are no surprises as you can see all of
the commands explained in the comments.*

-------------------------------------------------------

<p>
    REM John Pfeiffer's windows vbscript 2010-01-22REM In Visual Basic Script a REM stands for "remark", which is a comment REM (something ignored by the computer)REM we must declare what variables we want but without saying what typeREM in this case we've used the good practice of naming the variablesREM as they're intended to be used: i = programming standard for counting,REM astring is a string of characters (though in a real program it would be REM better named "username" or "address_street") and array is a list of items.dim i, astring, arrayREM assigning a literal piece of text to a string variable is really easyastring = "this,should,be,interesting,csv," REM built in functions do most of the hard work - like splitting up a stringREM into an array of strings based on a "splitting character"array = split(astring, ",")REM wscript.echo displays message boxes, REM the & symbol concatenates strings and variables to display togetherwscript.echo astring & " BECOMES => " & array(4) & array(3) & array(2) & array(1) & array(0)REM The for loop counts from the first (lbound) element to the uppermost this REM "object oriented" technique of a method/function to access the attributes REM (in this case size/bounds) of a variable, rather than predefined symbol or number,REM prevents a careless programmer error or an unforseen change from crashingREM the program by accessing (or writing!) outside of the defined variable spaceREM Lines between the "for" and "next" are executed as many times as the for loopREM iteratesfor i = lbound(array) to ubound(array)   wscript.echo array(i)nextREM the "for each" is a special case of a for loop which will do something for REM every item in the array - better than the above for this specific exampleREM as it is easier to read and understand what it is doing (with even lessREM chance of an error)  for each i in array    wscript.echo inextREM REMEMBER, 50-80% of your time will be spent debugging, recompiling, REM fixing, updating!  More important than getting it right the first timeREM is making it easy to figure out where/why it went wrongwscript.echo "the end"

</div>
</div>
</div>
</p>

