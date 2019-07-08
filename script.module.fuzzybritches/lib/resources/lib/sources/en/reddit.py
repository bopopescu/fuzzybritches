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
import traceback

from resources.lib.modules import cleantitle, client, log_utils


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www']
        self.language = ['en']
        self.domains = ['reddit.com']
        self.base_link = 'https://www.reddit.com/user/nbatman/m/streaming2/search?q=%s&restrict_sr=on'

    def movie(self, imdb, title, localtitle, aliases, year):
        try:
            title = cleantitle.geturl(title)
            title = title.replace('-', '+')
            query = '%s+%s' % (title, year)
            url = self.base_link % query
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Reddit - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                match = re.compile(
                    'class="search-title may-blank" >(.+?)</a>.+?<span class="search-result-icon search-result-icon-external"></span><a href="(.+?)://(.+?)/(.+?)" class="search-link may-blank" >').findall(r)
                for info, http, host, ext in match:
                    if '2160' in info:
                        quality = '4K'
                    elif '1080' in info:
                        quality = '1080p'
                    elif '720' in info:
                        quality = 'HD'
                    elif '480' in info:
                        quality = 'SD'
                    else:
                        quality = 'SD'

                    url = '%s://%s/%s' % (http, host, ext)
                    if 'google' in host:
                        host = 'GDrive'
                    if 'Google' in host:
                        host = 'GDrive'
                    if 'GOOGLE' in host:
                        host = 'GDrive'

                    sources.append({
                        'source': host,
                        'quality': quality,
                        'language': 'en',
                        'url': url,
                        'info': info,
                        'direct': False,
                        'debridonly': False
                    })
            except Exception:
                failure = traceback.format_exc()
                log_utils.log('Reddit - Exception: \n' + str(failure))
                return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('Reddit - Exception: \n' + str(failure))
            return sources
        return sources

    def resolve(self, url):
        return url
