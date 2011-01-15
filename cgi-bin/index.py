#!/usr/bin/python
# index script will determine permissions to view subsequent pages
# and redirect to the appropriate page.
import cgi

TMPL_DIR = '../tmpl/'

CONTENT_DIR = '../content/'

tmpl = open(TMPL_DIR+'page','r').read()

lsidebar = open(TMPL_DIR+'lsidebar','r').read()

rsidebar = open(TMPL_DIR+'rsidebar','r').read()

form = cgi.FieldStorage()

if form.has_key('q'):

	page = form['q'].value

else:

	page = 'home'

content = open(CONTENT_DIR+page,'r').read()

print('Content-Type: text/html\n\n\n')

print(tmpl.replace('<!--CONTENT-->',content).replace('<!--LSIDEBAR-->',lsidebar).replace('<!--RSIDEBAR-->',rsidebar))
