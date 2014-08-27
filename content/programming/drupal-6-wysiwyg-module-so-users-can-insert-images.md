Title: Drupal 6 wysiwyg module so users can insert images
Date: 2010-08-26 05:00
Author: John Pfeiffer
Slug: drupal-6-wysiwyg-module-so-users-can-insert-images

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Content manager made easy = WYSIWYG (what you see is what you get)  

(screenshots coming soon!)

</p>

download and install (upload to /sites/all/modules) and enable module  

Administer -\> Site building -\> Modules

</p>

Administer -\> Site configuration -\> Wysiwyg

</p>

lists which editor modules you can use (and a helpful download link)

</p>

e.g. TinyMCE (Download) Not installed.

</p>

Extract the archive and copy its contents into a new folder in the
following location:  

sites/all/libraries/tinymce

</p>

Administer -\> Site configuration -\> Input formats  

Ensure that the "Content Manager Role" (or authenticated user?) has
access to Full HTML  

Also you can set the default format to Full HTML

</p>

(alternatively you can create a more limited input type role that
matches your paranoia)

</p>

Administer -\> Site configuration -\> Wysiwyg

</p>

Input Format = Full HTML = TinyMCE 3.8.8

</p>

Edit the profile of your WYSIWYG editor to decide which
buttons/functions are displayed.  

Up until now you only get bold and inserting images that are already
uploaded...

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - -  

IMCE (image manager) (with the WYSIWYG bridge module)

</p>

download and install (upload to /sites/all/modules) and enable module  

Administer -\> Site building -\> Modules

</p>

Administer -\> Site configuration -\> IMCE -\> User-1  

Configure any specific settings, then give a role (e.g. Content Manager)
permission

</p>

Administer -\> Site configuration -\> IMCE

</p>

\* Enable the Image button (as IMCE is accessed from the Image plugin).

</p>

\* Enable the IMCE plugin in the plugins/buttons configuration of the
wysiwyg  

profiles of your choice.

</p>

(checkbox)

</p>

Edit the profile of your WYSIWYG editor to decide which
buttons/functions are displayed.  

You MUST include the checkbox IMCE...

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - -

</p>

Ensure the future "content manager" role has create content permissions  

Administer -\> User management -\> Roles = Add Role  

Administer -\> User management -\>Permissions

</p>

Then assign that role to the user

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - -  

Finally a user with the appropriate role (e.g. "content manager" above)
can insert bold/underline/etc.  

and insert images (and upload photos using IMCE).

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Drupal][]

</div>
</p>

  [Drupal]: http://john-pfeiffer.com/category/tags/drupal
