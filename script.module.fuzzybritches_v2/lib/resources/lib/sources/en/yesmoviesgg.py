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
        self.domains = ['yesmovies.fm', 'yesmovies.gg']
        self.base_link = 'https://www6.yesmovies.fm'
        self.movie_link = '/film/%s/watching.html?ep=0'
        self.tvshow_link = '/film/%s-season-%s/watching.html?ep=%s'


    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title).replace('--', '-')
            url = self.base_link + self.movie_link % title
            return url
        except:
            return


    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle).replace('--', '-')
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
            r = getSum.get(url)
            qual = getSum.findThat(r, 'class="quality">(.+?)<')[0]
            quality, info = source_utils.get_release_quality(qual, qual)
            match = getSum.findSum(r)
            for url in match:
                if 'vidcloud' in url:
                    r = getSum.get(url)
                    match = getSum.findSum(r)
                    for url in match:
                        valid, host = source_utils.is_host_valid(url, hostDict)
                        if valid:
                            sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
                else:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    if valid:
                        sources.append({'source': host, 'quality': quality, 'language': 'en', 'info': info, 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except:
            return sources


    def resolve(self, url):
        if 'api.vidnode.net' in url:
            url = getSum.get(url, type='redirect')
        return url


