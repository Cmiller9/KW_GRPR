# -*- coding: utf-8 -*-
from xml.etree import ElementTree as ET
import string

import requests


BASE_URL = 'http://google.com/complete/search?output=toolbar&q='

"""r = requests.get('http://google.com/complete/search?output=toolbar&q=keyword')

x = str(r.text)
root = ET.fromstring(x)

for child in root: print child[0].attrib"""

"""def suggestion_decorator(func):
	def wrapper(*args,**kwargs):
		for value in func(*args,**kwargs):
			print value
	return wrapper"""

#@suggestion_decorator
def google_suggestions(URL, qry):
	r = requests.get('%s%s' % (URL,qry))
	x = r.text
	root = ET.fromstring(x)
	a = []
	for child in root:
		a.append('%s' % child[0].attrib['data'])
	return a

def google_az_suggestions(URL, qry):
	a = []
	for i in range(len(string.ascii_lowercase)):
		x = string.ascii_lowercase[i]
		r = requests.get('%s%s+%s' % (URL,qry,x))
		y = r.text
		try:
			root = ET.fromstring(y)
			#LIST COMPREHENSION
			a.append(['%s' % child[0].attrib['data'] for child in root])
		except:
			a.append(['-']*10)
	return a

if __name__ == '__main__':
	a = google_az_suggestions(BASE_URL,'ça')
	for line in a:
		print line
