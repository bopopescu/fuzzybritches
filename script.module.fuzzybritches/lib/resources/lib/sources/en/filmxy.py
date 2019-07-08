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

from resources.lib.modules import cleantitle, log_utils, source_utils, cfscrape


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.language = ['en']
        self.domains = ['filmxy.me', 'filmxy.one', 'filmxy.ws']
        self.base_link = 'https://filmxy.live'
        self.search_link = '/%s-%s'
        self.cfscraper = cfscrape.create_scraper()

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FilmXY - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None:
                return sources
            # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            result = self.cfscraper.get(url).content
            streams = re.compile('data-player="&lt;[A-Za-z]{6}\s[A-Za-z]{3}=&quot;(.+?)&quot;', re.DOTALL).findall(result)

            for link in streams:
                quality = source_utils.check_sd_url(link)
                host = link.split('//')[1].replace('www.', '')
                host = host.split('/')[0].lower()
                '''
                Now source_utils can't strip quality on some of these links. It will drop them
                down to SD. So i say we try this as most if not all links are HD
                '''
                if quality == 'SD':
                    sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})
                else:
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False, 'debridonly': False})

            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('FilmXY - Exception: \n' + str(failure))
            return sources

    def resolve(self, url):
        return url
