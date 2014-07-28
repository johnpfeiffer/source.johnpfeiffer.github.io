#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://johnpfeiffer.bitbucket.org'
RELATIVE_URLS = True
FEED_DOMAIN = 'https://johnpfeiffer.bitbucket.org'

LINKS =  (('About John Pfeiffer', 'http://johnpfeiffer.bitbucket.org/pages/about-john-pfeiffer.html'),
          ('CV', 'https://www.linkedin.com/in/foupfeiffer'),
          ('source code', 'https://bitbucket.org/johnpfeiffer'))


FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
DELETE_OUTPUT_DIRECTORY = True
#DISQUS_SITENAME = ""
GOOGLE_ANALYTICS = "UA-3758734-7"
