# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches
# Addon id: script.module.fuzzybritches
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''

import re

from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hackimdb.com']
        self.base_link = 'https://hackimdb.com'
        self.search_link = '/title/&%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
            r = self.scraper.get(url, headers=headers).content
            try:
                try:
                    match = re.compile('<iframe .+?src="(.+?)"').findall(r)
                    for url in match:
                        if 'youtube' in url:
                            continue
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            sources.append(
                                {'source': host, 'quality': '720p', 'language': 'en', 'url': url, 'direct': False,
                                 'debridonly': False})
                except:
                    return
                try:
                    match = re.compile('<iframe src="(.+?)"').findall(r)
                    for url in match:
                        if 'youtube' in url:
                            continue
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            sources.append(
                                {'source': host, 'quality': '720p', 'language': 'en', 'url': url, 'direct': False,
                                 'debridonly': False})
                except:
                    return
            except:
                return
        except Exception:
            return
        return sources

    def resolve(self, url):
        return url
