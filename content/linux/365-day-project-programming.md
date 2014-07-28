Title: 365 Day Project: Programming
Date: 2010-01-15 17:38
Author: John Pfeiffer
Slug: 365-day-project-programming

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
I have been inspired by my wife's 365 day project
([http://www.flickr.com/photos/big\_rock\_cat/][]) to do a photograph a
day for 2010.

</p>

I spend my working days and much of my free time installing, repairing,
updating, maintaining, and administering computers, servers, routers,
business software, etc.

</p>

Yet I have long wanted to focus more on Programming, and rather than
spending my spare time reinstalling Linux (ok Stallman, GNU/Linux) and I
thought that a little structure and motivation would help me channel my
energies.

</p>

So every day I will write a program, "A set of coded instructions that
enables a machine, especially a computer, to perform a desired sequence
of operations."

</p>

To keep it a S.M.A.R.T. goal (Specific = 1 program, Measurable = per
day, Achievable = I hope so, Relevant\*, Tangible = all source code
posted) I will try to utilize some fundamental good rules of
programming:

</p>

\1. high level plan  

\2. modular  

\3. devise a test and desired outcome before you start coding  

\4. clean, descriptive variable and function names with a minimum of
parameters  

\5. comments built into the code

</p>

\*Relevant = my own rules for this are that it must be code writing that
makes something happen: e.g. coding html is ok, changing the color/theme
on a website by clicking a menu is not. Writing a script to install
something is ok, installing something by choosing menu options is not.

</p>

It can be on any platform or hardware Windows, Linux, WinCE, Android,
laptop, desktop, server, virtual machine, phone, etc.

</p>

Building up little pieces into a larger one is ok, in fact it's not only
Programming best practice but one of the goals of the whole project
(shhh... to be revealed at the end!)

</p>

Building little applications: first a program to display hard coded
data, then a program to take hard coded data and do something to it
(e.g. add up a bunch of numbers), then a program to get input from a
user, then a program to integrate all of the above!

</p>

Learning by copying others is ok for just learning but my code has to be
modified enough to represent my work and understanding.  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
- - - - - - - - - - - - - - - - - - - - - - - - - - - -

</p>

Enough talking, let's see some code!

</p>

**Pseudo Code (aka high level plan)**  

I want a web page that when a user hovers their mouse over an image it
changes.

</p>

I will use html and css

</p>

First I need to create the original image and the "hovered" image.

</p>

My first "test" is that after I upload them I can actually see them  

(e.g. debugging that they're at the right location)

</p>

< html\>  

< head\>  

< !-- this is embeddeding my cascading style sheet commands directly
into the HTML --\>  

< style type="text/css"\>

</p>

/\* a block displays down, inline would display it to the right  

The width and the height of the image are important (otherwise it won't
all show)  

We remove "text decoration" to prevent any funny "anchor link" borders  

\*/

</p>

\#rollover {  

display: block;  

width: 190px;  

height: 80px;  

text-decoration: none;  

background: url("[http://kittyandbear.net/images/blog/usa-image.png][]")
no-repeat 0 0;  

}

</p>

\#rollover:hover  

{  

width: 190px;  

height: 80px;  

text-decoration: none;  

background:
url("[http://kittyandbear.net/images/blog/usa-image-hover.png][]")
no-repeat 0 0;  

}

</p>

< /style\>  

< /head\>

</p>

< body\>  

I require 2 images, the original and a "hovered over" image:  

< br /\>

</p>

< a id="rollover" href="\#"\>< span\>< /span\>< /a\>

</p>

< br /\>  

Notice there was a delay sometimes, a recommended solution would be to
use a single image and a tricky "only show the half that you want to
see", e.g. normal top half, "hover" = lower half.

</p>

< /body\>  

< /html\>

</p>

Voila!  
[http://kittyandbear.net/john/web-tutorials/css-image-mouseover.htm][]

</p>

One down, many more to go!

</p>
<p>
</div>
</div>
</div>
</p>

  [http://www.flickr.com/photos/big\_rock\_cat/]: http://www.flickr.com/photos/big_rock_cat/
  [http://kittyandbear.net/images/blog/usa-image.png]: http://kittyandbear.net/images/blog/usa-image.png
  [http://kittyandbear.net/images/blog/usa-image-hover.png]: http://kittyandbear.net/images/blog/usa-image-hover.png
  [http://kittyandbear.net/john/web-tutorials/css-image-mouseover.htm]: http://kittyandbear.net/john/web-tutorials/css-image-mouseover.htm
