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

import re

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.language = ['en']
        self.domains = ['123movies4u.cz', '123movies4u.ch']
        self.base_link = 'https://123movies4u.cz'
        self.search_link = '/movie/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('--', '-')
            url = self.base_link + self.search_link % title
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            hostDict = hostDict + hostprDict
            sources = []
            r = client.request(url)
            qual = re.compile('<span class="quality">(.+?)<').findall(r)
            if 'DVD' in qual:
                quality = '720p'
            else:
                quality = 'SD'
            u = client.parseDOM(r, "div", attrs={"id": "link_list"})
            for t in u:
                u = client.parseDOM(t, 'a', ret='href')
                for url in u:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if host not in hostDict:
                        continue
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
                return sources
        except:
            return

    def resolve(self, url):
        return url
