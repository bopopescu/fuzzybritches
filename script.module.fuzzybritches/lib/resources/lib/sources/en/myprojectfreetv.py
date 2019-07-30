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

from resources.lib.modules import cleantitle, client, log_utils, proxy


class source:
    def __init__(self):
        self.priority = 1
        self.source = ['www', www9]
        self.language = ['en']
        self.domains = ['my-project-free.tv', 'project-free-tv.ag']
        self.base_link = 'https://project-free-tv.ag'
        self.search_link = '/episode/%s-season-%s-episode-%s'

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        try:
            clean_title = cleantitle.geturl(tvshowtitle)
            url = clean_title
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MyProjectFreeTV - Exception: \n' + str(failure))
            return

    def episode(self, url, imdb, tvdb, title, premiered, season, episode):
        try:
            if not url:
                return
            tvshowtitle = url
            url = self.base_link + self.search_link % (tvshowtitle, int(season), int(episode))
            return url
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MyProjectFreeTV - Exception: \n' + str(failure))
            return

    def sources(self, url, hostDict, hostprDict):
        try:
            sources = []
            r = client.request(url)
            try:
                data = re.compile("callvalue\('.+?','.+?','(.+?)://(.+?)/(.+?)'\)", re.DOTALL).findall(r)
                for http, host, url in data:
                    url = '%s://%s/%s' % (http, host, url)
                    sources.append({
                        'source': host,
                        'quality': 'SD',
                        'language': 'en',
                        'url': url,
                        'direct': False,
                        'debridonly': False
                    })
            except Exception:
                pass
            return sources
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('MyProjectFreeTV - Exception: \n' + str(failure))
            return

    def resolve(self, url):
        return url
