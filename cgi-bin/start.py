#!/usr/bin/python
## Cookie Auth Script
import xml.dom.minidom, string, cgi, os, re, feedparser, datetime, cgitb
cgitb.enable()

KEY = '0' # Output of cmdline pi 42
DEMO_SWITCH = 'demo'
START_SWITCH = '0'
WORK_SWITCH = '1'
START_TEMPLATE = open("start.tmpl", "r")
TMPL = START_TEMPLATE.read()

MONO_TEMPLATE = open("mono.tmpl", "r")
MONO_TMPL = MONO_TEMPLATE.read()

welcomRedir = '<html><head><meta http-equiv="refresh" content="0;url=welcome.py"></head><body>&nbsp;</body></html>'

rssFrameStr = '<td align="left" valign="top"><h5>RSS</h5><div id="allrssdiv" class="frame">&nbsp;</div></td>'

RSS = '<div id="feed-control-%N%"><span style="color:#676767;font-size:14px;font-color:#000000;margin:10px;padding:4px;">Loading...</span></div>'

STYLE = 'koepkes-style.css'

args = cgi.parse()

def links(f):
   output = ''
   for i in links:
      output += '<p><a target="_blank" href="'+i["url"]+'">'+i["name"]+'</a></p>'
   return output

def style(css_file):
   CSS_DOC = open(css_file, "r")
   CSS = CSS_DOC.read()
   return CSS

def determineAuth():
   return KEY

def get_user_data(uid):
   userDataArray = json.loads(open('/var/www/user-data/'+uid).read())
   return userDataArray


def main():
   output = ''
   urlVals = {}
   try:
      auth_stat = args['uchi'][0]
      urlVals['uchi'] = auth_stat
      user = get_user_data(auth_stat)
   except:
      auth_stat = None

   try:
      o_stat = args['sore'][0]
      urlVals['sore'] = o_stat
   except:
      o_stat = None

   try:
      koko_stat = args['koko'][0]
      urlVals['koko'] = koko_stat
   except:
      koko_stat = 'main'
      urlVals['koko'] = koko_stat

   try:
      output = TMPL.replace('<!--style-->',style(user['css'])).replace('<!--links-->',links(user['links'])).replace('<!--RSS-->',feeds(user['feeds']))
   except:
      output = welcomeRedir

   output = output.encode('utf-8')
   return output

print 'Content-Type: text/html\n'
# print(cgi.parse())
print(main())
