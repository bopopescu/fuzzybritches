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
		self.domains = ['hdm.to']
		self.base_link = 'https://hdm.to'
		self.search_link = '/search/%s+%s'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title).replace('-', '+').replace('++', '+')
			url = self.base_link + self.search_link % (title, year)
			r = client.request(url)
			u = client.parseDOM(r, "div", attrs={"class": "col-md-2 col-sm-2 mrgb"})
			for i in u:
				t = re.compile('<a href="(.+?)"').findall(i)
				for url in t:
					if not cleantitle.get(title) in cleantitle.get(url):
						continue
					return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			hostDict = hostDict + hostprDict
			sources = []

			if url is None:
				return sources

			t = client.request(url)

			r = re.compile('<iframe.+?src="(.+?)"').findall(t)

			for url in r:
				valid, host = source_utils.is_host_valid(url, hostDict)
				if valid:
					sources.append({'source': host, 'quality': 'HD', 'language': 'en', 'url': url, 'direct': False,
					                'debridonly': False})
			return sources
		except:
			return sources

	def resolve(self, url):
		return url
