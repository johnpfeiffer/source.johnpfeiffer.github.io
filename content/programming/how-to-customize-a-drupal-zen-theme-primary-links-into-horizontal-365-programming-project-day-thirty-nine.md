Title: How to customize a Drupal Zen theme Primary Links into Horizontal: 365 programming project day thirty nine
Date: 2010-02-23 20:52
Tags: drupal, drupal theme, zen theme

[TOC]

I'm squeezing my brain to get Drupal theme customization and CSS working as quickly as possible (while working a more than a full time job and doing something besides computers every once in a while)...

"Creating" a Zen sub theme is relatively easy, mostly a lot of copying, replacing STARTERKIT, and uploading again to a different directory...


### Web Admin configs

But to make significant changes in the layout you have to modify **layout.css**

Before that! FIRST MODIFY THE SETTINGS THAT ARE GIVEN VIA THE WEB ADMIN e.g. Theme configuration

**http://example.com/admin/build/themes/settings/**

Here you can choose whether to display the "Theme" Primary Links (appears just below the header section)...  

*(I think it's best to uncheck it and use Blocks instead...)*

**http://example.com/admin/build/block**

> Block layouts is where you can put the Primary links up at the top and Secondary links at the bottom.

### Firefox Firebug Plugin

Allows you to "peek" at the html and css source and figure out exactly what code controls what...  
<http://getfirebug.com>

**Tools -> AddOns -> disable**
> when you're not working on a website CSS  

### Modifying layout.css

LOOK AT THE SOURCE CODE FROM YOUR UNMODIFIED SITE (with Firebug too...) e.g. line 37 of the home page

WE FIND "menu-primary" in **zen.css**

To "override" the default **zen.css** all we have to do is create our own version in **layout.css**

    :::css
    #block-menu-primary-links /* "Primary links" block */
    {
        font-size: 16px;
    }
    
To take advantage of the "nested" control principle, so any links in div "block-menu-primary-links" will now be red, we add the following to **layout.css** (with comments explaining it too, of course!)

    :::css
    #block-menu-primary-links a:link {
        color: green;	
    }
    
    #block-menu-primary-links a:visited {
        color: red;	
    }
    
TRY UPLOADING **layout.css** and forcing your browser to refresh... neat!


### Horizontal menu in layout.css

SOME ADDITIONAL EXAMPLES (finally the horizontal menu!)

    :::css
    /* "Primary links" block */
    #block-menu-primary-links {
        margin: 0; padding: 0;
    }
    
    /* this means by default ordered and unordered lists and anchors have no underlines */
    #block-menu-primary-links li ul,
    #block-menu-primary-links li,
    #block-menu-primary-links a {
        text-decoration: none;
    }
    
    /* specifically "anchors" or links will appear as blocks */
    #block-menu-primary-links a {
        display: block;
    }
    
    #block-menu-primary-links a:links {
        color: #008000;	
    }
    #block-menu-primary-links a:visited {
        color: #CCBA22;	
    }
    

Unfortunately haven't figured out why the drupal menu width, when set, makes them appear to go down instead of widening to the right... material for a future post I suppose...

Scratch that, 30 frantic minutes later, a solution has arrived...

### Horizontal menu in layout.css with the width workaround

    :::css
    /* FORCING THEM TO BE HORIZONTAL? 2010-02-22 JOHNPFEIFFER	*/
    
    #block-menu-primary-links /* overriding the zen.css "Primary links" block */
    {
        margin: 0; 		/* remove any previously defined margins or padding */
        padding: 0;
    }
    
    /* this means by default ordered and unordered lists and anchors have no underlines */
    #block-menu-primary-links li ul,
    #block-menu-primary-links li,
    #block-menu-primary-links a { 
        text-decoration: none;	/* no underlining links */
        list-style-type: none;	/* no bullet points */
        list-style-image: none; /* no custom bullet images */
        text-align: center; /* I prefer my text to be neat and centered */
    }
    
    /* specifically "anchors" or links will horizontal */
    #block-menu-primary-links a { 
        display: block; /*inline;  /* blocks force a newline but inline just uses a little width */
        width: 70px;	/* wide enough for the longest element, unless you want words on two lines */
    }
    
    #block-menu-primary-links a:links { 		color: #008000;	 	} 	/* light blue */
    #block-menu-primary-links a:visited { 		color: #CCBA22;	 	}   /* light brown */
    #block-menu-primary-links li { float: left; position: relative; }
    
    
### How to create a zen subtheme (part one)

*Note - you should only create custom themes in a test environment, leave your production website alone until you've got everything working!*

1.	Download the newest version: <http://drupal.org/project/zen>
2.  Extract the files into a directory (e.g. `tar -xzvf zen-6.x-1.1.tar.gz` or winzip and extract)
3.	Upload the files using FTP (or better yet, SFTP) into the **/drupal-root/sites/all/themes**
4.	Upload the STARTERKIT directory that's inside your zen-6.x-1.1 folder from your pc into the **/drupal-root/sites/all/themes**
5.	Rename both the pc version and online STARTERKIT directory to your_subtheme_name (lowercase and underscores only)
6.	Inside both the pc version and the online STARTERKIT directory, rename the **STARTERKIT.info.txt** to **your_subtheme_name.info**
7.	On your pc, open the your_subtheme_name.info file and find and replace every "STARTERKIT" with "your_subtheme_name"
8.	inside **your_subtheme_name.info** find the following lines:

    ; The name and description of the theme used on the admin/build/themes page.
    name        = Zen Sub-theme Starter Kit
    
	> Replace the "zen Sub-theme Starter Kit" with your_subtheme_name

9. Repeat step 7 for the "template.php" file
10. Repeate step 7 for the "theme-settings.php" file
11.	Upload all 3 modified files (overwrite) to your **/drupal-root/sites/all/themes/your_subtheme_name** directory

12. Using your FTP download the following files from: 		

	**/drupal-root/sites/all/themes/zen-6.x-1.1/zen/zen**
	
	**html-elements.css, layout-fixed.css, layout-liquid.css, print.css, zen.css**

13. Upload all of the above files into your directory: **/drupal-root/sites/all/themes/your_subtheme_name**

    12a. If you want a fixed (ie 1024px) css layout then rename **layout-fixed.css** to **layout.css**
    
	12b. If you want a resizable css layout then rename **layout-liquid.css** to **layout.css**
	
14.	As the Drupal administrator login to your site and enable your new sub theme: **Administer -> Site building -> Themes**
	
**http://example.com/admin/build/themes/select**

> you'll probably want to set it as default


Apparently Drupal 6 is smart enough that when you click save:

For easier theme development, the theme registry is being rebuilt on every page request. 
It is extremely important to turn off this feature on production websites.
	
### More info

You may have to:

run cron manually (or you should be) so that the new options appear on the Drupal Menus.

Reload after you save the new theme as enabled and default
