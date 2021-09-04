#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'john pfeiffer'
SITENAME = u'john pfeiffer'
# commented out for development
# SITEURL = 'https://blog.john-pfeiffer.com'
OUTPUT_PATH = 'output/'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'
TIMEZONE="America/Los_Angeles"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = 12

# clean urls for pages
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'
# clean urls for articles
ARTICLE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = '{slug}/'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'weekly',
        'pages': 'monthly'
    }
}

THEME = 'themes/pelican-elegant'
PLUGIN_PATHS = ['plugins']
PLUGINS = ['sitemap', 'extract_toc', 'tipue_search', 'post_stats']
MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc']
MARKDOWN = {
  'extension_configs': {
    'markdown.extensions.codehilite': {'css_class': 'highlight'},
    'markdown.extensions.extra': {},
    'markdown.extensions.meta': {},
    'markdown.extensions.toc': {'title': ''},
  },
  'output_format': 'html5',
}

DIRECT_TEMPLATES = (('index', 'tags', 'categories','archives', 'search', '404'))
STATIC_PATHS = ['theme/images', 'themes/images', 'images']
LANDING_PAGE_ABOUT={'title': '', 
'details': "John Pfeiffer began with DOS on a 486, tweaking DOS to make games work and BBS's... <br />Then there was Internet -> University -> Linux -> Football (aka soccer) <br /> Interesting places and cultures I've enjoyed: <br /> California -> Tennessee -> France -> Los Angeles -> Bulgaria -> England -> SF Bay Area <br /> Interesting things I've learned: <br /> Football (soccer) -> Piano -> Karate -> Guitar -> French -> Bulgarian <br /> Still working on: <br /> Be Good, Change the World"}

PROJECTS_TITLE=''
PROJECTS = [{
    'name': 'My CV/Resume',
    'url': 'https://www.linkedin.com/in/foupfeiffer',
    'description': ''},
    {'name': 'My source code',
    'url': 'https://github.com/johnpfeiffer',
    'description': ''}
]
RECENT_ARTICLES_COUNT=20
