#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from glob import glob
from collections import Counter

globObj = glob('/Users/igw/documents/qualitätsberichte/Berichte-KH/*.xml')

def parseXML(XMLpath):
	with open(XMLpath) as xmlfile:
		xmlfile = xmlfile.read()
		bsObj = bs(xmlfile, 'html.parser')
		return(bsObj)


bsObj = parseXML(globObj[5])
for tag in bsObj.qualitaetsbericht.children:
	if not tag.name == None:
		print tag.name
		for a in tag.children:
			if not a.name == None:
				print '\t', a.name
				for b in a.children:
					if not b.name == None:
						print '\t', '\t', b.name
							
	
# cntr = Counter(globObj)
# print(len(globObj)) # There are 2193 quality reports for 2013

# This will give back the bed count for every quality report
#bettenList = [] 
#for filePath in globObj[0:20]:
#	bsObj = parseXML(filePath)
#	betten = int(bsObj.qualitaetsbericht.anzahl_betten.string)
#	bettenList.append(betten)

#print bettenList


