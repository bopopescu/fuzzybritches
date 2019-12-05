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
import urllib
import urlparse

from resources.lib.modules import cfscrape
from resources.lib.modules import cleantitle
from resources.lib.modules import client
from resources.lib.modules import debrid
from resources.lib.modules import source_utils


class source:
	def __init__(self):
		self.priority = 1
		self.language = ['en']
		self.domains = ['scene-rls.com', 'scene-rls.net']
		self.base_link = 'http://scene-rls.net'
		# self.search_link = '/search/%s'
		self.search_link = '/?s=%s'
		self.scraper = cfscrape.create_scraper()


	def movie(self, imdb, title, localtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'title': title, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return


	def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
		try:
			url = {'imdb': imdb, 'tvdb': tvdb, 'tvshowtitle': tvshowtitle, 'year': year}
			url = urllib.urlencode(url)
			return url
		except:
			return


	def episode(self, url, imdb, tvdb, title, premiered, season, episode):
		try:
			if url is None:
				return
			url = urlparse.parse_qs(url)
			url = dict([(i, url[i][0]) if url[i] else (i, '') for i in url])
			url['title'], url['premiered'], url['season'], url['episode'] = title, premiered, season, episode
			url = urllib.urlencode(url)
			return url
		except:
			return


	def sources(self, url, hostDict, hostprDict):
		try:
			sources = []

			if url is None:
				return sources

			if debrid.status() is False:
				return sources

			hostDict = hostprDict + hostDict

			data = urlparse.parse_qs(url)
			data = dict([(i, data[i][0]) if data[i] else (i, '') for i in data])

			title = data['tvshowtitle'] if 'tvshowtitle' in data else data['title']
			title = title.replace('&', 'and').replace('Special Victims Unit', 'SVU')

			hdlr = 'S%02dE%02d' % (int(data['season']), int(data['episode'])) if 'tvshowtitle' in data else data['year']

			query = '%s %s' % (title, hdlr)
			query = re.sub('(\\\|/| -|:|;|\*|\?|"|\'|<|>|\|)', '', query)

			try:
				url = self.search_link % urllib.quote_plus(query)
				url = urlparse.urljoin(self.base_link, url)
				# log_utils.log('url = %s' % url, log_utils.LOGDEBUG)

				r = self.scraper.get(url).content

				posts = client.parseDOM(r, 'div', attrs={'class': 'post'})

				items = [];
				dupes = []

				for post in posts:
					try:
						u = client.parseDOM(post, "div", attrs={"class": "postContent"})
						u = client.parseDOM(u, "h2")
						u = client.parseDOM(u, 'a', ret='href')
						u = [(i.strip('/').split('/')[-1], i) for i in u]
						items += u
					except:
						source_utils.scraper_error('SCENERLS')
						pass

			except:
				source_utils.scraper_error('SCENERLS')
				pass

			for item in items:
				try:
					name = item[0]
					name = client.replaceHTMLCodes(name)

					t = name.split(hdlr)[0].replace(data['year'], '').replace('(', '').replace(')', '').replace('&', 'and')
					if cleantitle.get(t) != cleantitle.get(title):
						continue

					tit = name.replace('.', ' ')

					if hdlr not in tit:
						continue

					quality, info = source_utils.get_release_quality(name, item[1])
					info = ' | '.join(info)

					url = item[1]

					if any(x in url for x in ['.rar', '.zip', '.iso']):
						continue

					url = client.replaceHTMLCodes(url)
					url = url.encode('utf-8')

					host = re.findall('([\w]+[.][\w]+)$', urlparse.urlparse(url.strip().lower()).netloc)[0]

					if not host in hostDict:
						continue

					host = client.replaceHTMLCodes(host)
					host = host.encode('utf-8')

					sources.append({'source': host, 'quality': quality, 'language': 'en', 'url': url, 'info': info,
									'direct': False, 'debridonly': True})
				except:
					source_utils.scraper_error('SCENERLS')
					pass

			return sources

		except:
			source_utils.scraper_error('SCENERLS')
			return sources


	def resolve(self, url):
		return url
