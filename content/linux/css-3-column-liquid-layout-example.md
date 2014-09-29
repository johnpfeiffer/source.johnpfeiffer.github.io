Title: CSS 3 column liquid layout example
Date: 2010-08-15 14:14
Author: John Pfeiffer
Slug: css-3-column-liquid-layout-example

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
CSS is much better than HTML, but making a webpage look the way it ought
to look can be very painful, frustrating, and time consuming.

</p>

Not only do you have to create cross browser compatible code, but it has
to look nice when you're done!

</p>

This is just a basic example that you can experiment with and add to
later, there are some comments but the code is mostly self explanatory:

</p>
<p>
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"><head><style type="text/css">/* required to kill off any extra "helpful" browser padding  */html, body {  margin: 0;   padding: 0;  height: 99%;} #container{    min-height: 100%;    height: 100%;    margin:0;     border: 1px solid green;}#column1 {    float: left;         width: 33%;  height: 100%;           /* full length column */ position: relative;   border: 1px solid red;}#column2 {  float: left;    /* wraps the div around the left of the prev object */   width: 34%;  height: 100%;    position: relative;   border: 1px solid yellow;}#column3 {   float: right;    width: 33%;  margin-left: -1%;   /* prevent the right column from being pushed down! */   height: 100%;    position: relative;   border: 1px solid blue;  overflow: hidden;}</style></head><body> <div id="container">        <div id="column1">         left left left left left left left left left left left left      </div>     <div id="column2">             center center center     </div>         <div id="column3">         right right right right right right right right right        </div></div><!-- end div container --></body></html>

</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Programming][]

</div>
</p>

  [Programming]: http://john-pfeiffer.com/category/tags/programming
