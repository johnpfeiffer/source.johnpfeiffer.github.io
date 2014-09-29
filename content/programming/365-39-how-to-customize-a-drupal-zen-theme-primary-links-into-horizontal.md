Title: 365-39 How to customize a Drupal Zen theme Primary Links into Horizontal
Date: 2010-02-23 20:52
Author: John Pfeiffer
Slug: 365-39-how-to-customize-a-drupal-zen-theme-primary-links-into-horizontal

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
I'm squeezing my brain to get Drupal theme customization and CSS working
as quickly as possible (while working a more than full time job and
doing some things besides computers every once in a while)...

</p>

"Creating" a Zen sub theme is relatively easy, mostly a lot of copying,
replacing STARTERKIT, and uploading again to a different directory...

</p>

[http://kittyandbear.net/john/web-tutorials/drupal-how-to-create-a-zen-su...][]

</p>

But to make significant changes in the layout you have to modify
layout.css

</p>

Before that! FIRST MODIFY THE SETTINGS THAT ARE GIVEN VIA THE WEB ADMIN
e.g. Theme configuration

</p>

http:// test.com /admin/build/themes/settings/  

Here you can choose whether to display the "Theme" Primary Links
(appears just below the header section)...  

(I think it's best to uncheck it and use Blocks instead...)

</p>

[http://test.com/admin/build/block][]  

Block layouts is where you can put the Primary links up at the top and
Secondary links at the bottom.

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -  

NEXT, IT'S BEST TO INSTALL THE FIREFOX "FIREBUG" PLUGIN  

which allows you to "peek" at the html & css source and figure out
exactly what code controls what...  
[http://getfirebug.com/downloads][]

</p>

Tools -\> AddOns -\> disable when you're not working on a website CSS  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - -  

THEN YOU CAN BEGIN MODIFYING layout.css

</p>

\1. LOOK AT THE SOURCE CODE FROM YOUR UNMODIFIED SITE (with Firebug
too...)

</p>

e.g. line 37 of the home page

</p>

WE FIND "menu-primary" in zen.css

</p>

To "override" the default zen.css all we have to do is create our own
version in layout.css

</p>

\#block-menu-primary-links /\* "Primary links" block \*/  

{  

font-size: 16px;  

}

</p>

To take advantage of the "nested" control principle, so any links in div
"block-menu-primary-links"  

will now be red, we add the following to layout.css (with comments
explaining it too, of course!)

</p>

\#block-menu-primary-links a:link  

{ color: green; }

</p>

\#block-menu-primary-links a:visited  

{ color: red; }

</p>

TRY UPLOADING layout.css and forcing your browser to refresh... neat!

</p>

SOME ADDITIONAL EXAMPLES (finally the horizontal menu!)

</p>

\#block-menu-primary-links /\* "Primary links" block \*/  

{ margin: 0; padding: 0;  

}

</p>

/\* this means by default ordered and unordered lists and anchors have
no underlines \*/  

\#block-menu-primary-links li ul,  

\#block-menu-primary-links li,  

\#block-menu-primary-links a {  

text-decoration: none;  

}

</p>

/\* specifically "anchors" or links will appear as blocks \*/  

\#block-menu-primary-links a {  

display: block;

</p>

}

</p>

\#block-menu-primary-links a:links { color: \#008000; }  

\#block-menu-primary-links a:visited { color: \#CCBA22; }

</p>

Unfortunately haven't figured out why the drupal menu width, when set,
makes them appear to go down instead of widening to the right...
material for a future post I suppose...

</p>

Scratch that, 30 frantic minutes later, a solution has arrived...

</p>
<p>
    /* FORCING THEM TO BE HORIZONTAL? 2010-02-22 JOHNPFEIFFER  */#block-menu-primary-links /* overriding the zen.css "Primary links" block */{     margin: 0;         /* remove any previously defined margins or padding */   padding: 0;}/* this means by default ordered and unordered lists and anchors have no underlines */#block-menu-primary-links li ul,#block-menu-primary-links li,#block-menu-primary-links a {   text-decoration: none;  /* no underlining links */   list-style-type: none;  /* no bullet points */   list-style-image: none; /* no custom bullet images */    text-align: center; /* I prefer my text to be neat and centered */} /* specifically "anchors" or links will horizontal */#block-menu-primary-links a {    display: block; /*inline;  /* blocks force a newline but inline just uses a little width */  width: 70px;    /* wide enough for the longest element, unless you want words on two lines */} #block-menu-primary-links a:links {         color: #008000;     }   /* light blue */#block-menu-primary-links a:visited {        color: #CCBA22;     }   /* light brown */#block-menu-primary-links li { float: left; position: relative; }

</div>
</div>
</div>
</p>

  [http://kittyandbear.net/john/web-tutorials/drupal-how-to-create-a-zen-su...]:
    http://kittyandbear.net/john/web-tutorials/drupal-how-to-create-a-zen-subtheme-part-one.txt
  [http://test.com/admin/build/block]: http://test.com/admin/build/block
  [http://getfirebug.com/downloads]: http://getfirebug.com/downloads
