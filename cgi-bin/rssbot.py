#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

FEEDS = [
      ['http://feeds.feedburner.com/Twitter/MannkoepkeWithFriends?format=xml','twitter.xml'],
      ['http://feeds.feedburner.com/darknethackers?format=xml','darknet.xml'],
      ['http://www.google.com','work/innove.xml'],
      ['http://www.google.com','work/wps.xml']
      ]

def rss(feed):
   get_cmd = 'wget '+feed[0]+' -O /var/www/feeds/'+feed[1]
   if os.system(get_cmd):
      pass
   else:
      return 'GET_ERROR'

for i in FEEDS:
   rss(i)