#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from glob import glob
from collections import Counter
import csv
import os

globObj = glob('/Users/igw/documents/qualitätsberichte/Berichte-KH/*.xml')

# function to parse xml files
def parseXML(XMLpath):
	with open(XMLpath) as xmlfile:
		xmlfile = xmlfile.read()
		bsObj = bs(xmlfile, 'html.parser')
		return(bsObj)

def getKontaktdaten(beautifulSoupObject,key):
	d[key].append(beautifulSoupObject.find(key).string)

# function takes bsObj (quality report data) and returns IK number (Unique identifier for each hosptial)
def getIK(beautifulSoupObject):
	ik = beautifulSoupObject.find('ik').string
	return(ik)	


# parse xml file with function: parseXML
# get hospital data from krankenhaus > kontaktdaten tag
d = {'ik':[], 'name':[], 'email':[],'url':[], 'standortnummer':[], 'url_homepage_krankenhaus':[], 'art':[]}
for file in globObj[0:2]:
	bsObj = parseXML(file)
	kh_kontakt = bsObj
	for key in d:
		getKontaktdaten(kh_kontakt, key)

for value in d:
	print value 