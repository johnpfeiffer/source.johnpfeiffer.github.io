Title: How to center with CSS: 365 programming project day thirty seven
Date: 2010-02-17 15:05

This is a tiny post, but it covers a very important part of how a CSS layout might look: how do you center something?

The "Centering CSS Blocks Trick" forces the text (or image too, hopefully, depending on a post 2006 browser)...

### CSS center (horizontal)

#### CSS
    :::css
    #footer {
        text-align: center;
        bottom: 0px;
        margin-left: auto;
        margin-right: auto;
        width: 30%;
        z-index: 0;
        position: relative;
    }

#### HTML

    :::html
    <div id="footer">footer text goes here<div>

Note that the text-align instruction is perhaps redundant but it's better to be safe (and more universally compatible).

### CSS centering vertically

To VERTICALLY CENTER things takes a bit of creativity,  basically you must pretend that an "inner div" is actually a table cell and use the "new" property of vertical-align (alot like html table cell valign)...

    :::html
    <html><head>
    <style type="text/css">
        #contentsContainer {
            /* height must be a fixed number */
            height: 200px;
            width: 100%;
            
            border: 1px solid green;
            text-align: center;
            
            display: table-cell;
            vertical-align: middle;
            
            position: relative;
        }
        
        #contents{
            border: 1px solid blue;
            /* height must be a fixed number */
            height:40px;
            position:relative;
        }
    </style>
    </head><body>
    	<div id="contentsContainer">
    		CONTENTS Lots of contents Vertically and horizontally centered CONTENTS
    		<div id="contents">
    			test more content (this is horizontally centered too)
    		</div>
    	</div>
    </body></html>
    


### Inline CSS centered
    :::html
    <div style="text-align: center; width: 100%; margin-left: auto; margin-right: auto;">
        <img alt="Logo" src="/img/icons/logo_256.png">
        <h2>Welcome</h2>
    </div>


Whew, back to work!
