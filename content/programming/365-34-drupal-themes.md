Title: 365-34 Drupal Themes
Date: 2010-02-10 15:02
Author: John Pfeiffer
Slug: 365-34-drupal-themes

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Drupal is meant to be a dynamic website platform (that runs quite well
out of the box) yet customizable.

</p>

Despite the good advice to create a "sub theme" by copying and pasting
the current files into a new folder i went ahead and hacked at the core
php and css...

</p>

While Garland itself (I'm using the "configurable sub theme Minelli"
which must be modified through Garland) is very hard to work with (I
will probably end up using Zen to get my final customized effect)...

</p>

FTP into your website hosting and ... /drupal-root/themes/garland

</p>

Modifying page.tpl.php with my trusty notepad2...

</p>

Line 66 has the very interesting terms:

</p>

From there you have to also modify "style.css" to the related terms
(that's the way css works, to abstract the content & functionality in
html/php and the design in css)...

</p>

FUNNILY ENOUGH, THINGS WORK BACKWARDS...

</p>

body.sidebars {  

/\* min-width: 980px; \*/  

min-width: 680px;  

}

</p>

So as you can see, I cleverly commented out the original and modified it
to be smaller (right?)... but it actually made the sidebars bigger... so
I'll try the reverse... but changes don't really appear...

</p>

<strong>  

Admin -\> Flush All Caches is supposed to help make the theme changes
appear!  
</strong>

</p>

After enough fiddling to understand it I've reset style.css to it's
default in Garland...

</p>

Apparently the "Minnelli" sub folder minnelli.css overrides the
style.css so that's what I need to work on...

</p>

/drupal-root/themes/garland/minnelli/minnelli.css

</p>

body \#wrapper \#container {  

/\* width: 560px; \*/  

width: 960px;  

}

</p>

body.sidebars \#wrapper \#container {  

/\* width: 980px; \*/  

width: 480px;  

}

</p>

body.sidebar-left \#wrapper \#container,  

body.sidebar-right \#wrapper \#container {  

/\* width: 770px; \*/  

width: 570px;  

}

</p>

Except that once again, the settings above have SHRUNK the body...

</p>

body.sidebar-left \#wrapper \#container,  

body.sidebar-right \#wrapper \#container {  

/\* width: 770px; \*/  

width: 870px;  

}

</p>

The above is the only bit of code needed to widen the body slightly, all
of the rest is the garland/minnelli default.

</p>

Ironically the changes only appear so far in the Admin User logged on
screen (not for anonymous users)...

</p>

But that's enough for today's post!

</p>

An excellent resource:  
[http://www.themeswiki.org/Customizing\_Drupal\_6\_Themes][]

</p>
<p>
</div>
</div>
</div>
</p>

  [http://www.themeswiki.org/Customizing\_Drupal\_6\_Themes]: http://www.themeswiki.org/Customizing_Drupal_6_Themes
