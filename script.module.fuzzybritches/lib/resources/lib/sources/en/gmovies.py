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

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['goldmovies.xyz']
        self.base_link = 'http://goldmovies.xyz'
        self.search_movie = '/%s/'
        self.search_tv = '/episode/%s'
        self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = self.base_link + self.search_movie % title
            return url
        except:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            title = cleantitle.geturl(tvshowtitle)
            url = self.base_link + self.search_tv % title
            return url
        except:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url == None: return
            url = url + '-season-%s-episode-%s/' % (season, episode)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None: return

            r = self.scraper.get(url).content
            u = client.parseDOM(r, "div", attrs={"id": "lnk list-downloads"})
            for t in u:
                r = client.parseDOM(t, 'a', ret='href')
                for url in r:
                    url = url.split('php?')[1]
                    if '2160p' in url: quality = '4K'
                    elif '1080p' in url: quality = '1080p'
                    elif '720p' in url: quality = '720p'
                    else: quality = 'SD'
                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'direct': True, 'debridonly': False})
            return sources
        except:
            return sources

    def resolve(self, url):
        return url
