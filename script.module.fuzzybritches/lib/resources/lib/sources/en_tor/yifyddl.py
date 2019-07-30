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

import re,urllib,urlparse

from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import log_utils
from resources.lib.modules import source_utils


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['yifyddl.movie']
        self.base_link = 'https://yifyddl.movie/'
        self.search_link = '/movie/%s'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except:
            failure = traceback.format_exc()
            log_utils.log('YIFYDLL - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None: return sources
            if debrid.status() is False: raise Exception()
            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            query = '%s %s' % (data['title'], data['year'])
            url = self.search_link % urllib.quote(query)
            url = urlparse.urljoin(self.base_link, url).replace('%20', '-')
            html = client.request(url)
            try:
                results = client.parseDOM(html, 'div', attrs={'class': 'ava1'})
            except:
                failure = traceback.format_exc()
                log_utils.log('YIFYDLL - Exception: \n' + str(failure))
                return sources
            for torrent in results:
                link = re.findall('a data-torrent-id=".+?" href="(magnet:.+?)" class=".+?" title="(.+?)"', torrent, re.DOTALL)
                for link, name in link:
                    link = str(client.replaceHTMLCodes(link).split('&tr')[0])
                    quality, info = source_utils.get_release_quality(name, name)
                    try:
                        size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GB|GiB|MB|MiB))', torrent)[-1]
                        div = 1 if size.endswith(('GB', 'GiB')) else 1024
                        size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                        size = '%.2f GB' % size
                        info.append(size)
                    except Exception:
                        pass
                    info = ' | '.join(info)
                    sources.append({'source': 'Torrent', 'quality': quality, 'language': 'en', 'url': link, 'info': info, 'direct': False, 'debridonly': True})

            return sources
        except:
            failure = traceback.format_exc()
            log_utils.log('YIFYDLL - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
