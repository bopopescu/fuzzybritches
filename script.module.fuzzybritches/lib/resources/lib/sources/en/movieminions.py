# -*- coding: utf-8 -*-
#######################################################################
# ----------------------------------------------------------------------------
# "A BEER-WARE LICENSE"
#  As long as you retain this notice, feel free to do whatever you
# wish with this file. If we meet some day, and you think
# this helped you in some way, you can buy me a beer. Since we most
# likey will never meet, buy a stranger a beer. - The Papaw
# ----------------------------------------------------------------------------
#######################################################################

# Addon Name: Fuzzy Britches
# Addon id: script.module.fuzzybritches
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import re, requests

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['movieminions.net']
        self.base_link = 'https://movieminions.net/english-movies/movies'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.get_query(title)
            title = '%s.%s' % (title, year)
            self.title = title.replace('-', '.')
            year = '-%s/' % year
            url = self.base_link + year
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            result = url
            try:
                r = requests.get(result, timeout=10).content
                r = client.parseDOM(r, "table", attrs={"id": "list"})
                for r in r:
                    r = re.compile('a title=".+?" data-xyz="(.+?)"').findall(r)
                    for url in r:
                        if not self.title in url: continue
                        url = 'http://' + url
                        quality = source_utils.check_url(url)
                        sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            except:
                return
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
