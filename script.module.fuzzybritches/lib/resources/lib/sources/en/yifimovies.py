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
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import dom_parser2


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.language = ['en']
        self.domains = ['yifymovies.org']
        self.base_link = 'https://yifymovies.org'
        self.search_link = '/search/%s/feed/rss2/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year, 'aliases': aliases}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def searchMovie(self, title, year):
        try:
            query = self.search_link % urllib.quote_plus(cleantitle.getsearch(title))
            url = urlparse.urljoin(self.base_link, query)
            r = client.request(url)
            r = client.parseDOM(r, 'item')
            r = [(client.parseDOM(i, 'title')[0], client.parseDOM(i, 'link')[0]) for i in r if i]
            r = [i[1] for i in r if cleantitle.get(title) == cleantitle.get(i[0])]
            return r[0]
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []

            if url is None: return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            url = self.searchMovie(data['title'], data['year'])
            if url is None: return sources
            
            r = client.request(url)
            data = client.parseDOM(r, 'div', attrs={'class': 'playex'})[0]
            frames = client.parseDOM(data, 'iframe', ret='src')
            frames += re.compile('''<iframe\s*src=['"](.+?)['"]''', re.DOTALL).findall(data)
            quality = client.parseDOM(r, 'span', attrs={'class': 'qualityx'})[0]
            for frame in frames:
                url = frame.split('=')[1] if frame.startswith('<') else frame
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                valid, host = source_utils.is_host_valid(url, hostDict)

                if valid:
                    quality, info = source_utils.get_release_quality(quality, url)
                    info = ' | '.join(info)
                    sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
                                    'direct': False, 'debridonly': False})

                elif url.endswith('mp4'):
                    url += '|User-Agent=%s' % urllib.quote_plus(client.agent())
                    sources.append({'source': 'MP4', 'quality': quality, 'language': 'en', 'url': url,
                                    'direct': True, 'debridonly': False})

                elif 'mystream' in url:
                    data = client.request(url)
                    links = dom_parser2.parse_dom(data, 'source', req=['src', 'label'])
                    for link in links:
                        label = link.attrs['label']
                        url = link.attrs['src'] + '|User-Agent=%s' % urllib.quote_plus(client.agent())

                        sources.append({'source': 'MYSTREAM', 'quality': label, 'language': 'en', 'url': url,
                                        'direct': True, 'debridonly': False})

                else:
                    continue
            return sources
        except Exception:
            return sources

    def resolve(self, url):
        try:
            if not '|Us' in url:
                return client.request(url, output='geturl')
        except Exception:
            return url