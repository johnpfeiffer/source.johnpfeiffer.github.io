Title: 365-24 Javascript on MS CRM Forms
Date: 2010-01-24 19:19
Author: John Pfeiffer
Slug: 365-24-javascript-on-ms-crm-forms

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
Programming isn't always fun and games. Here's an example from me
putting in extra time on a weekend...

</p>

At my work We use Microsoft Dynamics CRM 4.0 which is a customizable CRM
web interface on top of MS SQL Server. While the built in functionality
is pretty good a business always needs some more customization to get
things "just right"...

</p>

MS CRM has "onload" and "onsave" functionality for each entity that
allows a developer to stick in some custom javascript.

</p>

Below is the JS that controls the calculations on the Products section
of a Quote for Customer Form. This improves the end user experience as
user changes update the different fields instantly and automatically
(though they still have to press SAVE to keep those changes).

</p>

Note: Javascript isn't related to Java, it's a "client side" (runs on
your computer, not the server) piece of code frequently used to modify
how things look on your screen.

</p>

--------------------------------------------------------------------------------

</p>
<p>
    // if the Tax field is null (ie a new quote is being created) we fill in a default taxif (crmForm.all.new_taxpercentage.DataValue == null) { crmForm.all.new_taxpercentage.DataValue = 17.5;}//when Loading the Quote Form and on certain fields I have the following:crmForm.all.quantity.FireOnChange();//tells the system to pretend that the Quantity field has just changed //(and run it's jscripts)//this allows for one central place to control all of the calculations--------------------------------------------------------------------------------//this forces even "disabled" fields to update valuescrmForm.all.new_taxpercentage.ForceSubmit = true;//Calculate the BASE amount - MS CRM multicurrency required for moneycrmForm.all.baseamount_base.DataValue = crmForm.all.quantity.DataValue * crmForm.all.priceperunit_base.DataValue//Calculate the baseamount.crmForm.all.baseamount.DataValue = crmForm.all.quantity.DataValue * crmForm.all.priceperunit.DataValue;//Only calculate the discount if the user has actually filled in the discount fieldif( crmForm.all.new_manualdiscountpercentage.DataValue >= 0 ){    //Calculate the manual BASE discount amount. crmForm.all.manualdiscountamount_base.DataValue = crmForm.all.quantity.DataValue * crmForm.all.priceperunit_base.DataValue * (crmForm.all.new_manualdiscountpercentage.DataValue/100);    //Calculate the manual discount amount.  crmForm.all.manualdiscountamount.DataValue = crmForm.all.quantity.DataValue * crmForm.all.priceperunit.DataValue * (crmForm.all.new_manualdiscountpercentage.DataValue/100);}//Tricky piece of math with lots of ( and * and / ...//Calculate the new BASE Tax AmountcrmForm.all.tax_base.DataValue = ((crmForm.all.quantity.DataValue * crmForm.all.priceperunit_base.DataValue) - (crmForm.all.manualdiscountamount_base.DataValue)) * (crmForm.all.new_taxpercentage.DataValue/100);//Calculate the new Tax AmountcrmForm.all.tax.DataValue = ((crmForm.all.quantity.DataValue * crmForm.all.priceperunit.DataValue) -  (crmForm.all.manualdiscountamount.DataValue)) * (crmForm.all.new_taxpercentage.DataValue/100);//Calculate the new Extended BASE AmountcrmForm.all.extendedamount_base.DataValue = (crmForm.all.baseamount_base.DataValue -  crmForm.all.manualdiscountamount_base.DataValue) +  (crmForm.all.tax_base.DataValue);//Calculate the new Extended AmountcrmForm.all.extendedamount.DataValue = (crmForm.all.baseamount.DataValue -  crmForm.all.manualdiscountamount.DataValue) +  (crmForm.all.tax.DataValue);

</div>
</div>
</div>
</p>

