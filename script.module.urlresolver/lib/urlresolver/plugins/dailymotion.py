'''
plugin for URLResolver
Copyright (C) 2020 gujal

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''
import json
import re
from urlresolver import common
from lib import helpers
from urlresolver.resolver import UrlResolver, ResolverError


class DailymotionResolver(UrlResolver):
    name = 'dailymotion'
    domains = ['dailymotion.com']
    pattern = r'(?://|\.)(dailymotion\.com)/(?:video|embed|sequence|swf)(?:/video)?/([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()
        self.headers = {'User-Agent': common.RAND_UA,
                        'Origin': 'https://www.dailymotion.com',
                        'Referer': 'https://www.dailymotion.com/'}

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        js_result = json.loads(self.net.http_GET(web_url, headers=self.headers).content)

        if js_result.get('error'):
            raise ResolverError(js_result.get('error').get('title'))

        quals = js_result.get('qualities')
        if quals:
            mbtext = self.net.http_GET(quals.get('auto')[0].get('url'), headers=self.headers).content
            sources = re.findall('NAME="(?P<label>[^"]+)",PROGRESSIVE-URI="(?P<url>[^#]+)', mbtext)
            return helpers.pick_source(helpers.sort_sources_list(sources)) + helpers.append_headers(self.headers)
        raise ResolverError('No playable video found.')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://www.dailymotion.com/player/metadata/video/{media_id}')
