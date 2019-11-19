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

import urllib, urlparse, re

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils
from resources.lib.modules import cfscrape
from resources.lib.modules import directstream

class source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['watchhdmovie.net']
        self.base_link = 'https://watch32hd.org/'
        self.search_link = 'results?q=%s'

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

            title = data['title']
            hdlr = data['year']
            query = '%s %s' % (title, hdlr)
            query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', ' ', query)

            url = urlparse.urljoin(self.base_link, self.search_link % urllib.quote_plus(query))
            r = client.request(url)
            items = client.parseDOM(r, 'div', attrs={'class': 'cell_container'})

            for item in items:
                try:
                    name = client.parseDOM(item, 'a', ret='title')[0]
                    name = client.replaceHTMLCodes(name)
                    t = re.sub('(\.|\(|\[|\s)(\d{4}|S\d+E\d+|S\d+|3D)(\.|\)|\]|\s|)(.+|)', '', name)
                    if not cleantitle.get(t) == cleantitle.get(title):
                        raise Exception()

                    y = re.findall('[\.|\(|\[|\s](\d{4})[\.|\)|\]|\s]', name)[-1]
                    if not y == hdlr:
                        raise Exception()

                    link = client.parseDOM(item, 'a', ret='href')[0]
                    link = urlparse.urljoin(self.base_link, link) if link.startswith('/') else link
                except:
                    return sources
                try:
                    r = client.request(link)
                    url = re.findall('''frame_url\s*=\s*['"](.+?)['"]\;''', r, re.DOTALL)[0]
                    url = url if url.startswith('http') else urlparse.urljoin('https://', url)

                    if 'vidlink' in url:
                        ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:14.0) Gecko/20100101 Firefox/14.0.1'}
                        html = client.request(url, headers=ua)
                        postID = re.findall("postID\s*=\s*'([^']+)", html)[0]
                        data = {'postID': postID}

                        rid = client.request('https://vidlink.org/embed/update_views', post=data, headers=ua,
                                             referer=url)
                        from resources.lib.modules import jsunpack
                        rid = jsunpack.unpack(rid)
                        playlist = re.findall('''file1=['"](.+?)['"];''', rid)[0]
                        links = client.request(playlist, headers=ua, referer=url)

                        try:
                            sub = re.findall('''URI="/sub/vtt/(\d+)/sub.m3u8",LANGUAGE="el"''', links)[0]
                        except IndexError:
                            sub = re.findall('''URI="/sub/vtt/(\d+)/sub.m3u8",LANGUAGE="en"''', links)[0]
                        sub = 'https://opensubtitles.co/sub/{0}.vtt'.format(sub)

                        pattern = 'RESOLUTION=\d+x(\d{3,4}),SUBTITLES="subs"\s*(/drive.+?.m3u8)'
                        links = re.findall(pattern, links)
                        for quality, link in links:
                            quality = source_utils.get_release_quality(quality, quality)[0]
                            link = 'https://p2p.vidlink.org/' + link.replace('/drive//hls/', 'drive/hls/')
                            sources.append({'source': 'GVIDEO', 'quality': quality, 'language': 'en', 'url': link,
                                            'sub': sub, 'direct': True, 'debridonly': False})

                except:
                    pass

            return sources
        except:
            return sources

    def resolve(self, url):
        return url
