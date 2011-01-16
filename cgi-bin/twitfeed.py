#!/usr/bin/python
# -*- coding: utf8 -*-

import twitter, sys, re, json

from twitter.oauth import OAuth

CACHE = u'/tmp/twitter.cache'

output = u'<span id="ftitle"><b>RSS Feeds</b></span><br/>'

urlre = re.compile('[a-zA-Z]+://[\S]+')

mailre = re.compile("[a-z,A-Z,.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,6}")

cred = open("/home/hax/haxwithaxe").read().split()

def stash_tweets(tweets):

	cache = open(CACHE,'w')

	cache.write(json.dumps(tweets))

	cache.close()

def unstash_tweeets():

	cache = open(CACHE,'r')

	tweets = json.loads(cache.read())

	cache.close()

	return tweets

try:

	twit = twitter.api.Twitter(auth=OAuth(cred[2],cred[3],cred[0],cred[1]))

except:

	output += u'<span class="error">Authentication Failure</span>'

try:

	feed = twit.statuses.friends_timeline()

	stash_tweets(feed)

except:

	#print(sys.exc_info())

	try:

		feed = unstash_tweets()

	except:

		feed = [{u'user': {u'screen_name': u'tweetypy'}, u'text': u'ut-oh! no feed'}]

for t in feed:

	tweet = t['text']

	urls = re.findall(urlre,tweet)

	for u in urls:

		try:

			tweet = re.sub(re.escape(u),u'<a id="inline" target="_blank" href="'+u+u'">'+u+u'</a>', tweet)

		except:

			continue

	mailtos = re.findall(mailre,tweet)

	for m in mailtos:

		try:

			tweet = re.sub(re.escape(m),'<a id="mailto" href="mailto:'+m+'">'+m+'</a>', tweet)

		except:

			continue

	tweet = tweet.encode('utf-8')

	output += u'<div id="etitle">'+t['user']['screen_name'].encode('utf-8')+u'&lt; '+tweet+u'</div>\n'

print(output)
