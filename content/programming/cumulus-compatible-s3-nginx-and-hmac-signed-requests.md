Title: Cumulus compatible S3, nginx, and HMAC signed requests
Date: 2013-11-26 17:10
Author: John Pfeiffer
Slug: content/cumulus-compatible-s3-nginx-and-hmac-signed-requests


With the exceptionally fast, reliable and popular web server [nginx﻿](http://nginx.org/) as a front end customers can use a browser to access their uploaded
files via a simple URL, the same as the SaaS Amazon S3 implementation, without knowing about the [Cumulus backend](http://www.nimbusproject.org/doc/nimbus/faq/#what-is-cumulus).

Unfortunately there were edge cases around the encodings of spaces,
pluses, slashes, etc. where nginx + Cumulus was returning "Access
Denied" when trying to GET a file.

</p>

Examining the relevant RFC's ([http://tools.ietf.org/html/rfc3986\#section-2.1][])﻿, PHP﻿
([http://php.net/manual/en/function.rawurlencode.php][]) and Python﻿([http://docs.python.org/2/library/urllib.html][]) references, and
examining the ﻿Iogs, I could see the files were PUT correctly, [s3cmd﻿][] could retrieve the binary objects (files) from Cumulus fine... 

but the logs were showing a change in the URL's.



[nginx﻿]: http://nginx.org/
[Cumulus backend]: http://www.nimbusproject.org/doc/nimbus/faq/#what-is-cumulus
[http://tools.ietf.org/html/rfc3986\#section-2.1]: http://tools.ietf.org/html/rfc3986#section-2.1
[http://php.net/manual/en/function.rawurlencode.php]: http://php.net/manual/en/function.rawurlencode.php
[http://docs.python.org/2/library/urllib.html]: http://docs.python.org/2/library/urllib.html
[s3cmd﻿]: http://s3tools.org/s3cmd
[debugging in nginx﻿]: http://nginx.org/en/docs/debugging_log.html
[Cumulus source code﻿]: https://github.com/nimbusproject/nimbus/tree/master/cumulus
[nginx AWS Authentication Module﻿﻿]: https://github.com/anomalizer/ngx_aws_auth
[Python Boto library﻿]: http://docs.pythonboto.org/en/latest/
[supported﻿]: https://github.com/boto/boto/graphs/contributors
[Amazon﻿﻿]: http://aws.amazon.com/sdkforpython/
[signing process﻿]: http://docs.aws.amazon.com/AmazonS3/latest/dev/RESTAuthentication.html
[Programming]: http://john-pfeiffer.com/category/tags/programming



Increasing the [debugging in nginx﻿][], digging into the [Cumulus source
code﻿][] and [nginx AWS Authentication Module﻿﻿][] (and adding more
logging statements in Python and C respectively), I realized there was a
mismatch in the REST URL signature process.

</p>

Since Cumulus was using the open source [Python Boto library﻿][] which
is actually [supported﻿][] by [Amazon﻿﻿][] (the de facto rulers of the
S3 "standard"), I decided that their [signing process﻿][] was
authoritative.

</p>

A lot of digging into nginx configs and source, along with learning a
bit about nginx module development and hacking the source of the
ngx\_aws\_auth module, I finally came up with a matching signature
process, (success!)





    **ngx\_aws\_auth/ngx\_http\_aws\_auth.c**  
    
    /\* uses the source and length to copy the uri, does not escape
    characters  
    
    (the argument signature is compatible wit ngx\_escape\_uri)  
    
    \*/  
    
    uintptr\_t ngx\_uri\_extractor(u\_char \*dst, u\_char \*src, size\_t
    size, ngx\_uint\_t type)  
    
    {  
    
    while (size) {  
    
    \*dst++ = \*src++;  
    
    size--;  
    
    }  
    
    return (uintptr\_t) dst;  
    
    }  
    
    /\* customized to calculate the signature using the non escaped URI,
    compatible with cumulus boto  
    
    \*/  
    
    static ngx\_int\_t  
    
    ngx\_http\_aws\_auth\_variable\_s3(ngx\_http\_request\_t \*r,
    ngx\_http\_variable\_value\_t \*v,  
    
    uintptr\_t data)  
    
    {  
    
    ngx\_http\_aws\_auth\_conf\_t \*aws\_conf;  
    
    unsigned int md\_len;  
    
    unsigned char md[EVP\_MAX\_MD\_SIZE];  
    
    aws\_conf = ngx\_http\_get\_module\_loc\_conf(r,
    ngx\_http\_aws\_auth\_module);</code>
    
    </p>
    
    /\*  
    
    \* This Block of code added to deal with paths that are not on the root
    -  
    
    \* that is, via proxy\_pass that are being redirected and the base part
    of  
    
    \* the proxy url needs to be taken off the beginning of the URI in
    order  
    
    \* to sign it correctly.  
    
    \*/  
    
    u\_char \*uri = ngx\_palloc(r-\>pool, r-\>uri.len + 200); // allow room
    for escaping  
    
    /\*  
    
    u\_char \*uri\_end = (u\_char\*) ngx\_escape\_uri(uri,r-\>uri.data,
    r-\>uri.len, NGX\_ESCAPE\_URI);  
    
    \*/  
    
    u\_char \*uri\_end = (u\_char\*)
    ngx\_uri\_extractor(uri,r-\>unparsed\_uri.data, r-\>unparsed\_uri.len,
    NGX\_ESCAPE\_URI);  
    
    \*uri\_end = '\\0'; // null terminate  
    
    ...  
    

