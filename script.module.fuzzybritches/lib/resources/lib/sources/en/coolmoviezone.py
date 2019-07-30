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
import urlparse
import traceback

from resources.lib.modules import client, cleantitle, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.language = ['en']
        self.domains = ['coolmoviezone.online', 'coolmoviezone.co, 'coolmoviezone.io']
        self.base_link = 'https://www.coolmoviezone.io'
        self.search_link = '/%s-%s'
        # self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CoolMovieZone - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            r = client.request(url, headers=headers)
            match = re.compile('<td align="center"><strong><a href="(.+?)"').findall(r)
            for url in match:
                quality = source_utils.check_sd_url(url)
                valid, host = source_utils.is_host_valid(url, hostDict)
                sources.append({'source': host, 'quality': quality, 'language': 'en',
                                'url': url, 'direct': False, 'debridonly': False})
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('CoolMovieZone - Exception: \n' + str(failure))
            return
        return sources

    def resolve(self, url):
        return url
