#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as BS

l = []

with open('bvb_darmstadt.html') as f:
	soup = BS(f)
	table = soup.find('table', attrs={'class':'tStat tStatKarten'})
	rows = table.find_all('tr')

	for tr in rows:
		cols = tr.find_all('th')
		x = []
		for th in cols:
			x.append(th.find(text=True))	
		l.append(x)

x = []

for i in l:
	if len(i) > 3:
		 x.append(i)

heimteam = x[0][0]
auswteam = x[0][len(x[0])-1]

print heimteam, 'gegen', auswteam


