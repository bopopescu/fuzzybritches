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
		self.domains = ['hdpopcorns.eu']
		self.base_link = 'https://hdpopcorns.eu'

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = self.base_link + '/%s/' % title
			# https://hdpopcorns.eu/avengers-infinity-war/
			return url
		except:
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = cleantitle.geturl(tvshowtitle)
			return url
		except:
			return

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url: return
			tvshowtitle = url
			url = self.base_link + '/episode/%s-season-%s-episode-%s/' % (tvshowtitle, season, episode)
			# https://hdpopcorns.eu/episode/the-originals-season-1-episode-1/
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			r = client.request(url)
			try:
				match = re.compile('<iframe src=".+?//(.+?)/(.+?)"').findall(r)
				for host, url in match:
					url = 'https://%s/%s' % (host, url)
					quality = source_utils.check_url(url)
					host = host.replace('www.', '')
					valid, host = source_utils.is_host_valid(host, hostDict)
					if valid:
						sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url,
						                'direct': False, 'debridonly': False})
			except:
				return
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url