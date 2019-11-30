# -*- coding: utf-8 -*-
###############################################################################
#                           "A BEER-WARE LICENSE"                             #
# ----------------------------------------------------------------------------#
# Feel free to do whatever you wish with this file. Since we most likey will  #
# never meet, buy a stranger a beer. Give credit to ALL named, unnamed, past, #
# present and future dev's of this & files like this. -Share the Knowledge!   #
###############################################################################

# Addon Name: Fuzzy Britches v2
# Addon id: script.module.fuzzybritches_v2
# Addon Provider: The Papaw

import urllib
import urlparse

from resources.lib.modules import cfscrape
from resources.lib.modules import client


class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['naturalbd.com']
        self.base_link = 'http://naturalbd.com'
        self.search_link = 'http://naturalbd.com/rpc.php'
        self.scraper = cfscrape.create_scraper()

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
                data = self.scraper(url, referer=self.base_link).content
                links = client.parseDOM(data, 'source', ret='src')
            else:
                tm_api = '9c61dcfae7065994ce1008535ece53eb'
                tm_url = 'http://api.themoviedb.org/3/find/%s?api_key=%s&external_source=imdb_id' % (imdb, tm_api)
                tm_id = self.scraper.get(tm_url).content
                import json
                tm_id = json.loads(tm_id)['tv_results'][0]['id']
                tm_eplink = 'https://api.themoviedb.org/3/tv/%d/season/%d/episode/%d?api_key=%s' % \
                            (int(tm_id), int(data['season']), int(data['episode']), tm_api)
                tm_epiid = self.scraper.get(tm_eplink).content
                tm_epiid = json.loads(tm_epiid)['id']
                url = urlparse.urljoin(self.base_link, 'single-episode.php?epiid=%s&tvid=%s' % (tm_epiid, tm_id))
                data = self.scraper.get(url, referer=self.base_link).content
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
