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

from resources.lib.modules import client, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www', 'www6', 'www7']
        self.language = ['en']
        self.domains = ['putlockerr.is', 'putlockers.movie']
        self.base_link = 'https://putlockerr.is'
        self.search_link = '/embed/%s/'
        # self.scraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = self.base_link + self.search_link % imdb
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            url = url + '/%s-%s/' % (season, episode)
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            r = client.request(url, headers=headers)
            try:
                match = re.compile('<iframe src="(.+?)://(.+?)/(.+?)"').findall(r)
                for http, host, url in match:
                    url = '%s://%s/%s' % (http, host, url)
                    sources.append({'source': host, 'quality': 'HD', 'language': 'en',
                                    'url': url, 'direct': False, 'debridonly': False})
            except Exception:
                return
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Putlocker - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url
