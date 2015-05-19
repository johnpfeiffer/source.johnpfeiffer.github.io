Title: How to install a Drupal tag cloud
Date: 2010-07-06 12:04
Tags: drupal

How to install a Drupal Cloud Tag Block First, in case you've stumbled on this by mistake (you were looking for Blocks of Drupal "Cloud" cheese with price tags?)...

-   Drupal is a "content management system" - a fancy way of saying software that takes your text/photos and makes them pretty...     automatically!
-   Tag is an associated "label" - kind of like you might call a sandwich a "cheese sandwich", or "lunch", or a "snack". It's a neat free form way to categorize your thoughts without much effort (oh the wonders of Computers).

The tagadelic module for Drupal creates a weighted "cloud" of the tags you have on your content nodes. 

If you create a "block" on your pages it is MUCH easier for you and any readers (if you have them?) to navigate...

1. Download the module <http://drupal.org/project/tagadelic>
1. Extract the tar.gz (izarc2go and 7zip) into a folder Upload the folder to /drupal-root/sites/all/modules (using FTP or preferrably SFTP)
1. **Administer -> Site building -> Modules -> List (It appears under Taxonomy ... Tagadelic**, fill in the checkbox to Enable the module.
1. **Administer -> Site building -> Blocks -> List Blocks**
1. Tagadelic has already created the following Block parts for you: **Tags in Blog Tags**
1. Use the dropdown to put the tag in the "Right sidebar" 
1. Then drag and drop it to determine it's order (ie below the search box)
1. Finally click on "configure" next to it to select: customize the "title" above the cloud tag (e.g. Tag Cloud) what pages the block will appear.

*Note: Tags for the current post is an easy way to show "related content"*

These tags also may help your SEO but be careful to not overdo it! I personally like adding the other Block, "Tags for this post" as well because

As per my very smart's wife very smart suggestion - an image...

[![example-of-a-drupal-tagadelic-tag-cloud.gif]]

