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

from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['coolmoviezone.xyz']
		self.base_link = 'https://coolmoviezone.xyz'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			mtitle = cleantitle.geturl(title)
			url = self.base_link + '/%s-%s' % (mtitle, year)
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			hostDict = hostprDict + hostDict
			r = client.request(url)
			match = re.compile('<td align="center"><strong><a href="(.+?)"').findall(r)
			for url in match:
				valid, host = source_utils.is_host_valid(url, hostDict)
				if valid:
					quality, info = source_utils.get_release_quality(url, url)
					sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
					                'direct': False, 'debridonly': False})
			return sources
		except Exception:
			return sources

	def resolve(self, url):
		return url
