#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('text.db')
print 'Opened database successfully'

conn.execute("DROP TABLE IF EXISTS tbl_spiel")

conn.execute('''CREATE TABLE tbl_spiel (
		type1 TEXT,
	 	value_heim INT,
		sep TEXT,
		value_ausw INT,
	 	type2 TEXT)
		''')


from bs4 import BeautifulSoup as BS

l = []

with open('bvb_darmstadt.html') as f:
	soup = BS(f)
	table = soup.find('table', attrs={'class':'tStat tStatKarten'})
	rows = table.find_all('tr')

	for tr in rows:
		cols = tr.find_all('td')
		x = []
		for td in cols:
			x.append(td.find(text=True))	
		l.append(x)
	
with open('bvb_darmstadt.html') as f:
	soup = BS(f)
	table = soup.find('table', attrs={'class':'tStat tStatKarten'})
	rows = table.find_all('tr')
	y = []
	for th in rows:
		team = th.find_all('th')
		for th in team:
			y.append(th.find(text=True)

for i in l:
	if len(i) == 5:
		conn.executemany("INSERT INTO tbl_spiel (type1, value_heim, sep, value_ausw, type2) VALUES (?, ?, ?, ? ,?)", (i,)) 
	else:
		print 'Line skipped due to less values'
conn.commit()
print "Records created successfully"
conn.close()






