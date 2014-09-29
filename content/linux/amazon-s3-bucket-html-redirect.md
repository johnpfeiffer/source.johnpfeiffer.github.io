Title: Amazon S3 Bucket HTML Redirect
Date: 2012-04-13 23:57
Slug: content/amazon-s3-bucket-html-redirect
Tags: Amazon, S3, redirect

[TOC]

Goal: More efficient and less error prone method to update a regularly
changed downloadable file

Web page redirects enable you to change the URL of a web page on your S3 hosted website (e.g., from www.example.com/oldpage to www.example.com/newpage) without breaking links pointing to the old URL. Users accessing the old URL will automatically be redirected to the new one.

### Redirect a single object

Amazon updated their functionality to allow per object meta data based redirects:

1. WebUI
1. Object properties
1. Metadata
1. Add Website Redirect Location
1. either /newpage.html (internal redirect) or http://example2.com/page.html (external redirect)

Or PUT the object (or a zero byte file) with the x-amz-website-redirect-location header set (i.e. http://example2.com/page.html)

Or use the universal static html redirect method:

So upload the following download.html that includes

    <head>
    <meta http-equiv="refresh" content="0; url=http://example.com/file-v2.tar.gz">
    </head>

Whenever you have a new version of your file you only have to upload a new "download.html" with an updated meta refresh header and any Users and links will always download the newest version of your file.

Note, javascript may help you open the download and then return to the
original page but have strange interactions for a .txt file...

    <script type="text/javascript">
    <!--
    window.location = "http://example.com/file-v2.tar.gz"
    //-->
    </script>

### Redirect a domain
With two domains, example1.com and example2.com:

1. Create an s3 bucket for example1.com (static web hosting)
1. Set bucket property in the "Static Web Hosting" section, select "Redirect all requests to another host name" to redirect to example2.com
1. Configure Route53 (AWS DNS) for example1.com to have an A record that has an Alias Target as an S3 Website Endpoint (the bucket from step 1)
1. Register example1.com to use the Amazon name servers (from Route53)
1. Add any further subdomain redirects (e.g. www.example1.com) by repeating steps 1 and 2

### more info

<http://docs.aws.amazon.com/AmazonS3/latest/dev/how-to-page-redirect.html>
