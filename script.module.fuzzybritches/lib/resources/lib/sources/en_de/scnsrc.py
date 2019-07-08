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
import urllib
import urlparse
import requests

from resources.lib.modules import cleantitle, client, debrid, dom_parser2, log_utils, source_utils, workers


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['scnsrc.me']
        self.base_link = 'https://www.scnsrc.me'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'title': title, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if url is None:
                return

            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            self._sources = []
            if url is None:
                return self._sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

            query = '%s S%02dE%02d' % (
                data['tvshowtitle'],
                int(data['season']),
                int(data['episode'])) if 'tvshowtitle' in data else '%s %s' % (
                data['title'],
                data['year'])
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            query = cleantitle.geturl(query)
            url = urlparse.urljoin(self.base_link, query)
            shell = requests.Session()

            headers = {
                'Referer': url,
                'User-Agent':
                'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            r = scraper.get(url, headers=headers)
            r = r.headers['Location']
            r = scraper.get(r).content
            posts = dom_parser2.parse_dom(r, 'li', {'class': re.compile('.+?'), 'id': re.compile('comment-.+?')})
            self.hostDict = hostDict + hostprDict
            threads = []

            for i in posts:
                threads.append(workers.Thread(self._get_sources, i.content))
            [i.start() for i in threads]
            [i.join() for i in threads]

            return self._sources
        except Exception:
            return self._sources

    def _get_sources(self, item):
        try:
            links = dom_parser2.parse_dom(item, 'a', req='href')
            links = [i.attrs['href'] for i in links]
            info = []
            try:
                size = re.findall('((?:\d+\.\d+|\d+\,\d+|\d+)\s*(?:GiB|MiB|GB|MB))', item)[0]
                div = 1 if size.endswith('GB') else 1024
                size = float(re.sub('[^0-9|/.|/,]', '', size)) / div
                size = '%.2f GB' % size
                info.append(size)
            except Exception:
                pass
            info = ' | '.join(info)
            for url in links:
                if 'youtube' in url:
                    continue
                if any(x in url for x in ['.rar.', '.zip.', '.iso.']) or any(
                        url.endswith(x) for x in ['.rar', '.zip', '.iso']):
                            raise Exception()
                valid, host = source_utils.is_host_valid(url, self.hostDict)
                if not valid:
                    continue
                host = client.replaceHTMLCodes(host)
                host = host.encode('utf-8')
                quality, info2 = source_utils.get_release_quality(url, url)
                if url in str(self._sources):
                    continue
                self._sources.append(
                    {'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info, 'direct': False,
                     'debridonly': debrid.status()})
        except Exception:
            pass

    def resolve(self, url):
        return url
