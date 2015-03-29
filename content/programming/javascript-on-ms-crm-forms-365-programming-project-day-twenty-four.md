Title: Javascript on MS CRM Forms: 365 programming project day twenty-four
Date: 2010-01-24 19:19
Tags: javascript, CRM

Programming isn't always fun and games. Here's an example from me putting in extra time on a weekend...

At my work We use Microsoft Dynamics CRM 4.0 which is a customizable CRM web interface on top of MS SQL Server. While the built in functionality is pretty good a business always needs some more customization to get things "just right"...

MS CRM has "onload" and "onsave" functionality for each entity that allows a developer to stick in some custom javascript.

Below is the JS that controls the calculations on the Products section of a Quote for Customer Form. This improves the end user experience as user changes update the different fields instantly and automatically (though they still have to press SAVE to keep those changes).

Note: Javascript isn't related to Java, it's a "client side" (runs on your computer, not the server) piece of code frequently used to modify how things look on your screen.

- - -

    :::javascript
    // if the Tax field is null (ie a new quote is being created) we fill in a default tax
    if (crmForm.all.new_taxpercentage.DataValue == null) {
        crmForm.all.new_taxpercentage.DataValue = 17.5;
    }
    
    //when Loading the Quote Form and on certain fields I have the following:
    
    crmForm.all.quantity.FireOnChange();
    
    //tells the system to pretend that the Quantity field has just changed
    //(and run it's jscripts)
    //this allows for one central place to control all of the calculations
    
    --------------------------------------------------------------------------------
    
    //this forces even "disabled" fields to update values
    crmForm.all.new_taxpercentage.ForceSubmit = true;
    
    //Calculate the BASE amount - MS CRM multicurrency required for money
    crmForm.all.baseamount_base.DataValue =
        crmForm.all.quantity.DataValue * crmForm.all.priceperunit_base.DataValue
    
    //Calculate the baseamount.
    crmForm.all.baseamount.DataValue = 
        crmForm.all.quantity.DataValue * crmForm.all.priceperunit.DataValue;
    
    
    //Only calculate the discount if the user has actually filled in the discount field
    if( crmForm.all.new_manualdiscountpercentage.DataValue >= 0 )
    {
        	//Calculate the manual BASE discount amount.
        	crmForm.all.manualdiscountamount_base.DataValue =
        crmForm.all.quantity.DataValue * 
        crmForm.all.priceperunit_base.DataValue *
        (crmForm.all.new_manualdiscountpercentage.DataValue/100);
        
        	//Calculate the manual discount amount.
        	crmForm.all.manualdiscountamount.DataValue =
            crmForm.all.quantity.DataValue * crmForm.all.priceperunit.DataValue *
            (crmForm.all.new_manualdiscountpercentage.DataValue/100);
    
    }
    
    //Tricky piece of math with lots of ( and * and / ...
    //Calculate the new BASE Tax Amount
    crmForm.all.tax_base.DataValue =
        ((crmForm.all.quantity.DataValue *
         crmForm.all.priceperunit_base.DataValue) -
        (crmForm.all.manualdiscountamount_base.DataValue)) *
        (crmForm.all.new_taxpercentage.DataValue/100);
    
    //Calculate the new Tax Amount
    crmForm.all.tax.DataValue =
        ((crmForm.all.quantity.DataValue * crmForm.all.priceperunit.DataValue) -
        (crmForm.all.manualdiscountamount.DataValue)) *
        (crmForm.all.new_taxpercentage.DataValue/100);
    
    //Calculate the new Extended BASE Amount
    crmForm.all.extendedamount_base.DataValue =
        (crmForm.all.baseamount_base.DataValue -
        crmForm.all.manualdiscountamount_base.DataValue) +
        (crmForm.all.tax_base.DataValue);
    
    //Calculate the new Extended Amount
    crmForm.all.extendedamount.DataValue =
        (crmForm.all.baseamount.DataValue -
        crmForm.all.manualdiscountamount.DataValue) +
        (crmForm.all.tax.DataValue);

