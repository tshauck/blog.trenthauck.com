#!/usr/bin/env python
# -*- coding: utf-8 -*- #

from __future__ import unicode_literals

AUTHOR = u'Trent Hauck'
SITENAME = u'Lambda Omega Lambda'
SITEURL = u'blog.trenthauck.com'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

MARKUP = ('md', 'ipynb')

PLUGIN_PATHS = ['./plugins']
#PLUGINS = ['render_math']

THEME = './theme'

#page information
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

DEFAULT_PAGINATION = False


STATIC_PATHS = (['assets'])

PATH = 'content'

#ARTICLE_DIR = 'posts'
ARTICLE_PATH = ['posts']
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

TIMEZONE = 'US/Pacific'
