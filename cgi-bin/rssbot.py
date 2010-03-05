#!/usr/bin/python
# -*- coding: utf-8 -*-
import feedparser, string, re, cgitb
cgitb.enable()

print("Content-Type: text/html\n")
########## TODO ########################################################
# add mailto links regex=(\w+@[a-zA-Z]{2,6})
#
########################################################################

FEEDS = ['https://username:password@twitter.com/statuses/friends_timeline/############.rss']
urlre = re.compile('http[s]?://[\S]+')
mailre = re.compile("[a-z,A-Z,.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,6}")

def rss(feeds):
   for i in feeds:
      f = feedparser.parse(i)
      e = f.entries
      try:
         print('<span id="ftitle"><b>'+f.feed.title +'</b></span><br/>')
      except:
         print('<span id="ftitle"><b>RSS Feeds</b></span><br/>')
      for o in e:
	 print('<div id="etitle">')
	 try:
            etitle = o.title+' '
         except:
            etitle = 'No Message'
	 urls = re.findall(urlre,etitle)
	 for u in urls:
	    try:
	       etitle = re.sub(re.escape(u),'<a id="inline" target="_blank" href="'+u+'">'+u+'</a>', etitle)
	    except:
	       continue
         mailtos = re.findall(mailre,etitle)
         for m in mailtos:
	    try:
	       etitle = re.sub(re.escape(m),'<a id="mailto" href="mailto:'+m+'">'+m+'</a>', etitle)
	    except:
	       continue
	 print(etitle.encode("utf-8"))
	 print(' <a href="'+o.link+'">link</a></div><br/>')

rss(FEEDS)
