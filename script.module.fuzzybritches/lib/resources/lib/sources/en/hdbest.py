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

import urllib, urlparse, re

from resources.lib.modules import client
from resources.lib.modules import dom_parser2 as dom
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['hdbest.net']
        self.base_link = 'http://hdbest.net'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except BaseException:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            imdb = data['imdb']

            url = urlparse.urljoin(self.base_link, 'player/play.php?imdb=%s' % imdb)
            data = client.request(url, referer=self.base_link)
            links = dom.parse_dom(data, 'jwplayer:source', req=['file', 'label'])
            for link in links:
                url = link.attrs['file']
                url = url.replace(' ', '%20') + '|User-Agent={0}&Referer={1}'.format(
                    urllib.quote(client.agent()), url)
                quality, info = source_utils.get_release_quality(link.attrs['label'])
                sources.append(
                    {'source': 'GVIDEO', 'quality': quality, 'language': 'en', 'url': url,
                     'direct': True, 'debridonly': False})

            return sources
        except BaseException:
            return sources

    def resolve(self, url):
        return url