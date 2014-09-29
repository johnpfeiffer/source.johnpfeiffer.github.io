Title: Drupal Basic Site Configuration the Search Block
Date: 2010-02-11 21:35
Author: John Pfeiffer
Slug: drupal-basic-site-configuration-the-search-block

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
A basic Drupal theme has "regions" where you can put things...

</p>
<p>
                headerleft side                  right side           content           footer

Blocks are the "extra parts" that can appear in addition to your "node"
(stuff in the Content only)

</p>

While it is easy to get advanced functionality with a few clicks, it can
be a chore to remember the order and location of those clicks.

</p>

ENABLE SITE SEARCH

</p>

Administer -\> Site Building -\> Modules -\> List  

Click the checkbox next to SEARCH to enable it.

</p>

Hit the SAVE button (way down at the bottom).

</p>

Now you have to give Anonymous users (or just Authenticated Users, or
maybe your custom category of LOLcatz?) permission to actually see/use
the Search.  

Administer -\> User Management -\> Permissions  

Click the check boxes next to Search Module for the Anonymous and
Authenticated User columns (note you can also give access to Advanced
Search... cool.)

</p>

Hit the SAVE button (way down at the bottom).

</p>

NOTE that the "administrator/root" user isn't a column (and therefore
you can't remove your own permission to administer the site... not that
anyone'd ever be so silly...)

</p>

For Garland, specifically, when you add the Search it will make a
"double" so you have to  

disable the one that's built into the theme...  

Administer -\> Site Building -\> Themes -\> Configure -\> Global
Settings

</p>

Whew! Almost there...

</p>

Administer -\> Site Building -\> Blocks -\> List

</p>

From here you can either drag and drop (or use the "dropdown" next to
the Block name) to get the Search into the region of the page you want.

</p>

Hit the SAVE button (way down at the bottom) before doing anything else.
(Very frequently I forget to press save and all of my changes don't get
saved... must be a bug.)

</p>

THEN click on "Configure" next to the Search Block to specify some
details. (e.g. Search only appears on the page, or the title above the
Search Block will be FIND, or only show the Search Block to certain user
roles...)

</p>

OK, hit your SAVE button one last time... not only can you, super root
administrator see Search but hopefully Anonymous users can now find your
secret buried treasure...

</p>

Are you ready for URL's and page titles?

</p>
<p>
</div>
</div>
</div>
</p>

