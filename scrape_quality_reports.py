#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import urlopen
import pymysql
import glob
import re

import sys # encoding=utf8
reload(sys)
sys.setdefaultencoding('utf8')

#pw = raw_input('Enter DB password:  ')
pw = "6kY6a:D*HL"
conn = pymysql.connect(host='131.173.88.189', unix_socket='/var/run/mysqld/mysqld.sock', 
	user='huesers', passwd= pw, db='huesers', charset='utf8')
cur = conn.cursor()

def createTableHospital():
	#cur.execute('USE huesers')
	cur.execute('DROP TABLE IF EXISTS tbl_hospitalData;')
	cur.execute('''
		CREATE TABLE IF NOT EXISTS tbl_hospitalData (
			id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
			ik VARCHAR(255),
			standort_nummer VARCHAR(255),
			straße VARCHAR(255),
			hausnummer VARCHAR(255),
			postleitzahl VARCHAR(255),
			ort VARCHAR(255),
			created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)
		''')

# function to open a xml file and create a beatifulSoup object
def openQualiBerichte(file):
	xml_path = file
	with open(xml_path) as xml:
		xml = xml.read()
		bsObj = BeautifulSoup(xml)
		return(bsObj)

# function will look for person data (pflegedienstleitung, aerztliche Leitung etc.)
def getTag(person): 
	person = bsObj.find(person)
	return person

sql_insert_pdf = '''
INSERT INTO tbl_pflegedienstleitung (ik,standort_nummer,titel, vorname, nachname, position, vorwahl, rufnummer, durchwahl, email)
	VALUES ('%s','%s','%s','%s', '%s', '%s', '%s', '%s', '%s', '%s'); 
'''

pathToXMLfiles = "../Qualitaetsberichte/Berichte-KH/*.xml"
# create list ob xml files in the prespecified path
globObj = glob.glob(pathToXMLfiles)
globObj = globObj[0:3]
cnt = 0
absolut =  float(len(globObj))

for xmlFile in globObj:
	cnt += 1
	relative = float(cnt) / absolut 
	try:
		if(not '-99-' in xmlFile):
			print 'Data extraction started.'
			bsObj = openQualiBerichte(xmlFile)
			# Adressdaten
			currentTag = getTag('kontaktdaten')
			tagsKrankenhausAdresse = ['name', 'ik', 'standortnummer', 'strasse', 
									  'hausnummer', 'postleitzahl', 'ort']
			ik = re.findall('[0-9]{9}', xmlFile)[0]
			standortnummer = re.findall('-[0-9]{2}-', xmlFile)[0]
			standortnummer = re.findall('[0-9]{2}', standortnummer)[0]
			valueLst = [ik, standortnummer]

			for tag in tagsKrankenhausAdresse:
				try:
					currentValue = currentTag.find(tag).string
					valueLst.append(currentValue)
				except:
					currentValue = None
					valueLst.append(currentValue)

			# Trägerdaten
			currentTag = getTag('krankenhaustraeger')
			tagsKrankenhausTraeger = ['name', 'art']
			for tag in tagsKrankenhausTraeger:
				try:
					currentValue = currentTag.find(tag).string
					valueLst.append(currentValue)
				except:
					currentValue = None
					valueLst.append(currentValue)
			
			currentValue = bsObj.find('anzahl_betten').string
			valueLst.append(currentValue)
			print 'Adresse: ', valueLst
			
			# Demografische Daten
			currentTag = getTag('fallzahlen')
			tagsKrankenhausFallzahlen = ['vollstationaere_fallzahl', 'teilstationaere_fallzahl', 'ambulante_fallzahl']
			for tag in tagsKrankenhausFallzahlen:
				try:
					currentValue = currentTag.find(tag).string
					valueLst.append(currentValue)
				except:
					currentValue = None
					valueLst.append(currentValue)
			print valueLst	
	





			
			#cur.execute(sql_insert_pdf % tuple(valueLst))
			#print('data inserted, %', relative)


	except:
		print('Error occured Inserting NULLS, %', relative)
		#cur.execute(sql_insert_pdf % tuple(None, None, None, None, None, None, None, None, None, None))
conn.commit()
cur.close() 
conn.close()