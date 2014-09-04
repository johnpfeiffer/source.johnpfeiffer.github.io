#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'john pfeiffer'
SITENAME = u'johnpfeiffer'
# uncomment before publishing
# SITEURL = u'http://johnpfeiffer.bitbucket.org'
OUTPUT_PATH = 'output/'
DEFAULT_DATE_FORMAT = '%Y-%m-%d'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = 10

# clean urls for pages
PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'
# clean urls for articles
ARTICLE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = '{slug}'

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
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

THEME = 'themes/pelican-elegant'
PLUGIN_PATHS = ['plugins']
PLUGINS = ['sitemap', 'extract_toc', 'tipue_search']
MD_EXTENSIONS = ['codehilite(css_class=highlight)', 'extra', 'headerid', 'toc']
DIRECT_TEMPLATES = (('index', 'tags', 'categories','archives', 'search', '404', 'table'))
STATIC_PATHS = ['theme/images', 'themes/images', 'images']
LANDING_PAGE_ABOUT={'title': '', 
'details': "John Pfeiffer began with DOS on a 486, tweaking DOS to make games work and BBS's... <br />Then there was Internet -> University -> Linux -> Football (aka soccer) <br /> Interesting places and cultures I've enjoyed: <br /> California -> Tennessee -> France -> Los Angeles -> Bulgaria -> England -> SF Bay Area <br /> Interesting things I've learned: <br /> Football (soccer) -> Piano -> Karate -> Guitar -> French -> Bulgarian <br /> Still working on: <br /> Be Good, Change the World"}

PROJECTS_TITLE='Likes'
PROJECTS = [{
    'name': 'My CV/Resume',
    'url': 'https://www.linkedin.com/in/foupfeiffer',
    'description': ''},
    {'name': 'My source code',
    'url': 'https://bitbucket.org/johnpfeiffer',
    'description': ''},
    {'name': '', 'url': '', 'description': 'Clean Code by Robert C. "Uncle Bob" Martin'},
    {'name': '', 'url': '', 'description': 'Foundations of Programming - Building Better Software by Karl Seguin'},
    {'name': '', 'url': '', 'description': 'The C Programming Language (2nd Edition) by Brian Kernighan and Dennis Ritchie'},
    {'name': '', 'url': '', 'description': 'Effective Java Programming Language Guide by Joshua Bloch'},
    {'name': '', 'url': '', 'description': 'Racing the Beam by Nick Montfort and Ian Bogost'},
    {'name': '', 'url': '', 'description': 'Steve Jobs by Walter Isaacson'},
    {'name': '', 'url': '', 'description': "Founders at Work: Stories of Startups' Early Days by Jessica Livingston"},
    {'name': '', 'url': '', 'description': 'Peopleware: Productive Projects and Teams by Tom DeMarco, Timothy Lister'},
    {'name': '', 'url': '', 'description': 'The Mythical Man-Month: Essays on Software Engineering by Frederick P. Brooks Jr.'},
    {'name': '', 'url': '', 'description': 'Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Ralph Johnson, John Vlissides, Richard Helm'},
    {'name': '', 'url': '', 'description': 'Applied Cryptography by Bruce Schneier'},
    {'name': '', 'url': '', 'description': 'The Algorithm Design Manual, 2nd Edition by Steven Skiena'},
    {'name': '', 'url': '', 'description': 'Testing Computer Software, 2nd Edition by Cem Kaner, Jack Falk, Hung Q. Nguyen'}
]

