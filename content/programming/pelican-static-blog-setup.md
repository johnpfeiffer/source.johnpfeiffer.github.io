Title: How to set up a Pelican static blog site
Date: 2014-06-21 20:21
Tags: python, pelican, blog, static site

[TOC]

Pelican is an open source project that converts static text files into an html site.

Why use a static site generator (pelican) instead of a hosted blog platform or a CMS (Content Management System)?

**Because less is more and you should use the right tool for the right job**

- A static site made of html pages is very easy to maintain
- It is also more secure and performance is good too =)
- Allows for straightforward use of version control (git)
- Developers prefer to be able to customize and add functionality (python and javascript)
- Using widely adopted open source software reduces risk (more contributors, more testers, more bugfixes)
- Using a widely adopted platform increases leverage (themes, plugins, tutorials, etc.)


### Install Pelican

`sudo pip install pelican Markdown beautifulsoup4`
> - installing both the pelican and the Markdown packages
> - beautifulsoup4 is a dependency for the later step of the elegant theme TOC and search plugins
> - optionally use virtualenv venv; source venv/bin/activate

**`pelican-quickstart`**

    :::text
    Welcome to pelican-quickstart v3.3.0.
    This script will help you create a new Pelican-based website.
    Please answer the following questions so this script can generate the files needed by Pelican.

    > Where do you want to create your new web site? [.]
    > What will be the title of this web site? johnpfeiffer.bitbucket.org
    > Who will be the author of this web site? john pfeiffer
    > What will be the default language of this web site? [en]
    > Do you want to specify a URL prefix? e.g., http://example.com   (Y/n)
    > What is your URL prefix? (see above example; no trailing slash) https://johnpfeiffer.bitbucket.org
    > Do you want to enable article pagination? (Y/n)
    > Do you want to generate a Fabfile/Makefile to automate generation and publishing? (Y/n)
    > Do you want an auto-reload & simpleHTTP script to assist with theme and site development? (Y/n)
    > Do you want to upload your website using FTP? (y/N)
    > Do you want to upload your website using SSH? (y/N)
    > Do you want to upload your website using Dropbox? (y/N)
    > Do you want to upload your website using S3? (y/N)
    > Do you want to upload your website using Rackspace Cloud Files? (y/N)
    Done. Your new project is available at /home/ubuntu/BLOG

- - - 

`tree`

    :::text
    .
    ├── content
    ├── develop_server.sh
    ├── fabfile.py
    ├── Makefile
    ├── output
    ├── pelicanconf.py
    └── publishconf.py
    
    2 directories, 5 files

- - -
### Create Content
`vi content/hello_world.md`

    :::text
    Title: My first blog post
    Date: 2014-06-21 20:20
    Tags: python
    Slug: my-first-blog-post
    Author: John Pfeiffer
    Summary: Short version for index and feeds

    This is the content of my first blog post.


>optional UI markdown editor: 
`sudo apt-get install retext`

- - - 
### Run a dev server to see the results locally
`make devserver`
> ...Starting up Pelican and pelican.server...

`./develop_server.sh stop`
>  stop the dev server (required if reloading the .conf file)

**This only works with the basic first setup, after that it is better to manually use multiple screens:**

`make clean`

`make regenerate`
> auto detects any content changes and reloads itself

`cd output; python -m SimpleHTTPServer`
> Serving HTTP on 0.0.0.0 port 8000 ... (Control + C to quit)

**http://localhost:8000**

- <http://docs.getpelican.com/en/latest/publish.html>

#### Setup a static Pages directory

Besides lots of articles in categories it can be useful to have a few pages like About or Contact
    mkdir -p content/pages
    echo "Title: About Us" > content/pages/about.md

<http://docs.getpelican.com/en/latest/content.html#pages>

- - -
### Publish
I just use the pelicanconf output rather than publishconf, and I use git with a bitbucket static html site.

- - -
### Example pelican configuration file

*Contains the elegant theme and tipue search plugin*

```vi pelicanconf.py```

    :::text
    #!/usr/bin/env python
    # -*- coding: utf-8 -*- #
    from __future__ import unicode_literals

    AUTHOR = u'john pfeiffer'
    SITENAME = u'johnpfeiffer'
    SITEURL = u'https://blog-john-pfeiffer.com'
    OUTPUT_PATH = 'output/'
    DEFAULT_DATE_FORMAT = '%Y-%m-%d'
    TIMEZONE="America/Los_Angeles"
    
    # Feed generation is usually not desired when developing
    FEED_ALL_ATOM = None
    CATEGORY_FEED_ATOM = None
    TRANSLATION_FEED_ATOM = None

    # clean urls for pages , trailing slash to support HTTPS
    PAGE_URL = '{slug}/'
    PAGE_SAVE_AS = '{slug}/index.html'
    # clean urls for articles
    ARTICLE_SAVE_AS = '{slug}/index.html'
    ARTICLE_URL = '{slug}/'

    DEFAULT_PAGINATION = 10

    THEME = 'themes/pelican-elegant'
    PLUGIN_PATHS = ['plugins']
    PLUGINS = ['sitemap', 'extract_toc', 'tipue_search', 'post_stats']
    MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc']
    DIRECT_TEMPLATES = (('index', 'tags', 'categories','archives', 'search', '404'))
    STATIC_PATHS = ['theme/images', 'images']

    SITEMAP = {
        'format': 'xml',
        'priorities': {
            'articles': 0.5,
            'indexes': 0.5,
            'pages': 0.5
         },
        'changefreqs': {
            'articles': 'monthly',
            'indexes': 'daily',
            'pages': 'monthly'
        }
    }

