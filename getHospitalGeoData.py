#!/usr/bin/env python
# -*- coding: utf-8 -*-

# load libraries
from bs4 import BeautifulSoup as bs
import glob
import urllib
from httplib2 import iri2uri
import pymysql

import sys # encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')

# database setup
pw = raw_input('Enter DB password: ')
conn = pymysql.connect(host='131.173.88.189', user='huesers', passwd= pw, charset='utf8mb4')
cur = conn.cursor()

cur.execute('use huesers')

sqlCreateTableAddresses = '''
CREATE TABLE IF NOT EXISTS tbl_HospitalAddresses (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
	ik INT,
	formatted_address VARCHAR(255),
	longitude VARCHAR(255),
	latitude VARCHAR(255),
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
	)
'''
cur.execute(sqlCreateTableAddresses)

# creating functions
# read data and create BeautifulSoup object
def parseXML(XMLpath):
	with open(XMLpath) as xmlfile:
		xmlfile = xmlfile.read()
		bsObj = bs(xmlfile, 'html.parser')
		return(bsObj)

# function will catch data from xml with the function find
def getGeoData(beautifulSoupObject, XMLtags):
	values = []
	for tag in XMLtags:
		try:
			val = beautifulSoupObject.find('hausanschrift').find(tag).string

		except:
			val = 'Null'
		values.append(val)
	return(values)

# make function to create apiUrl 
def makeGeoURL(apiKey, adress):
	sep = '+'
	adress_data = sep.join(adressData)
	apiURL = 'https://maps.googleapis.com/maps/api/geocode/xml?address=' + adress_data + '&key=' + apiKey 
	return(apiURL)

# function to convert urls to unicoding
def iri_to_uri(iri):
    """Transform a unicode iri into a ascii uri."""
    if not isinstance(iri, unicode):
        raise TypeError('iri %r should be unicode.' % iri)
    return bytes(iri2uri(iri))

# loading required data
# of which data tags should the data be extracted?
geoTags = ['strasse', 'hausnummer', 'postleitzahl', 'ort']
# define path to xml files
pathToXMLfiles = './Berichte-KH/*.xml'
# create list ob xml files in the prespecified path
globObj = glob.glob(pathToXMLfiles)

cnt = 1

for XMLfile in globObj:
	# make beautiful soup object of XML files
	bsObj = parseXML(XMLfile)
	# call function get geoData which will return data from xmlFiles
	# this data is stored in a list which will be used to create a api url to obtain geodata
	adressData = getGeoData(beautifulSoupObject = bsObj, XMLtags = geoTags)
	# geoDate
	apiKey = 'AIzaSyAQlNFxEOHJohz-ncxOJ_js0X8avAH2Ytg'
	apiURL = makeGeoURL(apiKey = apiKey, adress = adressData)
	# convert apiURL to unicode
	apiURL = iri_to_uri(apiURL)

	# open url
	f = urllib.urlopen(apiURL)
	googleGeoData = f.read()
	bsGeoObj = bs(googleGeoData)

	#try except einbauen da ein Kranknenhaus keine formatierte Adresse zurückgibt
	ik = bsObj.ik.string
	try:
		formatted_address = bsGeoObj.find('formatted_address').string
	except:
		formatted_address = 'NULL'

	try:
		latitude = bsGeoObj.find('lat').string
		longitude = bsGeoObj.find('lng').string
	except:
		latitude = 'NULL'
		longitude = 'NULL'		
	
	geoList = (ik, formatted_address, latitude, longitude)
	print 'Loop number:', cnt 
	cnt += 1 

	sqlInsertStatement = '''
	INSERT INTO tbl_HospitalAddresses (ik, formatted_address, latitude, longitude) VALUES (\"%s\", \"%s\", \"%s\", \"%s\");
	''' % geoList

	cur.execute(sqlInsertStatement)

conn.commit()
cur.close()
conn.close