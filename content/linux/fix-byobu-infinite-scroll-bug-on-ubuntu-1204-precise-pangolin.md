Title: Fix Byobu infinite scroll bug on Ubuntu 12.04 Precise Pangolin
Date: 2013-02-15 17:36
Author: John Pfeiffer
Slug: fix-byobu-infinite-scroll-bug-on-ubuntu-1204-precise-pangolin

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
After installing Ubuntu Server 12.04 (Precise Pangolin) I was
disappointed to see that one of my favorite utilities, byobu (an
improvement on the classic screen = multi ssh screen with status and
hotkeys), had an infinite scroll problem. (Quick, type exit before your
screen disappears entirely!)

</p>

Amazingly this bug shipped in the official Ubuntu Release even though
byobu 5.17 lists it as a fixed.

</p>

The easy workaround is:

</p>

<strong>byobu-config  

Toggle status notifications  

Use the arrow keys to scroll down and space bar to disable the logo  

Tab and Enter to Apply -\> then Exit  
</strong>  

Now you can safely use "byobu" on the command line in Ubuntu 12.04!

</p>

p.s. Control + a (screen mode) and then Control + a , then c ... now
you've got multiple screens! (Control + a + 0 to go to screen 0, control
+ a + a to jump to the last used screen)

</p>

[https://help.ubuntu.com/community/Byobu][]

</p>

A fix for Windows Putty users ... Window -\> Translation -\> UTF8 (the
ISO-8859 + byobu UTF8 logo = ugh)

</p>

An untested alternate workaround: .byobu/status::tmux\_left : "logo" -\>
"\#logo" )

</p>

**UPDATE for 12.04.2!**

</p>

byobu in Ubuntu 12.04 uses tmux as the backend. You can change this by
running byobu-select-backend and selecting screen

</p>

Thanks for the tip Eric!

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [Linux][]

</div>
</p>

  [https://help.ubuntu.com/community/Byobu]: https://help.ubuntu.com/community/Byobu
  [Linux]: http://john-pfeiffer.com/category/tags/linux
