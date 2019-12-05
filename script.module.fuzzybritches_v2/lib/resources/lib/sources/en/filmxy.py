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

import re
import urlparse

from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['filmxy.nl', 'filmxy.me', 'filmxy.one', 'filmxy.ws']
		self.base_link = 'https://www.filmxy.nl'
		self.search_link = '/%s-%s'
		self.scraper = cfscrape.create_scraper()

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = urlparse.urljoin(self.base_link, (self.search_link % (title, year)))
			return url
		except Exception:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []

			if url is None:
				return sources
			headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:65.0) Gecko/20100101 Firefox/65.0'}
			result = self.scraper.get(url, headers=headers).content
			streams = re.compile('data-player="&lt;[A-Za-z]{6}\s[A-Za-z]{3}=&quot;(.+?)&quot;', re.DOTALL).findall(
				result)

			for link in streams:
				quality = source_utils.check_sd_url(link)
				host = link.split('//')[1].replace('www.', '')
				host = host.split('/')[0].lower()

				if quality == 'SD':
					sources.append({'source': host, 'quality': '720p', 'language': 'en', 'url': link, 'direct': False,
					                'debridonly': False})
				else:
					sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'direct': False,
					                'debridonly': False})

			return sources
		except Exception:
			return sources

	def resolve(self, url):
		return url