> Hint: if you use SSL (e.g. cloudflare) then make sure your SITEURL is https and there are trailing slashes on your clean url helpers PAGE_URL and ARTICLE_URL otherwise you may get mixed content warnings or mixed http and https links in your output html


    cp -a pelicanconf.py publishconf.py
> Update publishconf.py with any final tweaks that should occur only in Production

- - -
### Pelican Themes

[https://github.com/getpelican/pelican-themes][pelicanthemes]
[pelicanthemes]: https://github.com/getpelican/pelican-themes

`git clone --recursive https://github.com/getpelican/pelican-themes ~/pelican-themes`

[http://pelican.readthedocs.org/en/latest/pelican-themes.html][pelicanthemesdocs]
[pelicanthemesdocs]: http://pelican.readthedocs.org/en/latest/pelican-themes.html

    mkdir themes
    cp -a pelican-themes/elegant themes/
> This is the lazy way, the correct way is to only copy in the theme you are using ;)

> FYI For the elegant with tipuesearch you need to also install the tipuesearch plugin

- <http://moparx.com/2014/04/adding-search-capabilities-within-your-pelican-powered-site-using-tipue-search/>


### Depedency Management by Vendoring in Version Control

Dependencies are always hard and leveraging the work of others (themes and plugins) means you have to consider how to manage changes to those moving parts too.

Using your Build/CI/CD server to grab the latest themes/plugins is a mistake because while you would benefit from any new features and bug fixes you will also get burned (yes it has happened to me!) when you are publishing a blog post and suddenly your site doesn't work.  

(Oh are you using Continuous Post Deploy Smoke Tests and Realtime Everything Monitoring to detect this on your blog?)

I highly recommend "vendoring" by copying pelican-elegant into the themes subdirectory in your version control.

This sort of pinning makes an explicit choice that will ensure your site will continue to work until you choose to next upgrade.  Pinning in the Build/CI/CD server by git sha will also work but makes it harder to keep everything in one place for development.

> The drawback of "vendoring" is the technical debt by the inevitable customization that occurs in this "directory separated" fork of the original

- - - 
### Pelican Plugins
[https://github.com/getpelican/pelican-plugins][pelicanplugins]
[pelicanplugins]: https://github.com/getpelican/pelican-plugins

    git clone https://github.com/getpelican/pelican-plugins
    mkdir plugins
    cp -a pelican-plugins/sitemap plugins/
    
> note this is the lazy way, a more precise way would be to only copy in the plugins used

### Hacking ListJS and per Article word count into a theme

Basically once you get the hang of the config file format (just python really) and the templating engine (HTML with some jinja2) you can add all sorts of interesting pieces.

In this example I leverage some javascript and another pelican plugin (python) to allow sorting and filtering on more data than the usual "archives.html" provides.


    <div id="article-list">
        <button class="sort" data-sort="date">date</button>
        <button class="sort" data-sort="title">title</button>
        <button class="sort" data-sort="wordcount">word count</button>
        <button class="sort" data-sort="category">category</button>
        <input class="search" placeholder="Find by filter" style="margin-top: 10px; height: 16px;"/>
        &nbsp; from {{ dates| length }} articles
    
        <ul class="list">
        {% for category, articles in categories %}
            {% for article in articles %}
            <li>
                <span class="date" style="padding-right: 10px;">
                    <time pubdate="pubdate" datetime="{{ article.date.isoformat() }}">{{ article.locale_date }}</time>
                </span>
                <a href="{{ SITEURL }}/{{ article.url }}"><span class="title">{{ article.title }} {%if article.subtitle %}
                    <small> {{ article.subtitle }} </small> {% endif %}</span> </a>
                <em><span class="wordcount">({{ article.stats['wc'] }} words)</span></em>
                <em><span class="category">{{ article.category }}</span></em>
            </li>
            {% endfor %}
        {% endfor %}
        </ul>
    </div>
    ...
    ...
    <script type="text/javascript">
        var options = {
            valueNames: [ 'date', 'title', 'wordcount', 'category'],
            page: 1000
        };
        var hackerList = new List('article-list', options);
        hackerList.sort('date', { order: "desc" })
    </script>


- <https://blog.john-pfeiffer.com/listjs-sort-filters-search-and-more-for-html-lists-and-tables-in-javascript/>
- <https://github.com/getpelican/pelican-plugins/tree/master/post_stats>

### Advanced: skipping the Makefile

    pelican --help
    pelican ./content -o ./output -s ./publishconf.py
    cd output ; python -m SimpleHTTPServer

- - -
### Importing from Drupal with pelican-import

**Hack the Drupal files to allow a lot more than 10 items per feed**
`grep -r 'items per feed' . `
> learned from drupal-7.28/modules/system/system.module

`vi modules/system/system.admin.inc`

>    $form['feed_default_items']
>    
>    Add to the dropdown choices of 10, 15, 30 etc. the option of 999

- - -

    sudo apt-get install pandoc
    sudo pip install feedparser
    pelican-import -h
    pelican-import --feed http://blog.example.com/rss.xml -o output/ -m markdown


### more info
- <https://pelican.readthedocs.org/en/latest/settings.html>
- Tweaking default syntax highlighting:
- - <http://pygments.org/docs/lexers>
- - <http://pygments.org/demo>
- <https://bitbucket.org/johnpfeiffer/docker/src>

    