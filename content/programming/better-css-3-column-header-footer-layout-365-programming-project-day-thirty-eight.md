Title: A better CSS 3 column header footer layout: 365 programming project day thirty eight
Date: 2010-02-18 14:57
Tags: css, html

It's messy as some of the code could be removed but it gets you most of the way there - a footer at the bottom (even if the content doesn't fill the page)... 

a header at the top that's full width, and 3 columns... with a little weird bug on the right column...


    :::html
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en">
    <head>
    <style type="text/css">
    
    /* required to kill off any extra "helpful" browser padding */
    html, body {
    	margin: 0;
    	padding: 0;
    	height: 99%;
    } 
    
    #header {
    	height: 60px;	
    	overflow: hidden;
    	z-index: 0;	
    	border: 1px solid purple;
    	text-align: center;
    }
    
    
    #container1
    {
    	min-height: 100%;
    	height: auto;
    	height: 100%;
    	overflow: hidden;
    	margin:0;	
    	position: relative;
    	border: 1px solid green;
    }
    
    #container2
    {
    	border: 1px solid green;
    	position: relative;
    }
    
    #container3
    {
    	position: relative;
    }
    
    
    #column1 {
    	float: left;
    	width: 20%;
    	overflow: hidden;
    	border: 1px solid red;
    	position: relative;
    }
    
    
    #column2 {
    	float: none;
    	width: 60%;
    	overflow: hidden;
    	border: 1px solid blue;
    	position: relative;
    }
    
    #column3 {
    	float: right;
    	width: 20%;
    	overflow: hidden;
    	border: 1px solid blue;
    	position: relative;	
    }
    
    
    #footer {
    	height: 60px;	
    	overflow: hidden;
    	z-index: 0;	
    	border: 1px solid purple;
    	text-align: center;
    	bottom: 0;
    	width: 99%;
    	position: absolute;
    }
    
    </style>
    
    </head>
    <body>
    
    
    <div id="container1">
    	<div id="header">
    		header
    	</div>
            <div id="column1">
                	left left left left left left left left left left left left
            </div>
            <div id="column2">
                	standard 3 column layout with header and footer
                	content and columns are ordered by SEO priority				
            </div>	
            <div id="column3">
                	right right right right right right right right right
                	<img src="image.png">
            </div>
            </div>
    <div id="footer">
    	footer
    </div>
    
    
    <!--div id="container1">
    	<div id="container2">
    		<div id="c3">
    	</div>
    </div-->
    </body>
    </html> 
    