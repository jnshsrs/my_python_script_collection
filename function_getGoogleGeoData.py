#!/usr/bin/env python
# -*- coding: utf-8 -*-

# load libraries

from bs4 import BeautifulSoup as bs
import glob
import urllib
from httplib2 import iri2uri
import pymysql

filePath = './Berichte-KH/260000066-00-2013-xml.xml'

with open(filePath) as f:
	XMLfile = f.read()
	bsObj = bs(XMLfile)

# database setup
user = 'huesers'
IP = '131.173.88.189'
pw = raw_input('Enter DB password for %s@%s: ' % (user, IP))
pw = '6kY6a:D*HL'
conn = pymysql.connect(host=IP, user=user, passwd= pw, charset='utf8mb4')
cur = conn.cursor()
cur.execute('use huesers')
#cur.execute('DROP TABLE tbl_HospitalAddresses;')
print 'Tables dropped'
lstPersonen = ['aerztliche_leitung', 'pflegedienstleitung', 'verwaltungsleitung']
personen_tags = ['vorname', 'nachname', 'position', 'vorwahl', 'rufnummer', 'durchwahl', 'email']

def createPersonPostionTable(positionName, lstPersonValues):
	createPersonTables = '''
		CREATE TABLE IF NOT EXISTS tbl_%s (
			ID_%s INT NOT NULL AUTO_INCREMENT,
			%s VARCHAR(255),
			%s VARCHAR(255),
			%s VARCHAR(255),
			%s VARCHAR(255),
			%s VARCHAR(255),
			%s VARCHAR(255),
			%s VARCHAR(255),
			created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			ID_hospital INT,
			PRIMARY KEY (ID_%s),
			FOREIGN KEY (ID_hospital) REFERENCES tbl_HospitalAddresses(ID_hospital)
			);
	'''
	return(createPersonTables % tuple(2*[positionName] + lstPersonValues + [positionName]))

sqlCreateTableGoogleAddresses = '''
CREATE TABLE IF NOT EXISTS tbl_GoogleAddresses (
	ID_GoogleAdresses INT AUTO_INCREMENT,
	postal_code VARCHAR(255),
	route VARCHAR(255),
	street_number VARCHAR(255),
	locality VARCHAR(255),
	sublocality_level_1 VARCHAR(255),
	administrative_area_level_1 VARCHAR(255),
	longitude VARCHAR(255),
	latitude VARCHAR(255),
	formatted_address VARCHAR(255),
	ID_hospital INT,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (ID_GoogleAdresses),
	FOREIGN KEY (ID_hospital) REFERENCES tbl_HospitalAddresses(ID_hospital)
	);
'''

GeoTags = ['postal_code', 'route', 'street_number', 'locality', 'sublocality_level_1', 'administrative_area_level_1', 'country']

def createHospitalTable():
	sqlCreateHospitalTable = '''
	CREATE TABLE IF NOT EXISTS tbl_HospitalAddresses (
		ID_hospital INT NOT NULL AUTO_INCREMENT,
		name VARCHAR(255),
		ik VARCHAR(255),
		standortnummer VARCHAR(255),
		strasse VARCHAR(255),
		postleitzahl VARCHAR(255),
		ort VARCHAR(255),
		vorwahl VARCHAR(255),
		rufnummer VARCHAR(255),
		durchwahl VARCHAR(255),
		email VARCHAR(255),
		url_traeger VARCHAR(255),
		url_krankenhaus VARCHAR(255),
		traeger_name VARCHAR(255),
		traeger_art VARCHAR(255),
		created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
		PRIMARY KEY (ID_hospital)
		);
	'''
	return(sqlCreateHospitalTable)

cur.execute(createHospitalTable())
for element in lstPersonen:
	 cur.execute(createPersonPostionTable(element, personen_tags))
cur.execute(sqlCreateTableGoogleAddresses)



conn.commit()
cur.close()
conn.close



#for person in lstPersonen:
#	x = bsObj.find(person).person_kontakt
#	
#	for tag in personen_tags:
#		print x.find(tag).string



