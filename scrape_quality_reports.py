#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import urlopen
import pymysql
import glob
import re

#  pw = raw_input('Enter DB password')

conn = pymysql.connect(host='131.173.88.189', unix_socket='/var/run/mysqld/mysqld.sock', 
	user='huesers', passwd= '6kY6a:D*HL', db='huesers', charset='utf8mb4')
cur = conn.cursor()

def createTablePDL():
	#cur.execute('USE huesers')
	cur.execute('DROP TABLE IF EXISTS tbl_pflegedienstleitung;')
	cur.execute('''
		CREATE TABLE IF NOT EXISTS tbl_pflegedienstleitung (
			id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
			ik VARCHAR(255) NOT NULL,
			standort_nummer INT NOT NULL
			titel VARCHAR(255) NOT NULL,
			vorname VARCHAR(255) NOT NULL,
			nachname VARCHAR(255) NOT NULL,
			position VARCHAR(255) NOT NULL,
			email VARCHAR(255),
			created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)
		''')

def createTablePDL():
	#cur.execute('USE huesers')

	cur.execute('DROP TABLE IF EXISTS tbl_hospitalData;')
	cur.execute('''
		CREATE TABLE IF NOT EXISTS tbl_hospitalData (
			id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
			ik VARCHAR(255) NOT NULL,
			standort_nummer INT NOT NULL
			straße VARCHAR(255) NOT NULL,
			hausnummer VARCHAR(255) NOT NULL,
			postleitzahl VARCHAR(255) NOT NULL,
			ort VARCHAR(255) NOT NULL,
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

# my task for scraping hospital data
filePath = "../Qualitätsberichte/Berichte-KH/260000066-00-2013-xml.xml"
bsObj = openQualiBerichte(filePath)
person = getPerson('pflegedienstleitung')

tagLst = ['titel', 'vorname', 'nachname', 'position', 
		  'vorwahl', 'rufnummer', 'durchwahl', 'email']
print re.findall('[0-9]{9}', filePath)[0]
standortnummer = re.findall('-[0-9]{2}-', filePath)[0]
standortnummer = re.findall('[0-9]{2}', standortnummer)[0]
print standortnummer
for tag in tagLst:
	try:
		print person.find(tag).string
	except:
		print 'NULL'
# person data is a list which is filled with

# ik, standordnummer, titel, vorname, nachnameposition
personData = []

# select a tag and then iterate over it
#for element in person:
# 	if not element.name == None:
# 		varlist.append(element.string)

#print varlist
#var_string = "%s, %s, %s, %s"
#query_string = '''INSERT INTO tbl_pflegedienstleitung (titel, vorname, nachname, position) VALUES (%s);''' % var_string
#cur.execute(query_string, varlist)

conn.commit()
cur.close() 
conn.close()