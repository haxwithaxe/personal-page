#!/usr/bin/python
# -*- coding: utf-8 -*-
import feedparser, string, cgitb
cgitb.enable()

FEEDS = ['http://feeds.feedburner.com/Twitter/MannkoepkeWithFriends?format=xml','http://feeds.feedburner.com/darknethackers?format=xml']

def rss(feeds):
   r = ''
   for i in feeds:
      f = feedparser.parse(i)
      e = f.entries
      r += '<div id=rssbox>'
      r += ('<span id=ftitle>'+f.feed.title +'</b><br/>')
      for o in e:
	 r += ('<span id=etitle>'+o.title+'</span><a href="'+o.link+'">link</a><br/>')
   r += '</div>'
   return r

rssOut = "document.write('%s');" % rss(FEEDS)

print("Content-Type: text/html\n")


print(rssOut.decode('utf-8', 'ignore'))
