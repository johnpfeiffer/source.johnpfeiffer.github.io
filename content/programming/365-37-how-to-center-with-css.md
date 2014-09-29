Title: 365-37 How to center with CSS
Date: 2010-02-17 15:05
Author: John Pfeiffer
Slug: 365-37-how-to-center-with-css

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
This is a tiny post, but it covers a very important part of how a CSS
layout might look: how do you center something?

</p>

The "Centering CSS Blocks Trick" forces the text (or image too,
hopefully, depending on a post 2006 browser)...

</p>

THE CSS  

\#footer {

</p>

text-align: center;  

bottom: 0px;  

margin-left: auto;  

margin-right: auto;  

width: 30%;  

z-index: 0;  

position: relative;  

}

</p>

THE HTML

</p>

footer text goes here

</p>

Note that the text-align instruction is perhaps redundant but it's
better to be safe (and more universally compatible).

</p>

To VERTICALLY CENTER things takes a bit of creativity,  

basically you must pretend that an "inner div" is actually a table cell
and use the "new" property of vertical-align (alot like html table cell
valign)...

</p>

\#contentsContainer {

</p>

/\* height must be a fixed number \*/  

height: 200px;  

width: 100%;

</p>

border: 1px solid green;  

text-align: center;

</p>

display: table-cell;  

vertical-align: middle;

</p>

position: relative;

</p>

}

</p>

\#contents{  

border: 1px solid blue;  

/\* height must be a fixed number \*/  

height:40px;  

position:relative;  

}

</p>

CONTENTS Lots of contents Vertically and horizontally centered CONTENTS

</p>

test more content

</p>

Whew, back to work!

</p>
<p>
</div>
</div>
</div>
</p>

