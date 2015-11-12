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
			name VARCHAR(255), 
			ik_from_xml VARCHAR(255),
			standort_nummer_from_xml VARCHAR(255),
			straße VARCHAR(255),
			hausnummer VARCHAR(255),
			postleitzahl VARCHAR(255),
			ort VARCHAR(255),
			traeger_name VARCHAR(255),
			traeger_art VARCHAR(255),
			anzahl_betten INT,
			vollstationaere_fallzahl INT,
			teilstationaere_fallzahl INT,
			ambulante_fallzahl INT,
			created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)
		''')
createTableHospital()
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

def getValuesFromParentTag(parentBSObj, valueTagNames, lstToAppend):
	for tag in valueTagNames:
					try:
						currentValue = parentBSObj.find(tag).string
						lstToAppend.append(currentValue)
					except:
						currentValue = None
						lstToAppend.append(currentValue)

sql_insert_pdf = '''
INSERT INTO tbl_hospitalData 
			(ik, standort_nummer, name, ik_from_xml, standort_nummer_from_xml, straße, 
			hausnummer, postleitzahl, ort, traeger_name,
			traeger_art, anzahl_betten, vollstationaere_fallzahl, 
			teilstationaere_fallzahl, ambulante_fallzahl)
	VALUES ('%s','%s','%s','%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'); 
'''

pathToXMLfiles = "../Qualitaetsberichte/Berichte-KH/*.xml"
# create list ob xml files in the prespecified path
globObj = glob.glob(pathToXMLfiles)

cnt = 0
absolut =  float(len(globObj))

for xmlFile in globObj:
	cnt += 1
	relative = float(cnt) / absolut 
	try:
		if(not '-99-' in xmlFile):
			print 'Data extraction started.'
			bsObj = openQualiBerichte(xmlFile)
			
			ik = re.findall('[0-9]{9}', xmlFile)[0]
			standortnummer = re.findall('[0-9]{2}', re.findall('-[0-9]{2}-', xmlFile)[0])[0]
			valueLst = [ik, standortnummer]

			# Adressdaten
			currentTag = getTag('kontaktdaten')
			tagsKrankenhausAdresse = ['name', 'ik', 'standortnummer', 'strasse', 
									  'hausnummer', 'postleitzahl', 'ort']
			getValuesFromParentTag(parentBSObj = currentTag, valueTagNames = tagsKrankenhausAdresse, lstToAppend = valueLst)

			# Trägerdaten
			currentTag = getTag('krankenhaustraeger')
			tagsKrankenhausTraeger = ['name', 'art']
			getValuesFromParentTag(parentBSObj = currentTag, valueTagNames = tagsKrankenhausTraeger, lstToAppend = valueLst)
			

			# Bettenanzahl
			currentValue = bsObj.find('anzahl_betten').string
			valueLst.append(currentValue)

			# Demografische Daten
			currentTag = getTag('fallzahlen')
			tagsKrankenhausFallzahlen = ['vollstationaere_fallzahl', 'teilstationaere_fallzahl', 'ambulante_fallzahl']
			getValuesFromParentTag(parentBSObj = currentTag, valueTagNames = tagsKrankenhausFallzahlen, lstToAppend = valueLst)
			
			print valueLst
			cur.execute(sql_insert_pdf % tuple(valueLst))
			print('data inserted, %', relative)
	except:
		print('Error occured Inserting NULLS, %', relative)
		print('The Previous IK was:', ik)
				
conn.commit()
cur.close() 
conn.close()