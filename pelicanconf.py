#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
SITENAME = 'shambo.li'
DOMAIN = 'shambo.li'
BIO_TEXT = """just a person who does some things online<hr>
occasionally posts writeups, occasionally participates in ctfs, occasionally plays video games
"""
FOOTER_TEXT = 'Powered by <a href="http://getpelican.com">Pelican</a>, <a href="https://github.com/iKevinY/pneumatic">Pneumatic</a> and <a href="http://pages.github.com">GitHub Pages</a>.'

SITE_AUTHOR = 'n'
TWITTER_USERNAME = '@shamb0li'
INDEX_DESCRIPTION = 'website of some person who posts stuff'

SIDEBAR_LINKS = [
    '<a href="/about-me/">About</a>',
    '<a href="/archive/">Archive</a>',
]

SOCIAL_ICONS = [
    ('mailto:n@shambo.li', 'send me an email', 'fa-envelope-o'),
    ('http://twitter.com/shamb0li', 'follow me on twitter', 'fa-twitter'),
    ('http://github.com/shamboli', 'shamboli github', 'fa-github')
]

AUTHOR = u'n'
SITENAME = u'shambo.li'
SITEURL = 'https://shambo.li'
PATH = 'content'
TIMEZONE = 'America/Chicago'
DEFAULT_LANG = u'en'
RELATIVE_URLS = True
DEFAULT_PAGINATION = False
SUMMARY_MAX_LENGTH = 42
TYPOGRIFY = True

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Plugins
PLUGIN_PATHS = ['plugins']
PLUGINS = ['neighbors', 'assets']

# Navigation Bar
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_PAGES_ON_MENU = True

# Dev
CACHE_CONTENT = False
DELETE_OUTPUT_DIRECTORY = True
OUTPUT_PATH = 'develop'
PATH = 'content'

templates = ['404.html']


# Theme configuration
THEME = 'pneumatic' 
STATIC_PATHS = ['includes', 'images', 'extras', 'pages']
extras = ['CNAME', 'favicon.ico', 'keybase.txt', 'robots.txt']
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = ARTICLE_URL + 'index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = PAGE_URL + 'index.html'
ARCHIVES_SAVE_AS = 'archive/index.html'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'


# Extensions
MARKDOWN = {
    'extension_configs': {
        'markdown.extensions.admonition': {},
        'markdown.extensions.codehilite': {'linenums': None},
        'markdown.extensions.extra': {},
    },
    'output_format': 'html5',
}

# Extras
ICONS_PATH = 'images/icons'
