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

import re, urllib, urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import dom_parser2 as dom
from resources.lib.modules import client
from resources.lib.modules import source_utils

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['iwaatch.com']
        self.base_link = 'https://iwaatch.com/'
        self.search_link = 'api/api.php?page=moviesearch&q={0}'

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
            if not url: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['title']
            year = data['year']
            t = title + year

            query = '%s' % data['title']
            query = re.sub(r'(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = self.search_link.format(urllib.quote_plus(query))
            url = urlparse.urljoin(self.base_link, url)

            r = client.request(url)
            items = client.parseDOM(r, 'li')
            items = [(dom.parse_dom(i, 'a', req='href')[0]) for i in items if year in i]
            items = [(i.attrs['href'], re.sub('<.+?>|\n', '', i.content).strip()) for i in items]
            item = [i[0].replace('movie', 'view') for i in items if cleantitle.get(t) == cleantitle.get(i[1])][0]

            html = client.request(item)
            streams = re.findall('sources\:\s*\[(.+?)\]\,', html, re.DOTALL)[0]
            streams = re.findall('file:\s*[\'"](.+?)[\'"].+?label:\s*[\'"](.+?)[\'"]', streams, re.DOTALL)

            for link, label in streams:
                quality = source_utils.get_release_quality(label, label)[0]
                link += '|User-Agent=%s&Referer=%s' % (urllib.quote(client.agent()), item)
                sources.append({'source': 'Direct', 'quality': quality, 'language': 'en', 'url': link,
                                'direct': True, 'debridonly': False})

            return sources
        except BaseException:
            return sources

    def resolve(self, url):
        return url

