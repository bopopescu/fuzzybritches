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

from resources.lib.modules import cleantitle
from resources.lib.modules import getSum
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['goprojectfreetv.com']
        self.base_link = 'https://www1.goprojectfreetv.com'
        self.tvshow_link = '/watch-%s-season-%s-episode-%s-online/'


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except:
            return


    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowtitle = url
            url = self.base_link + self.tvshow_link % (tvshowtitle, season, episode)
            return url
        except:
            return


    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url == None:
                return sources
            hostDict = hostprDict + hostDict
            page = getSum.get(url)
            match = getSum.findEm(page, '<td class="linkdom2"><span><a class="btn-xs" rel="nofollow" title="(.+?)" target="_blank" href="(.+?)"')
            if match:
                for hoster, url in match:
                    valid, host = source_utils.is_host_valid(hoster, hostDict)
                    if valid:
                        if source_utils.limit_hosts() is True and host in str(sources):
                            continue
                        sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        try:
            page2 = getSum.get(url)
            match2 = getSum.findEm(page2, '<a rel="external nofollow" href="/open/site/(.+?)"')
            if match2:
                for link in match2:
                    link = self.base_link + "/open/site/" + link
                    url = getSum.get(link, Type='redirect')
                    return url
        except:
            return url


