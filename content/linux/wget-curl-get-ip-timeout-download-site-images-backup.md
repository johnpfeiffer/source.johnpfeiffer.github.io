Title: wget curl get ip timeout backup download site including images
Date: 2009-09-06 21:07:02
Tags: linux, wget, curl, get, ip, timeout, download, site, images, http, password, backup

[TOC]

    wget --quiet http://example.com/folder/file --output-document output_filename

    wget --timestamping http://example.com/file.tar.gz
> only download if the remote file is newer by timestamp

### curl

cURL is often installed with Linux/MacOS but depends on a library installed on the operating system.

- <https://en.wikipedia.org/wiki/CURL>
- <https://curl.haxx.se/docs/libs.html>

Given its ease of use and many programming language library wrappers it is a ubiquitous tool for HTTP operations.

    sudo apt-get install -y curl
> install curl on ubuntu

    curl -O https://example.com/folder/file
> download the file using the original file name like wget

    curl -s checkip.amazonaws.com

	curl -s ipinfo.io/ip
	curl -s www.trackip.net/ip
	curl -s whatsmyip.me
	curl -s whatismyip.akamai.com
	curl -s icanhazip.com

    curl --silent --output output_filename http://example.com/filename.html
> download the file with a new local filename

    curl -I --max-time 2 https://172.24.33.133
> HEAD response only and wait at most 2 seconds

    curl --silent --max-time 1 -o /dev/null --insecure -I -w "%{http_code}" --insecure https://172.24.33.133 | grep 200
> only show response status code 200 or nothing

    curl --silent --location --insecure https://example.com
> no transfer output, follow (HTTP) redirects, do not verify the SSL


    curl --header "X-Custom-Header: foobar" http://example.com:8080

<http://curl.haxx.se/docs/manpage.html#-H>

    curl --data-urlencode "name=My Name" http://www.example.com
> does the percent encoding

    curl --request POST http://example.com/resource.cgi

<http://superuser.com/questions/149329/what-is-the-curl-command-line-syntax-to-do-a-post-request>


    curl --header "content-type: application/json" --header "Authorization: TOKEN" -X POST \
    -d '{"name":"Room of Requirement","owner":{"id":1234}}' https://example.com/room/55


### spoofing google bot with curl and wget

    curl -A "Googlebot/2.1 (+http://www.google.com/bot.html)" -O https://support.google.com/webmasters/answer/1061943?hl=en
> spoof googlebot to scrape a page that has nagging javascript

    wget --user-agent="Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" https://example.com
> wget way to spoof googlebot to scrape a page that has nagging javascript

### using browsers to modify post requests or forms

1. Chrome developer tools (control + shift + i)
1. choose Network (panel after Elements)
1. Right click on a request (e.g. GET and choose Copy as cURL)

OR

1. Firefox (maybe requires Firebug extension installed) and (control + shift + k)
1. Network panel (Headers)
1. Edit and Resend

- - -
## wget examples to download a blog and images

    wget "http://johnnypfeiffer.blogspot.com" --mirror --convert-links --warc-file="johnnypfeiffer-blogspot" --warc-cdx=on
> using wget with the new WARC option to m

Backups "outsourced" via <https://archive.org/> but you probably want a local copy (preferably burned to blu-ray) by using <https://en.wikipedia.org/wiki/Web_ARChive>

*(you only need to keep the .warc.gz but the optional .cdx index may help you if later you want to list the contents without browsing the whole warc)*

To view the web archive (even offline) you can try:

- <https://github.com/webrecorder/webrecorderplayer-electron>
- <https://github.com/sbilly/webarchiveplayer>
- <https://github.com/ukwa/webarchive-explorer/tree/master>

    wget -r -H -D bpfeiffer.blogspot.com,1.bp.blogspot.com,2.bp.blogspot.com,3.bp.blogspot.com,4.bp.blogspot.com,www.blogger.blogspot.com,lh6.googleusercontent.com,lh5.googleusercontent.com,lh4.googleusercontent.com,lh3.googleusercontent.com, lh2.googleusercontent.com,lh1.googleusercontent.com -k -p -E -nH -erobots=off -U Mozilla http://bpfeiffer.blogspot.com
> annoyingly have to find each google image server until figured out wildcards with the example list

    wget -r -H -D johnnypfeiffer.blogspot.com,1.bp.blogspot.com,2.bp.blogspot.com,3.bp.blogspot.com,4.bp.blogspot.com,www.blogger.blogspot.com -k -p -E -nH -erobots=off -U Mozilla http://johnnypfeiffer.blogspot.com
