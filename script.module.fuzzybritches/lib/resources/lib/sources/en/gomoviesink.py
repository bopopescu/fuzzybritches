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
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['www.gomovies.ink']
        self.base_link = 'https://www.gomovies.ink'
        self.search_link = '/?s=%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '+')
            u = self.base_link + self.search_link % title
            u = client.request(u)
            i = client.parseDOM(u, "div", attrs={"class": "movies-list movies-list-full"})
            for r in i:
                r = re.compile('<a href="(.+?)"').findall(r)
                for url in r:
                    title = cleantitle.geturl(title)
                    if not title in url:
                        continue
                    return url
        except:
            return url

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            hostDict = hostprDict + hostDict
            print url
            r = client.request(url)
            qual = re.compile('class="quality">(.+?)<').findall(r)
            for i in qual:
                if 'HD' in i:
                    quality = '720p'
                else:
                    quality = 'SD'
            r = client.parseDOM(r, "div", attrs={"id": "mv-info"})
            for i in r:
                t = re.compile('<a href="(.+?)"').findall(i)
                for url in t:
                    t = client.request(url)
                    t = client.parseDOM(t, "div", attrs={"id": "content-embed"})
                    for u in t:
                        i = re.findall('iframe src="(.+?)"', u)
                        for url in i:
                            valid, host = source_utils.is_host_valid(url, hostDict)
                            if valid:
                                sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except:
            return sources
        

    def resolve(self, url):
        return url
