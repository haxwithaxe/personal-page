#!/usr/bin/python
# -*- coding: utf-8 -*-
import feedparser, string, cgitb
cgitb.enable()

FEEDS = ['http://mannkoepke:password@twitter.com/statuses/friends_timeline/15577540.rss']

def rss(feeds):
   r = ''
   for i in feeds:
      f = feedparser.parse(i)
      e = f.entries
      r += ('<span id=ftitle>'+f.feed.title +'</b><br/>')
      for o in e:
	 r += ('<span id=etitle>'+o.title+'</span><a href="'+o.link+'">link</a><br/>')
   return r

print("Content-Type: text/html\n")

print(rss(FEEDS).decode('utf-8', 'ignore'))