> we cannot use the -nd flag because some images have the same name but different servers 1.bp.blogspot.com/NAME.jpg 2.bp.blogspot.com/NAME.jpg*

	-r = recursive (infinite by default)
	-l 2 = number of levels deep to recurse
	-H = span to other sites (examples, i.e. images.blogspot.com and 2.bp.blogspot.com)
	-D example1.com,example2.com = only span to these specific examples
	--exclude-examples  bad.com = do not crawl if the link is from example bad.com
	-k = convert-links (to be accessible entirely locally without internet - it does this at the END after downloading everything)
	-p = download the "page requisities" (i.e. css and images)
	-E = if it doesn't originally end in .html it will once downloaded
	-erobots=off
	-nH = do not prefix  index.html in the johnnypfeiffer.blogspot.com

	-nd = don't bother to create directories for everything
	-P = --directory-prefix=/usr/local/src    (prepends all filenames downloaded with a string, e.g. a local path), by default this is .
	-U = user agent (i.e. Mozilla)

	-O file = puts all of the content into one file, not a good idea for a large site (and invalidates many flag options)
	-O - = outputs to standard out (so you can use a pipe, like wget -O http://kittyandbear.net | grep linux
	-N = uses timestamps to only download newer remote files (which will be stamped with the remote timestamp), depends on server providing Last-Modified header
	
	--no-use-server-timestamps = files will be stamped with download time (default behavior is to stamp the download with the remote file)
	--spider = only checks that pages are there, no downloads (checks if the url / files are correct/exist)

	-b  (backgrounds the job, you can check it via "tail -f wget-log"

- - -
### More wget parameters

	wget -r -H -l1 -k -p -E -nd -erobots=off http://bpfeiffer.blogspot.com
	wget -r -H --exclude-examples azlyrics.com -l1 -k -p -E -nd -erobots=off http://bpfeiffer.blogspot.com
	wget --http-user=user --http-password=pass -r -E -p --convert-links http://website/trac/umr5series/ -b		# backgrounded
	wget -p -k http://www.gnu.org/ -o logfile    		# get css etc. and convert links to local links and outputs a log of actions to logfile
	wget -c = will continue a download of a large file if interrupted
	wget -r -A.pdf http://url-to-webpage-with-pdfs/

	--user-agent="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.3) Gecko/2008092416 Firefox/3.0.3"

	wget --http-user=johnpfeiffer --http-password=* -r -l1 -A "*.pdf" http://wss/test/Forms/AllItems.aspx

	-r = recursive
	-l1 = one level of recursive depth only
	-A "*.pdf" = pdf files only

- - -
    wget --reject=gif WEBSITE-TO-BE-DOWNLOADED
> do not download gifs

     wget -S http://website/
> preserve the original timestamps

    wget -N http://website/
> only get the newer files by timestamp

    wget "ftp://ftp.website/*"
> the double quotes prevent the shell from trying to interpret the *

    wget -m http://website.com
> mirror option

	-m or --mirror
	Turn on options suitable for mirroring [a web site]. This option turns on recursion and time-stamping, 
	sets infinite recursion depth and keeps FTP directory listings. 
	It is currently equivalent to -r -N -l inf --no-remove-listing.


    wget -m --user=user --pasword=pass ftp://ftp.web.com
> ftp site mirror with user & pass

    wget --timestamping -r ftp://ftp.website/
> Run regularly to mirror a website (recursively)



    wget --wait=20 --limit-rate=20K -r -p -U Mozilla http://www.stupidsite.com/
> TO BE POLITE... use the wait and limit rate so as not to crash someone's site (be invisible!)

    wget --no-parent http://site/subdir
> allows you to just get the subdir

    wget --limit-rate=20k -i file.txt
> runs wget from the list of urls in the file at 20KB/s

- - -
### wget with self signed ssl certificates
    wget https://example.com --no-check-certificate

**HTTPS (SSL/TLS) options:**

   --secure-protocol=PR     choose secure protocol, one of auto, SSLv2,
                            SSLv3, and TLSv1.
   --no-check-certificate   don't validate the server's certificate.
   --certificate=FILE       client certificate file.
   --certificate-type=TYPE  client certificate type, PEM or DER.
   --private-key=FILE       private key file.
   --private-key-type=TYPE  private key type, PEM or DER.
   --ca-certificate=FILE    file with the bundle of CA's.
   --ca-directory=DIR       directory where hash list of CA's is stored.
   --random-file=FILE       file with random data for seeding the SSL PRNG.
   --egd-file=FILE          file naming the EGD socket with random data.


- - -
    wget --random-wait ftp://user:pass@userver.com/dir
> random pauses to simulate a real user downloading

   --user=user --password=pass

    wget -c ftp://ftp.website/file
> continue downloading a previous wget that was interrupted
> note does not handle a changed file very well...

	--ignore-length			//if some http servers send bogus info out...
	--referer=url 			//if website only allows access from a browser that was previously on their site...


Note that time-stamping will only work for files for which the server gives a timestamp. 

http depends on a Last-Modified header.  ftp depends on a directory listing with dates in a wget parseable format

### .wgetrc for permanent configuration changes

wget could have these changes permanent using the wget startup file .wgetrc


    /usr/local/etc/wgetrc    or per user settings 		$HOME/.wgetrc

    #passive_ftp = off
    waitretry = 10
    #timestamping = off
    
    #recursive = off

- - -
### example wget to scrape java posse podcast mp3s
    wget -U Mozilla -e robots=off --random-wait -r -l1 -H -D "javaposse.com,traffic.libsyn.com" -A "Java*.mp3" http://javaposse.com/2008/05

	-H = --span-hosts = recursive will get from other examples too
	-D = --examples = what examples to download from
	 --exclude-examples = what examples to NOT download

