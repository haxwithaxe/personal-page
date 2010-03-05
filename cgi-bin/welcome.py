#!/usr/bin/python
## Cookie Auth Script
import string, cgi, feedparser, datetime, cgitb
cgitb.enable()

WELCOME_TMPL = open("welcome.tmpl", "r")
REDIR_TMPL = open("redirect.tmpl", "r")
WELCOME = WELCOME_TMPL.read()
REDIR = REDIR_TMPL.read()

try:
   is_start = cgi.parse()['uchi'][0]
except:
   is_start = 1

def main():
   output = WELCOME.replace('%URL%','/cgi-bin/welcome.py')
   if ( is_start == 0 ):
      output = REDIR.replace('%URL%','/cgi-bin/start.py?uchi=0&sore=0')
   output = output.encode('utf-8')
   return output

print 'Content-Type: text/html\n'
print(main())
