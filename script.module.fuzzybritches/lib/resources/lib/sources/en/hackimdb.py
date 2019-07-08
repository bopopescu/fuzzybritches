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

from resources.lib.modules import cfscrape, client, log_utils, source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.language = ['en']
        self.domains = ['hackimdb.com']
        self.base_link = 'https://hackimdb.com'
        # this still works too '/title/&%s'
        self.search_link = '/title/%s'
        self.cfscraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('HackIMDB - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0'}
            r = self.cfscraper.get(url, headers=headers).content
            quality_bitches = re.compile('<strong>Quality:\s+</strong>\s+<span class="quality">(.+?)</span>', re.DOTALL).findall(r)

            for quality in quality_bitches:

                if 'HD' in quality:
                    quality = '720p'
                elif 'CAM' in quality:
                    quality = 'CAM'
                else:
                    quality = 'SD'

            match = re.compile('<iframe.+?src="(.+?)"').findall(r)
            for url in match:
                if 'youtube' in url:
                    continue
                valid, hoster = source_utils.is_host_valid(url, hostDict)
                if not valid:
                    continue
                sources.append({'source': hoster, 'quality': quality, 'language': 'en', 'url': url, 'direct': False, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('HackIMDB - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
