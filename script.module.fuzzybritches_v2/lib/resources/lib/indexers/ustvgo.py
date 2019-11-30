# -*- coding: utf-8 -*-
# --[ USTVgo v1.5 ]--|--[ From JewBMX & Tempest ]--
# IPTV Indexer made just for the one site as of now.

import re, os, sys, urllib, traceback
from resources.lib.modules import client
from resources.lib.modules import control
from resources.lib.modules import log_utils


class ustvgo:
    def __init__(self):
        self.list = []
        self.base_link = 'http://ustvgo.tv/'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0', 'Referer': self.base_link}


    def root(self):
        channels = [
            ('ABC', 'abc-live-streaming-free', 'channels/ABC.png'),
            ('A&E', 'ae-networks-live-streaming-free', 'channels/A&E.png'),
            ('AMC', 'amc-live', 'channels/AMC.png'),
            ('Animal Planet', 'animal-planet-live', 'channels/Animalplanet.png'),
            ('BBC America', 'bbc-america-live', 'channels/BBC America.png'),
            ('BET', 'bet', 'channels/Bet.png'),
            ('Boomerang', 'boomerang', 'channels/Boomerang.png'),
            ('Bravo', 'bravo-channel-live-free', 'channels/Bravo.png'),
            ('Cartoon Network', 'cartoon-network-live-streaming-free', 'channels/Cartoon Network.png'),
            ('CBS', 'cbs-live-streaming-free', 'channels/CBS.png'),
            ('CMT', 'cmt', 'channels/CMT.png'),
            ('CNBC', 'cnbc-live-streaming-free', 'channels/CNBC.png'),
            ('CNN', 'cnn-live-streaming-free', 'channels/CNN.png'),
            ('Comedy Central', 'comedy-central-live-free', 'channels/Comedy Central.png'),
            ('Destination America', 'destination-america', 'channels/Destination America.png'),
            ('Discovery Channel', 'discovery-channel-live', 'channels/Discovery Channel.png'),
            ('Disney Channel', 'disney-channel-live-streaming-free', 'channels/Disney Channel.png'),
            ('Disney Jr', 'disneyjr', 'channels/Disney Junior.png'),
            ('Disney XD', 'disneyxd', 'channels/Disney XD.png'),
            ('DIY', 'diy', 'channels/DIY.png'),
            ('E', 'e', 'channels/E!.png'),
            ('ESPN', 'espn-live', 'channels/ESPN.png'),
            ('ESPN 2', 'espn2', 'channels/ESPN.png'),
            ('Food Network', 'food-network-live-free', 'channels/Food Network.png'),
            ('Fox Business', 'fox-business-live-streaming-free', 'channels/Fox Business.png'),
            ('Fox', 'fox-hd-live-streaming', 'channels/FOX.png'),
            ('Fox News', 'fox-news-live-streaming-free', 'channels/Fox_News_Channel.png'),
            ('Fox Sports 1', 'fox-sports-1', 'channels/Fox_Sports_1.png'),
            ('Fox Sports 2', 'fox-sports-2', 'channels/Fox_Sports_2.png'),
            ('FreeForm', 'freeform-channel-live-free', 'channels/Freeform.png'),
            ('FX', 'fx-channel-live', 'channels/FX.png'),
            ('FXM', 'fxm', 'channels/FXM.png'),
            ('FXX', 'fxx', 'channels/FXX.png'),
            ('Golf', 'golf-channel-live-free', 'channels/Golf.png'),
            ('GSN', 'gsn', 'channels/Game Show Network.png'),
            ('Halmark Channel', 'hallmark-channel-live-streaming-free', 'channels/Hallmark Channel.png'),
            ('Halmark Movies & Mysteries', 'hallmark-movies-mysteries-live-streaming-free', 'channels/Hallmark_Movies_Mysteries.png'),
            ('HBO', 'hbo', 'channels/HBO.png'),
            ('HGTV', 'hgtv-live-streaming-free', 'channels/HGTV.png'),
            ('History Channel', 'history-channel-live', 'channels/History.png'),
            ('HLN', 'hln', 'channels/HLN.png'),
            ('Investigation Discovery', 'investigation-discovery-live-streaming-free', 'channels/Investigation Discovery.png'),
            ('Lifetime Channel', 'lifetime-channel-live', 'channels/Lifetime.png'),
            ('Lifetime Movies', 'lifetime-movies', 'channels/Lifetime Networks.png'),
            ('MLB Network', 'mlb-network', 'channels/MLB Network.png'),
            ('MotorTrend', 'motortrend', 'channels/Motor_Trend.png'),
            ('MSNBC', 'msnbc-live-streaming-free', 'channels/MSNBC.png'),
            ('MTV', 'mtv', 'channels/MTV.png'),
            ('NAT GEO WILD', 'nat-geo-wild-live', 'channels/Nat Geo Wild.png'),
            ('National Geographic', 'national-geographic-live', 'channels/National Geographic.png'),
            ('NBA TV', 'nba-tv', 'channels/NBC.png'),
            ('NBC Sports', 'nbc-sports', 'channels/NBCSN.png'),
            ('NBC', 'nbc', 'channels/NBC.png'),
            ('NFL Network', 'nfl-network-live-free', 'channels/NFL_Network.png'),
            ('Nickelodeon', 'nickelodeon-live-streaming-free', 'channels/Nickelodeon.png'),
            ('NickToons', 'nicktoons', 'channels/NickToons.png'),
            ('One America News Network', 'one-america-news-network', 'channels/OANN.png'),
            ('OWN', 'own', 'channels/OWN.png'),
            ('Oxygen', 'oxygen', 'channels/Oxygen.png'),
            ('Paramont Network', 'paramount-network', 'channels/Paramount Network.png'),
            ('PBS', 'pbs-live', 'channels/PBS.png'),
            ('POP', 'pop', 'channels/Pop_Network.png'),
            ('Science', 'science', 'channels/Science Channel.png'),
            ('Showtime', 'showtime', 'channels/Showtime.png'),
            ('Starz', 'starz-channel-live', 'channels/Starz.png'),
            ('Sundance', 'sundance-tv', 'channels/SundanceTV.png'),
            ('SYFY', 'syfy-channel-live', 'channels/Syfy.png'),
            ('TBS', 'tbs-channel-live-free', 'channels/TBS.png'),
            ('TCM', 'tcm', 'channels/Turner Classic Movies (TCM).png'),
            ('Telemundo', 'telemundo', 'channels/Telemundo.png'),
            ('Tennis Channel', 'tennis-channel-live-free', 'channels/Tennis_Channel.png'),
            ('The CW', 'the-cw-live-streaming-free', 'channels/The CW.png'),
            ('The Weather Channel', 'the-weather-channel-live-streaming-free', 'channels/The_Weather_Channel.png'),
            ('TLC', 'tlc-live-free', 'channels/TLC.png'),
            ('TNT', 'tnt', 'channels/TNT.png'),
            ('Travel Channel', 'travel-channel-live-free', 'channels/Travel Channel.png'),
            ('TruTv', 'trutv', 'channels/truTV.png'),
            ('Tv Land', 'tv-land-live-free', 'channels/TV Land.png'),
            ('Univision', 'univision', 'channels/Univision.png'),
            ('USA Network', 'usa-network-live', 'channels/USA Network.png'),
            ('VH1', 'vh1', 'channels/VH1.png'),
            ('We Tv', 'we-tv', 'channels/We_TV.png'),
            ('WWE Network', 'wwe-network', 'channels/WWE_Network.png')
        ]
        for channel in channels:
            self.list.append({'name': channel[0], 'url': self.base_link + channel[1], 'image': channel[2], 'action': 'ustvgoPlay'})
        self.addDirectory(self.list)
        return self.list


    def play(self, url):
        try:
            #page = client.request(url, headers=self.headers)
            #url = re.compile('<iframe .+? src="(.+?)"', re.DOTALL).findall(page)[0]
            #url = "http:" + url if not url.startswith('http') else url
            stream = client.request(url, headers=self.headers)
            link = re.compile("file: '(.+?)',", re.DOTALL).findall(stream)[0]
            control.execute('PlayMedia(%s)' % link)
        except Exception:
            failure = traceback.format_exc()
            log_utils.log('---USTVgo - Exception: \n' + str(failure))
            return


    def addDirectory(self, items, queue=False, isFolder=True):
        if items is None or len(items) is 0:
            control.idle()
            sys.exit()
        sysaddon = sys.argv[0]
        syshandle = int(sys.argv[1])
        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()
        for i in items:
            try:
                name = i['name']
                if i['image'].startswith('http'):
                    thumb = i['image']
                elif artPath is not None:
                    thumb = os.path.join(artPath, i['image'])
                else:
                    thumb = addonThumb
                item = control.item(label=name)
                if isFolder:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % urllib.quote_plus(i['url'])
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'false')
                else:
                    url = '%s?action=%s' % (sysaddon, i['action'])
                    try:
                        url += '&url=%s' % i['url']
                    except Exception:
                        pass
                    item.setProperty('IsPlayable', 'true')
                    item.setInfo("mediatype", "video")
                    item.setInfo("audio", '')
                item.setArt({'icon': thumb, 'thumb': thumb})
                if addonFanart is not None:
                    item.setProperty('Fanart_Image', addonFanart)
                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=isFolder)
            except Exception:
                pass
        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)


