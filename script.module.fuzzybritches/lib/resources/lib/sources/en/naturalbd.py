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


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.language = ['en']
        self.domains = ['naturalbd.com']
        self.base_link = 'http://naturalbd.com'
        self.search_link = 'http://naturalbd.com/msearch.php'

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
            if url is None: return
            url = urlparse.parse_qs(url)
            url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
            url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
            url = urllib.urlencode(url)
            return url
        except Exception:
            return

    def sources(self, url, hostDict, hostprDict):
        sources = []
        try:
            if url is None:
                return sources

            data = urlparse.parse_qs(url)
            data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])
            title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
            imdb = data['imdb']

            if not 'tvshowtitle' in data:
                url = urlparse.urljoin(self.base_link, 'movie.php?imdbid=%s' % imdb)
                data = client.request(url, referer=self.base_link)
                links = client.parseDOM(data, 'source', ret='src')
            else:
                tm_api = '9c61dcfae7065994ce1008535ece53eb'
                tm_url = 'http://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id' % (imdb, tm_api)
                tm_id = client.request(tm_url)
                import json
                tm_id = json.loads(tm_id)['tv_results'][0]['id']
                tm_eplink = 'https://api.themoviedb.org/3/tv/%d/season/%d/episode/%d?api_key=%s' %\
                            (int(tm_id), int(data['season']), int(data['episode']), tm_api)
                tm_epiid = client.request(tm_eplink)
                tm_epiid = json.loads(tm_epiid)['id']
                url = urlparse.urljoin(self.base_link, 'single-episode.php?epiid=%s&tvid=%s' % (tm_epiid, tm_id))
                data = client.request(url, referer=self.base_link)
                links = client.parseDOM(data, 'source', ret='src')

            for link in links:
                link = link.replace('/playlist.m3u8', '')
                link = 'http:{0}'.format(link) if link.startswith('//') else link
                link = urllib.quote(link, ':/_+!@#$%^&*-')
                link = link.replace(' ', '%20') + '|User-Agent={0}&Referer={1}'.format(
                    urllib.quote(client.agent()), url)

                sources.append(
                    {'source': 'DL', 'quality': '720p', 'language': 'en', 'url': link,
                     'direct': True, 'debridonly': False})

            return sources
        except Exception:
            return sources

    def resolve(self, url):
        return url