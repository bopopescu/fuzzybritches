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

import re,urllib,urlparse
from resources.lib.modules import cleantitle,client,source_utils,proxy,cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdm.to']
        self.base_link = 'https://hdm.to'
        self.scraper = cfscrape.create_scraper()


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            tit = cleantitle.geturl(title)
            url = '%s/%s/' % (self.base_link,tit)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = self.scraper.get(url).content
            try:
                match = re.compile('<iframe.+?src="(.+?)"').findall(r)
                for url in match:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False}) 
            except:
                return
        except Exception:
            return
        return sources


    def resolve(self, url):
        return url

