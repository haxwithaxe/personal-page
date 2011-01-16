#!/usr/bin/python
# index script will determine permissions to view subsequent pages
# and redirect to the appropriate page.
import cgi

TMPL_DIR = '../tmpl/'

CONTENT_DIR = '../content/'

tmpl = 'Content-Type: text/html\n\n\n'+open(TMPL_DIR+'page','r').read()

lsidebar = open(TMPL_DIR+'lsidebar','r').read()

rsidebar = open(TMPL_DIR+'rsidebar','r').read()

footer = open(TMPL_DIR+'footer','r').read()

form = cgi.FieldStorage()

if form.has_key('q'):

	page = form['q'].value

else:

	page = 'home'

content = open(CONTENT_DIR+page,'r').read()

print(tmpl.replace('<!--CONTENT-->',content).replace('<!--LSIDEBAR-->',lsidebar).replace('<!--RSIDEBAR-->',rsidebar).replace('<!--FOOTER-->',footer))
