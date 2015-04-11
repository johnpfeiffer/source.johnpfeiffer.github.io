Title: Javascript validation of an html form: 365 programming project day twenty six
Date: 2010-01-27 20:44
Tags: javascript, html, form validation

On the 26th I missed my 365 entry because I was being Mr. Corporate IT Hero at our annual Company Meeting but I actually have a number of things from the past that I can comment on and insert...

Everybody who has an HTML form would like some software "intelligence" to guide the User to fill in the "required" fields, or help direct the User if they've not entered a valid email address, etc...

I'm not a fan of Javascript if only because it runs on the client and can be a big security hole. If it's merely written poorly it can crash the browser or confuse the heck out of the user (rendering your HTML Form useless).

But here's the source code on how to do the most basic user input validation:

    :::javascript
    <html><head><title>javascript form validation</title></head>
    <body>
    
    <!-- onSubmit tells the browser that there is a javascript function to run when the user hits the submit button -->
    
    <FORM ACTION="javascript-form-validation.htm" NAME="testform" onSubmit="return validateMyForm()">
    	Starting X Point: <input name="startx" type="text"><br />
    	Starting Y Point: <input name="starty" type="text"><br />
    	Email Address: <input id="email" maxlength="80" name="email" size="20" type="text" />
    	<br />  <br />  
    <input type="submit" />
    </form>
    
    <script type="text/javascript" language="javascript">
    
    function validateMyForm() 
    {
        	if (document.getElementById('startx').value == '') 
        	{
        		alert('Please enter a Starting X value (integer)');
        		document.getElementById('startx').focus();
        		return false;
        	}
        	if (document.getElementById('starty').value == '') 
        	{
        		alert('Please enter a Starting Y value (integer)');
        		document.getElementById('starty').focus();
        		return false;
        	}
        	if (document.testform.email.value == '') {
        		alert('Please enter your email');
        		document.myForm.email.focus();
        		return false;
        	}	
        	
        	//if we've passed all of the above checks
        return true;

    }
    </script> 
    </body>
    </html>


There is a ton more that you can do with Javascript (including for loops on checkboxes minimum 2 out of 5, regular expressions on email addresses, etc.) so hopefully I'll get to it this year!

P.S. You must have Javascript enabled on your browser to see the example and some browsers will pop up "ActiveX Warnings" - if you're paranoid only run Javascript that you've coded yourself!
