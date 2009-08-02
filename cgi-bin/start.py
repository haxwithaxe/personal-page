#!/usr/bin/python
## Cookie Auth Script
import string, cgi, feedparser, datetime, cgitb
cgitb.enable()

KEY = '0' # Output od cmdline pi 42
START_SWITCH = '0'
WORK_SWITCH = '1'
START_TEMPLATE = open("start.tmpl", "r")
TMPL = START_TEMPLATE.read()
INNOVE_RSS = '<div id="innove-feed-control" style="color:#FFFFFF;font-size:14px;font-color:#000000;margin:10px;padding:4px;"><span style="color:#676767;font-size:14px;font-color:#000000;margin:10px;padding:4px;">Loading...</span></div>'
SEC_RSS = '<div id="sec-feed-control"><span style="color:#676767;font-size:14px;font-color:#000000;margin:10px;padding:4px;">Loading...</span></div>'
NOAUTH_STR = '<html><body><h1>It Works!</h1></body></html>'
AUTH_STR = '<html><head><title>Redirecting...</title><meta http-equiv="REFRESH" content="5;url=start.py?uchi='+KEY+'&sore='+START_SWITCH+'"/></head><body><h1>It Still Works!</h1></body></html>'
START_STR = TMPL.replace('<!--style-->','').replace('<!--links-->','').replace('<!--todo-->','<form action="todoput.py" method="POST" enctype="multipart/form-data"><input type="hidden" name="place" value="work"><input type=text name="ToDo" size="50"/><input type="submit" value="Post ToDo"/></form>').replace('<!--reminders-->','<form action="reminderput.py" method="POST" enctype="multipart/form-data"><input type=text name="reminder" size="50"/><input type="submit" value="Post Reminder"/></form>').replace('<!--dl_stats-->','') ##.replace('<!--rss-->', SEC_RSS)
WORK_STR = TMPL.replace('<!--style-->','').replace('<!--links-->','').replace('<!--todo-->','<form action="todoput.py" method="POST" enctype="multipart/form-data"><input type="hidden" name="place" value="work"><input type=text name="ToDo" size="50"/><input type="submit" value="Post ToDo"/></form>') ##.replace('<!--rss-->',INNOVE_RSS)
## FEEDS = ['http://feeds.feedburner.com/Twitter/MannkoepkeWithFriends?format=xml','http://feeds.feedburner.com/darknethackers?format=xml']

def todo():
   print()

def reminmind():
   print()

def main():
   try:
      auth_stat = cgi.parse()['uchi'][0]
   except:
      auth_stat = None

   try:
      o_stat = cgi.parse()['sore'][0]
   except:
      o_stat = None

   if str(o_stat) == WORK_SWITCH and str(auth_stat) == KEY:
      output = WORK_STR
   elif str(o_stat) == START_SWITCH and str(auth_stat) == KEY:
      output = START_STR
   elif str(auth_stat) == KEY:
      output = AUTH_STR
   else:
      output = NOAUTH_STR

   output = output.encode('utf-8')
   return output

print 'Content-Type: text/html\n'
print(main())
