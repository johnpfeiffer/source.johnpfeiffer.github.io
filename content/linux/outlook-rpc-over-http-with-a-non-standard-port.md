Title: Outlook RPC over HTTP with a non standard port
Date: 2010-06-14 13:03
Author: John Pfeiffer
Slug: outlook-rpc-over-http-with-a-non-standard-port

<div class="field field-name-body field-type-text-with-summary field-label-hidden">
<div class="field-items">
<div class="field-item even">
"The proxy server you have specified is invalid. Correct it and try
again."

</p>

Oh, the wonderful error messages from Microsoft...  

So Outlook 2003 has HTTP and HTTPS hard coded to ports 80 and 443
(wonderfully modular thinking).

</p>

Imagine you want to move your Outlook Web Access to a different port
(security reasons? Or maybe just that another application is hard coded
to port 443...)

</p>

Now it's easy to tell people: [https://mailserver.domain.com:4430][]

</p>

BUT you might have to update any Blackberry using OWA to connect to
Exchange users with the new port...

</p>

and RPC over HTTP (s) is quite useful for the non VPN inclined ...

</p>

The following unsupported workaround works, use at your own risk,
registry editing is required...  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

</p>

In Control Panel -\> Mail -\> Email Accounts -\> View or Change -\>
Change (button) -\> More Settings (button) -\> Connection (tab)

</p>

Checkbox: Connect to my Exchange mailbox using HTTP  

Then the button: Exchange Proxy Settings

</p>

[https://mailserver.domain.com-4430][]

</p>

Connect using SSL only (for the paranoid)  

Mutually authenticate...  

Yes, we need the following: msstd:mail.anders.co.uk  

(note that you may have to download and install the certificate from
your mail server for RPC over HTTP to work, the name we've entered
doesn't have a port because it's the name that's on the SSL certificate)

</p>

Authentication (NTLM = SSL, Basic means anything)

</p>

Click ok a million times and we've finished the easy part...

</p>

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

</p>

Start -\> Run -\> regedit (and hit the OK button)

</p>

(HKCU = hkey\_current\_user)  

HKCU\\Software\\Microsoft\\Windows NT\\CurrentVersion\\Windows Messaging
Subsystem\\Profiles\\\  

</p>

Browse down to the subkey: "13dbb0c8aa05101a9bb000aa002fc45a"  

(don't ask me why these settings are exactly there)

</p>

Locate in the name column: "001f6622" of type REG\_BINARY and double
click on it...

</p>

The "Value Data" will be in hex code (with a preview of the ascii on the
right)

</p>

0000 6D 00 61 00 69 00 6C 00 m.a.i.l.  

0008 65 00 72 00 2E 00 65 00 ......d.  

0010 78 00 61 00 6D 00 70 00 o.m.a.i.  

0018 6C 00 65 00 2E 00 63 00 n......c.  

0020 6F 00 6D 00 **2D** 00 34 00 o.m.-.4.  

0028 34 00 33 00 30 00 30 00 4.3.0.0.  

0030 00 00

</p>

You'll see the 2D in the middle - that's the hex code for '-', we're
going to change it to 3A (or the hex code for ':')  

(yes, we click inside, use the delete key to remove those two and type
in 3A)

</p>

0020 6F 00 6D 00 3A 00 34 00 o.m.:.4.

</p>

Click OK... Whew, hard part's over...  

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  

Now check that your change has taken by going to:

</p>

Control Panel -\> Mail -\> Email Accounts -\> View or Change -\> Change
(button) -\> More Settings (button) -\> Connection (tab)

</p>

You should now see: [https://mailserver.domain.com:4430][]

</p>

Note that you won't be able to click OK (because Outlook detects that
unpermitted colon) but hit Cancel a bunch of times and open up Outlook
to try connecting to your Exchange Server!

</p>

PLEASE NOTE: first ensure that you can get RPC over HTTP working with
the default port 443 (e.g. no colons needed) BEFORE trying a non
standard port as it is a little tricky to remember the certificate, the
firewall port forwarding (if you need to), etc.

</p>

ALSO, remember that to do this you've already changed your Exchange Mail
Server IIS SSL port to the non standard 4430 AND you've fixed any
firewall forwarding for your server so that 4430 goes to your mail
server...

</p>
<p>
</div>
</div>
</div>
<div class="field field-name-taxonomy-vocabulary-1 field-type-taxonomy-term-reference field-label-above clearfix">
### tags:

-   [IT][]

</div>
</p>

  [https://mailserver.domain.com:4430]: https://mailserver.domain.com:4430
  [https://mailserver.domain.com-4430]: https://mailserver.domain.com-4430
  [IT]: http://john-pfeiffer.com/category/it
