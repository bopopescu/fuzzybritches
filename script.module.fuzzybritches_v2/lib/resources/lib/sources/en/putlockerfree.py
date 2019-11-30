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
        self.language = ['en']
        self.domains = ['putlockersfree.sc', 'putlockerfree.sc']
        self.base_link = 'https://putlockersfree.sc'
        self.search_link = '/search-query/%s+%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            mtitle = cleantitle.geturl(title)
            url = self.base_link + '/films/%s-%s/' % (mtitle, year)
            url = client.request(url, timeout='10', output='geturl')
            return url
        except:
            return


    #def movie(self, imdb, title, localtitle, aliases, year):
        #try:
            #mtitle = cleantitle.geturl(title).replace('-', '+')
            #u = self.base_link + self.search_link % (mtitle, year)
            #u = client.request(u)
            #i = client.parseDOM(u, "div", attrs={"class": "movies-list movies-list-full"})
            #for r in i:
                #r = re.compile('<a href="(.+?)"').findall(r)
                #for url in r:
                    #ctitle = cleantitle.geturl(title).replace("+", "-")
                    #if not ctitle in url:
                        #continue
                    #return url
        #except:
            #return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            url = url + "watching.html/"
            r = client.request(url)
            t = re.compile('data-.+?="(.+?)".+?href="javascript:void').findall(r)
            for url in t:
                valid, host = source_utils.is_host_valid(url, hostDict)
                if valid:
                    quality, info = source_utils.get_release_quality(url, url)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        return url


