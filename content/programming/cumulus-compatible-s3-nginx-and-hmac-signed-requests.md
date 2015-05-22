Title: Cumulus compatible S3, nginx, and HMAC signed requests
Date: 2013-11-26 17:10
Tags: c,nginx

With the exceptionally fast, reliable and popular web server **[nginx](http://nginx.org/)** as a front end customers can use a browser to access their uploaded files via a simple URL, the same as the SaaS Amazon S3 implementation, without knowing about the **[Cumulus backend](http://www.nimbusproject.org/doc/nimbus/faq/#what-is-cumulus)**.

Unfortunately there were edge cases around the encodings of spaces, pluses, slashes, etc. where nginx + Cumulus was returning "Access Denied" when trying to GET a file.

Examining the relevant RFC's (<http://tools.ietf.org/html/rfc3986\#section-2.1>), PHP
(<http://php.net/manual/en/function.rawurlencode.php>) and Python  ﻿(<http://docs.python.org/2/library/urllib.html>) references, and examining the logs, I could see the files were PUT correctly, [s3cmd](http://s3tools.org/s3cmd) could retrieve the  binary objects (files) from Cumulus fine... but the logs were showing a change in the URL's.

Increasing the [debugging in nginx](http://nginx.org/en/docs/debugging_log.html), digging into the [Cumulus source
code](https://github.com/nimbusproject/nimbus/tree/master/cumulus) and [nginx AWS Authentication Module](https://github.com/anomalizer/ngx_aws_auth) (and adding more logging statements in  Python and C respectively), I realized there was a mismatch in the REST URL signature process.

Since Cumulus was using the open source [Python Boto library](http://docs.pythonboto.org/en/latest/) which is actually [supported](https://github.com/boto/boto/graphs/contributors) by [Amazon](http://aws.amazon.com/sdkforpython) (the de facto rulers of the S3 "standard"), I decided that their [signing process](http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html) was authoritative.

A lot of digging into nginx configs and source, along with learning a bit about nginx module development and hacking the source of the ngx_aws_auth module, I finally came up with a matching signature process, (success!)



**ngx\_aws\_auth/ngx\_http\_aws\_auth.c**  

    :::c    
    /* uses the source and length to copy the uri, does not escape characters
    (the argument signature is compatible with ngx_escape_uri)
    */
    uintptr_t ngx_uri_extractor(u_char *dst, u_char *src, size_t size, ngx_uint_t type)
    {
        while (size) {
            *dst++ = *src++;
            size--;
        }
        return (uintptr_t) dst;
    }
    
    /* customized to calculate the signature using the non escaped URI, compatible with cumulus boto
    */
    static ngx_int_t
    ngx_http_aws_auth_variable_s3(ngx_http_request_t *r, ngx_http_variable_value_t *v,  uintptr_t data)
    {
        ngx_http_aws_auth_conf_t *aws_conf;
        unsigned int md_len;
        unsigned char md[EVP_MAX_MD_SIZE];
        aws_conf = ngx_http_get_module_loc_conf(r, ngx_http_aws_auth_module);
        
        /*
        * This Block of code added to deal with paths that are not on the root -
        * that is, via proxy_pass that are being redirected and the base part of
        * the proxy url needs to be taken off the beginning of the URI in order
        * to sign it correctly.
        */
        u_char *uri = ngx_palloc(r->pool, r->uri.len + 200); // allow room for escaping
        /*
        u_char *uri_end = (u_char*) ngx_escape_uri(uri,r->uri.data, r->uri.len, NGX_ESCAPE_URI);
        */
        u_char *uri_end = (u_char*) ngx_uri_extractor(uri,r->unparsed_uri.data, r->unparsed_uri.len, NGX_ESCAPE_URI);
        *uri_end = '\0'; // null terminate
        ...
    }
