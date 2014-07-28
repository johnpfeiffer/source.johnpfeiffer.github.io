Title: How to install a Drupal tag cloud
Date: 2010-07-06 12:04
Author: John Pfeiffer
Slug: how-to-install-a-drupal-tag-cloud

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
How to install a Drupal Cloud Tag Block First, in case you've stumbled
on this by mistake (you were looking for Blocks of Drupal "Cloud" cheese
with price tags?)...

</p>

-   Drupal is a "content management system" - a fancy way of saying
    software takes your text/photos and makes them pretty...
    automatically!
-   Tag is an associated "label" - kind of like you migh call a sandwich
    a "cheese sandwich", or "lunch", or a "snack". It's a neat free form
    way to categorize your thoughts without much effort (oh the wonders
    of Computers).

The tagadelic module for Drupal creates a weighted "cloud" of the tags
you have on your content nodes. If you create a "block" on your pages it
is MUCH easier for you and any readers (if you have them?) to
navigate...

</p>

Download the module [http://drupal.org/project/tagadelic][]

</p>

Extract the tar.gz (izarc2go and 7zip) into a folder Upload the folder
to /drupal-root/sites/all/modules (using FTP or preferrably SFTP)

</p>

**Administer -\> Site building -\> Modules -\> List (It appears under
Taxonomy ... Tagadelic**, fill in the checkbox to Enable the module.

</p>

**Administer -\> Site building -\> Blocks -\> List Blocks**

</p>

Tagadelic has already created the following Block parts for you: Tags in
Blog Tags

</p>

Use the dropdown to put the tag in the "Right sidebar" Then drag and
drop it to determine it's order (ie below the search box)

</p>

Finally click on "configure" next to it to select: customize the "title"
above the cloud tag (e.g. Tag Cloud) what pages the block will appear.

</p>

Note: Tags for the current post is an easy way to show "related content"
These tags also may help your SEO but be careful to not overdo it! I
personally like adding the other Block, "Tags for this post" as well
because

</p>

As per my very smart's wife very smart suggestion - an image...

</p>

[![example of a drupal tagadelic tag cloud][]][example of a drupal
tagadelic tag cloud]

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

  [http://drupal.org/project/tagadelic]: http://drupal.org/project/tagadelic
  [example of a drupal tagadelic tag cloud]: http://john-pfeiffer.com/sites/default/files/images/example-of-tagadelic-cloud-tag.gif
  [Drupal]: http://john-pfeiffer.com/category/tags/drupal
