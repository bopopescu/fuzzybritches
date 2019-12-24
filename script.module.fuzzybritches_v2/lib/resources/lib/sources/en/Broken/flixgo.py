# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v2
# Addon id: script.module.fuzzybritches_v2
# Addon Provider: The Papaw

import re
from resources.lib.modules import client
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']  #  Old  flixgo.cc  flixgo.co
        self.domains = ['flixgo.fun']
        self.base_link = 'https://www1.flixgo.fun'
        self.search_link = '/?do=search&mode=advanced&subaction=search&story=%s+%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('-', '+')
            url = self.base_link + self.search_link % (title, year)
            searchPage = client.request(url)
            section = client.parseDOM(searchPage, "div", attrs={"class": "film__cover"})
            for item in section:
                results = re.compile('<a href="(.+?)">').findall(item)
                for url in results:
                    mtitle = cleantitle.geturl(title)
                    if mtitle.lower() in url:
                        url = self.base_link + url
                        return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostDict + hostprDict
            sourcesPage = client.request(url)
            results = re.compile('"file": "(.+?)",').findall(sourcesPage)
            for links in results:
                pattern = "\[(.+?)\]([0-9a-zA-Z-/._?=&:]+)"
                results1 = re.compile(pattern).findall(links)
                for qual1, url1 in results1:
                    quality, info = source_utils.get_release_quality(qual1, url1)
                    if "1080" in quality:
                        continue
                    sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': url1, 'info': info, 'direct': True, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url

