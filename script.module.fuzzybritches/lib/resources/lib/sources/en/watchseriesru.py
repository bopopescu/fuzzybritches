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
import traceback
import urlparse

from resources.lib.modules import cleantitle, client, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watch-series.live']
        self.base_link = 'https://www2.watch-series.live'
        self.search_link = '/series/%s-season-%s-episode-%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = cleantitle.geturl(tvshowtitle)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchSeriesRU - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowtitle = url
            url = self.base_link + self.search_link % (tvshowtitle, season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchSeriesRU - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            r = client.request(url, headers=headers)
            match = re.compile('data-video="(.+?)">').findall(r)
            for url in match:
                if 'vidcloud' in url:
                    url = urlparse.urljoin('https:', url)
                    r = client.request(url, headers=headers)
                    regex = re.compile("file: '(.+?)'").findall(r)
                    for direct_links in regex:
                        sources.append({'source': 'cdn', 'quality': 'SD', 'language': 'en', 'url': direct_links, 'direct': False, 'debridonly': False})

                else:
                    valid, host = source_utils.is_host_valid(url, hostDict)
                    sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('WatchSeriesRU - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
