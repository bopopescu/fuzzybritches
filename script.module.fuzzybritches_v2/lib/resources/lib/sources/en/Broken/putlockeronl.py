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

from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['putlocker.onl']
		self.base_link = 'http://ww0.putlocker.onl'
		self.tv_link = '/show/%s/season/%s/episode/%s'
		self.movie_link = '/movie/%s'
		self.scraper = cfscrape.create_scraper()

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			movietitle = cleantitle.geturl(title)
			url = self.base_link + self.movie_link % movietitle
			return url
		except:
			return

	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			tvshowtitle = cleantitle.geturl(tvshowtitle)
			url = tvshowtitle
			return url
		except:
			return

	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if not url:
				return
			tvshowtitle = url
			url = self.base_link + self.tv_link % (tvshowtitle, season, episode)
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []

			if url is None:
				return sources

			r = self.scraper.get(url).content

			try:
				match = re.compile('<IFRAME.+?SRC=.+?//(.+?)/(.+?)"').findall(r)
				for host, url in match:
					url = 'http://%s/%s' % (host, url)

					host = host.replace('www.', '')
					valid, host = source_utils.is_host_valid(host, hostDict)

					if source_utils.limit_hosts() is True and host in str(sources):
						continue

					if valid:
						sources.append({'source': host, 'quality': 'SD', 'language': 'en', 'url': url, 'direct': False,
						                'debridonly': False})
			except:
				return
		except Exception:
			return
		return sources

	def resolve(self, url):
		return url
