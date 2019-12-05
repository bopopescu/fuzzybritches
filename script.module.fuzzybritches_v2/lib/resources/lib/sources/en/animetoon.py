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
		self.genre_filter = ['animation', 'anime']
		self.domains = ['animetoon.org', 'animetoon.tv']
		self.base_link = 'http://www.animetoon.org'
		self.scraper = cfscrape.create_scraper()

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = '%s-%s' % (title, year)
			url = self.base_link + '/' + url
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
			if not url:
				return
			if season == '1':
				url = self.base_link + '/' + url + '-episode-' + episode
			else:
				url = self.base_link + '/' + url + '-season-' + season + '-episode-' + episode
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		sources = []
		try:
			r = self.scraper.get(url).content
			match = re.compile('<div><iframe src="(.+?)"').findall(r)
			for url in match:
				host = url.split('//')[1].replace('www.', '')
				host = host.split('/')[0].split('.')[0].title()
				quality = source_utils.check_sd_url(url)
				r = self.scraper.get(url).content
				if 'http' in url:
					match = re.compile("url: '(.+?)',").findall(r)
				else:
					match = re.compile('file: "(.+?)",').findall(r)
				for url in match:
					sources.append(
						{'source': host, 'quality': quality, 'language': 'en', 'url': url, 'direct': False,
						 'debridonly': False})
		except:
			return
		return sources

	def resolve(self, url):
		return url
