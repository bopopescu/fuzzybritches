# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches
# Addon id: script.module.fuzzybritches
# Addon Provider: The Papaw

'''
Included with the Fuzzy Britches Add-on
'''


import re,urllib,urlparse

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser2

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['divxcrawler.tv']
        self.base_link = 'http://www.divxcrawler.club'
        self.search_link = '/latest.htm'
        self.search_link2 = '/streaming.htm'
        self.search_link3 = '/movies.htm'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            imdb = data['imdb']

            query = urlparse.urljoin(self.base_link, self.search_link)
            result = client.request(query)
            m = re.findall('Movie Size:(.+?)<.+?href="(.+?)".+?href="(.+?)"\s*onMouse', result, re.DOTALL|re.I)
            m = [(i[0], i[1], i[2]) for i in m if imdb in i[1]]
            if m:
                link = m
            else:
                query = urlparse.urljoin(self.base_link, self.search_link2)
                result = client.request(query)
                m = re.findall('Movie Size:(.+?)<.+?href="(.+?)".+?href="(.+?)"\s*onMouse', result, re.DOTALL|re.I)
                m = [(i[0], i[1], i[2]) for i in m if imdb in i[1]]
                if m:
                    link = m
                else:
                    query = urlparse.urljoin(self.base_link, self.search_link3)
                    result = client.request(query)
                    m = re.findall('Movie Size:(.+?)<.+?href="(.+?)".+?href="(.+?)"\s*onMouse', result, re.DOTALL|re.I)
                    m = [(i[0], i[1], i[2]) for i in m if imdb in i[1]]
                    if m: link = m

            for item in link:
                try:

                    quality, info = source_utils.get_release_quality(item[2], None)

                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+) (?:GB|GiB|MB|MiB))', item[0], flags=re.I)[-1]
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                        size = '%.2f GB' % size
                        info.append(size)
                    except:
                        pass

                    info = ' | '.join(info)

                    url = item[2]
                    if any(x in url.lower() for x in ['.rar.', '.zip.', '.iso.']) or any(
                            url.lower().endswith(x) for x in ['.rar', '.zip', '.iso']): raise Exception()

                    if any(x in url.lower() for x in ['youtube', 'sample', 'trailer']): raise Exception()
                    url = client.replaceHTMLCodes(url)
                    url = url.encode('utf-8')

                    sources.append({'source': 'DL', 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                    'direct': True, 'debridonly': False})
                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url


