#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
from glob import glob
from collections import Counter
import csv
import os
import numpy as np

pathToXMLfiles = './qualit_berichte/*.xml'

globObj = glob(pathToXMLfiles)

# function to parse xml files
def parseXML(XMLpath):
	with open(XMLpath) as xmlfile:
		xmlfile = xmlfile.read()
		bsObj = bs(xmlfile, 'html.parser')
		return(bsObj)

# function will catch data from xml with the function find
def getKontaktdaten(beautifulSoupObject,key):
	values = []
	for tag in key:
		try:
			val = beautifulSoupObject.find(tag).string
		except:
			val = 'Null'
		values.append(val)
	return(values)

# function takes bsObj (quality report data) and returns IK number (Unique identifier for each hosptial)
def getIK(beautifulSoupObject):
	ik = beautifulSoupObject.find('ik').string
	return(ik)	

tags = ['ik', 'name', 'email','url', 'standortnummer', 'url_homepage_krankenhaus','art']
listKontaktdaten = []
for XMLfile in globObj:
	bsObj = parseXML(XMLpath = XMLfile)
	tag_values = getKontaktdaten(beautifulSoupObject = bsObj, key = tags)
	print tag_values
	listKontaktdaten.append(tag_values)