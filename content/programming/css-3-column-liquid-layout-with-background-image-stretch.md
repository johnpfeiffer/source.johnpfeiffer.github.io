Title: CSS 3 column liquid layout with background image stretch
Date: 2010-05-15 14:30
Tags: css, html

[TOC]

CSS keeps improving but sometimes it takes some creativity to meet what might seem like obvious demands: a background image stretched in a column

The following example gives two different methods of background image stretching, though I admit that the background image is just a color gradient and that this kind of stretching on a graphical image (in a liquid layout) could appear at best, "funny".

I created a color gradient and then resized it to be 640x2 pixels, otherwise all of the code is below:

### 3 column liquid layout with background image stretch code

    :::html
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
    <head><style type="text/css">
    
    /* required to kill off any extra "helpful" browser padding  */
    html, body {
        margin: 0;
        padding: 0;
        height: 99%;
    } 
    
    #container
    {
        min-height: 100%;	
        height: 100%;
        margin:0;	
        border: 1px solid green;
    }
    #column1 {
        float: left; 		
        width: 20%;	
        height: 100%;			/* full length column */
        position: relative;
    
        border: 1px solid red;
        /* bg-body-left is a 640 wide by 2 pixel tall image color gradient */
        background-image: url('bg-body-left.png');
        background-repeat: repeat-y;
    }
    #column2 {
        float: left;	/* wraps the div around the left of the prev object */
        width: 60%;	
        height: 100%;
        position: relative;
        border: 1px solid yellow;
    }
    #column3 {
        float: right;
        width: 20%;
        margin-left: -1%;	/* prevent the right column from being pushed down! */
        height: 100%;
        position: relative;	
        border: 1px solid blue;
        overflow: hidden;
    }
    /* a class is defined below called stretch to force an image to stretch */
    .stretch {       
        width:100%;
        height:100%;
    }
    </style>
    </head>
    <body>
    	<div id="container">
    		<div id="column1">
    			left left left left left left left left left left left left
    		</div>
    		<div id="column2">
    				center center center
    		</div>	
    		<div id="column3">
    right right right right right right right right right
    		<img src="bg-body-left.png" class="stretch" alt="" />
    		</div>
    </div><!-- end div container -->
    </body></html>


Please leave a comment if you've appreciated this or any other posts on my site! Thanks! -John

### 3 column liquid layout with background image stretch example

<div class="field field-name-body field-type-text-with-summary field-label-hidden">

<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
<head><style type="text/css">

/* required to kill off any extra "helpful" browser padding  */
html, body {
    margin: 0;
    padding: 0;
    height: 99%;
}

#container
{
    min-height: 100%;   
    height: 100%;
    margin:0;   
    border: 1px solid green;
}
#column1 {
    float: left;        
    width: 20%; 
    height: 100%;           /* full length column */
    position: relative;

    border: 1px solid red;
    /* bg-body-left is a 640 wide by 2 pixel tall image color gradient */
    background-image: url('bg-body-left.png');
    background-repeat: repeat-y;
}
#column2 {
    float: left;    /* wraps the div around the left of the prev object */
    width: 60%; 
    height: 100%;
    position: relative;
    border: 1px solid yellow;
}
#column3 {
    float: right;
    width: 20%;
    margin-left: -1%;   /* prevent the right column from being pushed down! */
    height: 100%;
    position: relative; 
    border: 1px solid blue;
    overflow: hidden;
}
/* a class is defined below called stretch to force an image to stretch */
.stretch {       
    width:100%;
    height:100%;
}
</style>
</head>
<body>
    <div id="container">

        <div id="column1">
            left left left left left left left left left left left left
        </div>
        <div id="column2">
                center center center
        </div>  
        <div id="column3">
right right right right right right right right right
        <img src="bg-body-left.png" class="stretch" alt="" />

        </div>
</div><!-- end div container -->
</body>
</html>
</div>