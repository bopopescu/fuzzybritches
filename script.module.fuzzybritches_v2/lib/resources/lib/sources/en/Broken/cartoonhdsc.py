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
from resources.lib.modules import more_sources
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['cartoonhd.sc', 'cartoonhd.to']
		self.base_link = 'https://www.cartoonhd.sc'
		self.search_link = '/?s=%s'
		self.scraper = cfscrape.create_scraper()

	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			searchName = cleantitle.getsearch(title)
			searchURL = self.base_link + self.search_link % (searchName.replace(':', ' ').replace(' ', '+'))
			searchPage = self.scraper.get(searchURL).content
			results = re.compile('<a href="(.+?)">(.+?)</a>.+?<span class="year">(.+?)</span>', re.DOTALL).findall(
				searchPage)
			for url, zName, zYear in results:
				if cleantitle.geturl(title).lower() in cleantitle.geturl(zName).lower():
					if year in str(zYear):
						url = url + "?watching"
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
			if url is None:
				return
			tvshowtitle = url
			url = self.base_link + '/episodes/%s-season-%s-episode-%s/?watching' % (tvshowtitle, season, episode)
			return url
		except:
			return

	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			if url is None:
				return sources
			hostDict = hostDict + hostprDict
			sourcePage = self.scraper.get(url).content
			links = re.compile('<iframe.+?src="(.+?)"', re.DOTALL).findall(sourcePage)
			for link in links:
				if "gomostream.com" in link:
					for source in more_sources.more_gomo(link, hostDict):
						sources.append(source)
				else:
					quality, info = source_utils.get_release_quality(link, link)
					valid, host = source_utils.is_host_valid(link, hostDict)
					sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': link, 'info': info,
					                'direct': False, 'debridonly': False})
			return sources
		except:
			return sources

	def resolve(self, url):
		return url
