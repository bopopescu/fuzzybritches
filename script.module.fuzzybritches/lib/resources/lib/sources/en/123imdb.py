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
import requests
import traceback

from resources.lib.modules import cleantitle, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.language = ['en']
        self.domains = ['123imdb.to']
        self.base_link = 'https://123imdb.to'
        self.search_link = '/movie/%s-%s/'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('123IMDB - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            if url is None:
                return sources
            hostDict = hostprDict + hostDict
            '''
            Sometimes this source url will have extra characters after /movie/%s-%s/.
            Site will automatically forward us to the correct page for the movie. So
            using title-year in the url string works everytime.
            '''
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
            '''
            However we will need to capture that redirect before joining the end of
            the url.
            '''
            r = requests.get(url, headers=headers).url
            url = urlparse.urljoin(r, 'watching/?ep=1')

            r = requests.get(url, headers=headers).content

            quality_scrape = re.compile('<span class="quality"><a href=.+?rel="tag">(.+?)</a>', re.DOTALL).findall(r)

            if 'HD' in quality_scrape:
                quality = '720p'
            elif 'CAM' in quality_scrape:
                quality = 'CAM'
            else:
                quality = 'SD'

            # We pull the only playable link
            movie_scrape = re.compile('<a title=.+?data-svv1="(.+?)"', re.DOTALL).findall(r)[0]

            host = movie_scrape.split('//')[1].replace('www.', '')
            host = host.split('/')[0].split('.')[0].title()
            sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': movie_scrape, 'direct': False, 'debridonly': False})
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('123IMDB - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
