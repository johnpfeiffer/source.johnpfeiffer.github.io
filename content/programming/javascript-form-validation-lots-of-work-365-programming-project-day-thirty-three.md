Title: Javascript Form Validation, Lots of work: 365 programming project day thirty three
Date: 2010-02-04 14:59
Tags: javascript, html form

I'm working too much which is why these posts are more infrequent (though I will keep numbering them sequentially and hopefully one day I'll have enough time to backfill all 365 before the 1 year deadline)...

Javascript is meant to easily add functionality to a webpage.

Unfortunately some people don't really test it enough, case in point, an email newsletter went out with a link to an online competition page BUT the submit button "didn't work"...

Here comes John to save the day!

From the HTML everything appeared fine:

    :::html
    <form name="f" method="post" action="send_enquiry_displays.asp">
        <td nowrap>First Name:*  </td>
        
        <td><input class="pTextBox1" name="txFirstName" type="text" value=""></td>
        
        More form stuff here...  Notice that the radio button only has one choice...
        
        <input type="radio" name="rdDisplaySize" value="5.7 VGA TFT"></td>
        
        <td nowrap>Wireless LAN:  </td>
        <td><input type="checkbox" name="ckWirelessLAN" value="1"></td>
        
        <td valign="top"><input type="hidden" name="whereDidYouHear" value="WUNL0309#1"></td>
        
        <td><a href="javascript:checkSingupForm()" onClick="this.blur()" 
        
        onmouseover="genericRollover('elImgSubmit','images/buttons/submit_over.gif');
        window.status='Submit Form';return true;"
        
        onmouseout="genericRollover('elImgSubmit','images/buttons/submit.gif');
        window.status='';return true;">
        
        <img src="images/buttons/submit.gif" name="elImgSubmit"
        alt="Submit Form" width="66" height="22" hspace="10" border="0">
        </a></td>
        
        </table>
        </td>
        </tr>
    </form>
    
    <script language="JavaScript">
    
    function checkSingupForm(){
        var f = document.forms["f"];
        
        //this array should contain every text field you require to be filled in
        	var arr = [
        				 ["txFirstName","First Name"]
        				,["txLastName","Last Name"]
        				,["txCompany","Company"]
        				,["txTown","Town"]
                    ,["txEmail","E-mail"]
        ];
        
        //for loop checks each value if it is blank "" ... then popup alert and changes focus
        for(i=0;i<arr.length;i++){
            if(f.elements[arr[i][0]].value == ""){
                alert("Please fill in " + arr[i][1] + ".")
                f.elements[arr[i][0]].focus();
                return;
            }
        }
        
        //a regular expression check to ensure the email is in a valid email format
        var emailRE = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9_\-])+\.)+([a-zA-Z0-9]{2,4})+$/
        if( !emailRE.exec(f.elements["txEmail"].value) ){
            alert("Please fill in a valid e-mail address.");
            f.elements["txEmail"].focus();
            return;
        }
        
        //ensures that the display size have been filled out... 
        
        rdDisplaySizeValid = -1;
        for( i=0; i< f.elements["rdDisplaySize"].length; i++)
        {
            if( f.elements["rdDisplaySize"][i].checked )
            {	
                rdDisplaySizeValid = 1;	
            }
        }
        
        if( rdDisplaySizeValid == -1 )
        {
            alert("Please choose a Display size.");
            f.elements["rdDisplaySize"][0].focus();
            return;
        }
        
        //ensures that the embeddedconfiguration field has been checked at least once...
        if(!f.elements["rdEmbeddedConfiguration"][0].checked && !f.elements["rdEmbeddedConfiguration"][1].checked) 
        {
            alert("Please choose a Embedded Configuration.");
            f.elements["rdEmbeddedConfiguration"][0].focus();
            return;
        }
        	
        f.submit();
    }
    
    //-->
    </script>
    

After downloading the ASP file and creating a backup copy...

So what was the problem?

The incorrect validation of radio button rdDisplaySize had to be commented out.

I also added the nifty "default CHECKED" option as the form only gave one Radio Button option (but it was a Required field!)

`<input type="radio" name="rdDisplaySize" value="5.7 VGA TFT CHECKED"></td>`

Whew, another crisis averted, customers now able to register for the competition and turn themselves into Leads for our company!
