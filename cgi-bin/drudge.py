#!/usr/bin/python
#
import re, string, urllib

target = "http://idrudgereport.com"

style = re.compile('<style [\W\w\n]*?</style>')
script = re.compile('<script [\W\w\n]*?</script>')
head = re.compile('<HEAD[\W\w\n]*?</HEAD>')
img = re.compile('<img [\W\w\n]*?/>')
drudge = urllib.urlopen(target).read()

slob = re.sub(style,'',drudge)
loaf = re.sub(script,'',slob)
page = re.sub(head,'<head></head>',loaf)

print('Content-Type: text/html\n\n')
print(re.sub(img,'',page))
