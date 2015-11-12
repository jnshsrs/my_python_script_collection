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

cur.execute('DROP TABLE IF EXISTS tbl_pflegedienstleitung;')
cur.execute('''
		CREATE TABLE IF NOT EXISTS tbl_pflegedienstleitung (
			id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
			ik VARCHAR(255),
			standort_nummer VARCHAR(255),
			titel VARCHAR(255),
			vorname VARCHAR(255),
			nachname VARCHAR(255),
			position VARCHAR(255),
			vorwahl VARCHAR(255),
			rufnummer VARCHAR(255),
			durchwahl VARCHAR(255),
			email VARCHAR(255),
			created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)
		ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin
		AUTO_INCREMENT=1;
		''')

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
def getPerson(person): 
	person = bsObj.find(person)
	return person

sql_insert_pdf = '''
INSERT INTO tbl_pflegedienstleitung (ik,standort_nummer,titel, vorname, nachname, position, vorwahl, rufnummer, durchwahl, email)
	VALUES ('%s','%s','%s','%s', '%s', '%s', '%s', '%s', '%s', '%s'); 
'''

pathToXMLfiles = "../Qualitaetsberichte/Berichte-KH/*.xml"
# create list ob xml files in the prespecified path
globObj = glob.glob(pathToXMLfiles)
dglobObj = globObj[0:10]
cnt = 0
absolut =  float(len(globObj))

for xmlFile in globObj:
	cnt += 1
	relative = float(cnt) / absolut 
	try:
		if(not '-99-' in xmlFile):
			print 'Data extraction started.'
			bsObj = openQualiBerichte(xmlFile)
			person = getPerson('pflegedienstleitung')
			tagLst = ['titel', 'vorname', 'nachname', 'position', 
					  'vorwahl', 'rufnummer', 'durchwahl', 'email']
			ik = re.findall('[0-9]{9}', xmlFile)[0]
			standortnummer = re.findall('-[0-9]{2}-', xmlFile)[0]
			standortnummer = re.findall('[0-9]{2}', standortnummer)[0]
			valueLst = [ik, standortnummer]
			for tag in tagLst:
				try:
					currentValue = person.find(tag).string
					valueLst.append(currentValue)
				except:
					currentValue = None
					valueLst.append(currentValue)
			cur.execute(sql_insert_pdf % tuple(valueLst))
			print('data inserted, %', relative)
	except:
		print('Error occured Inserting NULLS, %', relative)
		cur.execute(sql_insert_pdf % tuple(None, None, None, None, None, None, None, None, None, None))

conn.commit()
cur.close() 
conn.close()