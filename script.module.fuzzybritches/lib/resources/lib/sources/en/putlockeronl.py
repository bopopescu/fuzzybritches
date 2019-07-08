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

import re,urllib,urlparse
from resources.lib.modules import cleantitle,client,cfscrape,proxy


class source:
	def __init__(self):
		self.priority = 1
        self.source = ['ww', 'www']
		self.language = ['en']
		self.domains = ['putlocker.onl']
		self.base_link = 'http://putlocker.onl'
		self.tv_link = '/show/%s/season/%s/episode/%s'
		self.movie_link = '/movie/%s'
		self.scraper = cfscrape.create_scraper()


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			title = cleantitle.geturl(title)
			url = self.base_link + self.movie_link % title
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
			if not url: return
			tvshowtitle = url
			url = self.base_link + self.tv_link % (tvshowtitle,season,episode)
			return url
		except:
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []
			r = self.scraper.get(url).content
			try:
				match = re.compile('<IFRAME.+?SRC=.+?//(.+?)/(.+?)"').findall(r)
				for host,url in match: 
					url = 'http://%s/%s' % (host,url)
					host = host.replace('www.','')
					sources.append({
						'source': host,
						'quality': 'SD',
						'language': 'en',
						'url': url,
						'direct': False,
						'debridonly': False
					})
			except:
				return
		except Exception:
			return
		return sources


	def resolve(self, url):
		return url

