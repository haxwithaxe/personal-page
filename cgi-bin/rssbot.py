#!/usr/bin/python
# -*- coding: utf-8 -*-
import feedparser, string, re, cgitb
cgitb.enable()

print("Content-Type: text/html\n")


FEEDS = ['http://mannkoepke:passwd@twitter.com/statuses/friends_timeline/15577540.rss']
urlre = re.compile('http://.*\.[a-z,A-Z]*.[a-z,A-Z,0-9]*[^\s ]')


def rss(feeds):
   for i in feeds:
      f = feedparser.parse(i)
      e = f.entries
      print('<span id="ftitle"><b>'+f.feed.title +'</b></span><br/>')
      for o in e:
	 print('<div id="etitle">')
	 etitle = o.title+' '
	 urls = re.findall(urlre,etitle)
	 for u in urls:
	    try:
	       etitle = re.sub(u,'<a id="inline" target="_blank" href="'+u+'">'+u+'</a>', etitle)
	    except:
	       continue
	 print(etitle.encode("utf-8"))
	 print(' <a href="'+o.link+'">link</a></div><br/>')

rss(FEEDS)
