Title: Maintaining an old ASP website with Javascript downloads: 365 programming project day twenty eight
Date: 2010-01-28 15:59
Tags: windows, asp, javascript

Our company has an outdated website which was a semi-custom "product catalog" from 2003 (or earlier) that uses SQL and ASP to create dynamic pages and a "webadmin" area to update the catalog (advertised as user friendly because no source code needed).

Modern Content Management Systems (Drupal anyone?) have made this obsolete but like many corporations, "If it's only broken a little and employees bend over backwards to make it work then don't fix or replace it until there's a disaster."

I have had the masochistic pleasure of learning the system: everything in one folder of .asp files calling lots of other ASP files (and a couple of .js files) and calls to the SQL database with obscure 4 digit codes.

Here's an example of me using my programming skills during the day for what might seem a simple request, "Please add another PDF to a page on the Website"...

The first step was to upload the PDF into the database (so that it would be magically assigned a 4 digit number in the SQL).

The webadmin was typically user unfriendly: 

*Login -> Menu with a blank page -> click Catalog tab and finally see the left navigation bar:*

**Catalog Main**

**Catalog Structure**

**Catalog Products**

**Table Headers**

hmmm...  

I got lucky and on my second attempt found Catalog Structure -> Displays -> Intelligent Display Platform

**Up Arrow, Down Arrow, Edit, Delete**  

Given the options I picked the obvious (no, not delete!)

Stuffed in about twenty hot linked words and options I then found "Product Family Files"

Counter-intuitively clicking on a "..." button to access a popup window to upload a new file...

A byzantine system: scrolling through what appears to be every PDF file in the system to verify that my 5.7" file isn't already there... 

Then using a Browse button (on the bottom of the screen) to see the PDF on my desktop, then seperately clicking the Upload button. Finally clicking on a "SELECT" button (at the top of the screen) to finally add it to the database (without any friendly message, just a refresh, so I scrolled through all 300+ items to make sure it was listed).

Bored yet?

Oh, at this point you've got the PDF selected but you still have to click ADD to actually put it in a table for that Product Family.

So... where's the Javascript?

Well this particular page that needs to be updated is actually a custom job that appears instead of the default... and it may even be that I did the work!

So each Product Family is reached by clicking on a link on the homepage, but those links are the inscrutable type:

<http://protect-the-guilty/displays_products.asp?prodFamID=4148>

I "hacked" the scripts.js file (which contains all of the Javascript functions, so maybe they got one thing right)...

    :::javascript
    /* MODIFIED FUNCTION TO GO TO SPECIFIC PAGE INSTEAD OF PULLING FROM DATABASE FOR CERTAIN PRODUCTS*/
    
    function GoToProductLine(prodLineID, partOfFilePath){
    
    	if( (prodLineID != 4136) && (prodLineID != 4536) )
    	{ 
    		location.href = partOfFilePath + "_families.asp?prodLineID=" + prodLineID;
    	}else{
    		location.href = "umr.asp";
    	}
    }


So to locate the "actual" magic 4 digit ID of the PDF I had to go to the original (non redirected) webpage...

<http://protect-the-guilty/displays_products.asp?prodFamID=4148>

View the Source  

Find the following bit of text:  

    :::html
    <td><a href="javascript:void(0)" class="regular" onclick="DownloadFile(1245);">Example_Datasheet_Rev_1.0</a></td>

Whew, almost there!

Next, download the "customized.asp" file and save a backup copy (ALWAYS SAVE A BACKUP!).

Then update the "customized.asp" file by adding your special code to the right place...  

    :::html
    <td><a href="javascript:void(0)" class="regular" onclick="DownloadFile(1245);">Example_Datasheet_Rev_1.0</a></td>

Once you've uploaded and tested it you can look at the clock and happily say, "Uploading 1 pdf took me 2 frickin hours!"
