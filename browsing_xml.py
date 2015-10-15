#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from glob import glob
from collections import Counter
import csv
import os
import numpy as np

globObj = glob('/Users/igw/documents/qualitätsberichte/Berichte-KH/*.xml')

# function to parse xml files
def parseXML(XMLpath):
	with open(XMLpath) as xmlfile:
		xmlfile = xmlfile.read()
		bsObj = bs(xmlfile, 'html.parser')
		return(bsObj)

# function will catch data from xml with the function find
def getKontaktdaten(beautifulSoupObject,key):
	tag_values = []
	tag_values.append(beautifulSoupObject.find(key).string)
	return(tag_values)
# function takes bsObj (quality report data) and returns IK number (Unique identifier for each hosptial)
def getIK(beautifulSoupObject):
	ik = beautifulSoupObject.find('ik').string
	return(ik)	

d = {'ik':[], 'name':[], 'email':[],'url':[], 'standortnummer':[], 'url_homepage_krankenhaus':[], 'art':[]}

tags = []
for key in d:
	tags.append(key)

for filepath in globObj[0]:
	bsObj = parseXML(filepath)



print tags
