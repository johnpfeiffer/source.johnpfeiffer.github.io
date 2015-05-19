Title: Drupal 6 wysiwyg module so users can insert images
Date: 2010-08-26 05:00
Tags: drupal, wysiwyg

[TOC]

Content manager made easy = WYSIWYG (what you see is what you get) (for Drupal 6)

- <https://www.drupal.org/project/wysiwyg>

### Download and install the Drupal 6 WYSIWYG module

Download and install (aka get the .tgz and upload it to /sites/all/modules) and enable the module  (in the main Drupal Modules menu)

1. Enable it with: Administer -> Site building -> Modules
1. Administer -> Site configuration -> Wysiwyg
1. lists which editor modules you can use (and a helpful download link)
1. e.g. TinyMCE (Download) Not installed.
1. Extract the archive and copy its contents into a new folder in the following location: **sites/all/libraries/tinymce**
1. Administer -> Site configuration -> Input formats
1. Ensure that the "Content Manager Role" (or authenticated user?) has access to Full HTML  
Also you can set the default format to Full HTML
(alternatively you can create a more limited input type role that matches your paranoia)

1. Administer -> Site configuration -> Wysiwyg
1. Input Format = Full HTML = TinyMCE 3.8.8
1. Edit the profile of your WYSIWYG editor to decide which buttons/functions are displayed

Up until now (by default) you only get bold and inserting images that are already uploaded...

### Setting up IMCE (Image Manager)

IMCE (image manager) (with the WYSIWYG bridge module)

Download and install (aka get the .tgz and upload it to /sites/all/modules) and enable the module  (in the main Drupal Modules menu)

1. Administer -> Site building -> Modules
1. Administer -> Site configuration -> IMCE -> User-1  
1. Configure any specific settings, then give a role (e.g. Content Manager) permission
1. Administer -> Site configuration -> IMCE
1. Enable the Image button (as IMCE is accessed from the Image plugin).
1. Enable the IMCE plugin in the plugins/buttons configuration of the wysiwyg profiles of your choice. (checkbox)
1. Edit the profile of your WYSIWYG editor to decide which buttons/functions are displayed.  
> You MUST include the checkbox IMCE...


### Permissions
One of the common gotchas in Drupal is forgetting to set permissions (and having to dig through a ton of UI to find them)

Ensure the future "content manager" role has create content permissions  

1. Administer -> User management -> Roles = Add Role  
1. Administer -> User management ->Permissions
1. Then assign that role to the user

### Verify it all works

Finally a user with the appropriate role (e.g. "content manager" above) can insert bold/underline/etc.  and insert images (and upload photos using IMCE).

1. Log In
2. Create a new article/post
3. In the UI you should see the menu has a lot more buttons
