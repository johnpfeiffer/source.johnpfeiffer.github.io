Title: Drupal Themes customization intro: 365 programming project day thirty four
Date: 2010-02-10 15:02
Tags: drupal, drupal theme, css

Drupal is meant to be a dynamic website platform (that runs quite well out of the box) yet customizable.

Despite the good advice to create a "sub theme" by copying and pasting the current files into a new folder i went ahead and hacked at the core php and css...

While Garland itself (I'm using the "configurable sub theme Minelli" which must be modified through Garland) is very hard to work with (I will probably end up using Zen to get my final customized effect)...

FTP into your website hosting and ... /drupal-root/themes/garland

Modifying page.tpl.php with my trusty notepad2...

Line 66 has the very interesting terms:

From there you have to also modify "style.css" to the related terms (that's the way css works, to abstract the content & functionality in html/php and the design in css)...

FUNNILY ENOUGH, THINGS WORK BACKWARDS...

    :::css
    body.sidebars {
        /* min-width: 980px; */
        min-width: 680px;
    }
    
So as you can see, I cleverly commented out the original and modified it to be smaller (right?)... but it actually made the sidebars bigger... so I'll try the reverse... but changes don't really appear...

**Admin -> Flush All Caches is supposed to help make the theme changes appear!**

After enough fiddling to understand it I've reset style.css to it's default in Garland...

Apparently the "Minnelli" sub folder minnelli.css overrides the style.css so that's what I need to work on...

**/drupal-root/themes/garland/minnelli/minnelli.css**

    :::css
    body #wrapper #container {
        /* width: 560px; */
        width: 960px;
    }
    
    body.sidebars #wrapper #container {
        /* width: 980px; */
        width: 480px;
    }
    
    body.sidebar-left #wrapper #container,
    body.sidebar-right #wrapper #container {
        /* width: 770px; */
        width: 570px;
    }

Except that once again, the settings above have SHRUNK the body...

    :::css
    body.sidebar-left #wrapper #container,
    body.sidebar-right #wrapper #container {
        /* width: 770px; */
        width: 870px;
    }
    
    
The above is the only bit of code needed to widen the body slightly, all of the rest is the garland/minnelli default.

Ironically the changes only appear so far in the Admin User logged on screen (not for anonymous users)...

But that's enough for today's post!

More info:

- <https://www.drupal.org/theme-guide/6-7>
- <https://www.drupal.org/node/225125>


</p>
<p>
</div>
</div>
</div>
</p>

  [http://www.themeswiki.org/Customizing\_Drupal\_6\_Themes]: http://www.themeswiki.org/Customizing_Drupal_6_Themes
