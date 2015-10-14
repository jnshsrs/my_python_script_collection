#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import urlopen
import pymysql

pw = '0mcuda1gb' #raw_input('Enter DB password')

conn = pymysql.connect(host='127.0.0.1', unix_socket='/var/run/mysqld/mysqld.sock', 
	user='root', passwd= pw, db='mysql', charset='utf8mb4')
cur = conn.cursor()

# cur.execute('DROP DATABASE IF EXISTS hospitals')
cur.execute('CREATE DATABASE IF NOT EXISTS hospitals')
cur.execute('USE hospitals')
cur.execute('''
	CREATE TABLE IF NOT EXISTS tbl_pflegedienstleitung (
		id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
		titel VARCHAR(255) NOT NULL,
		vorname VARCHAR(255) NOT NULL,
		nachname VARCHAR(255) NOT NULL,
		position VARCHAR(255) NOT NULL,
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
	person = bsObj.find(person).person_kontakt.person
	return person

# my task for scraping hospital data
bsObj = openQualiBerichte("./qualit_berichte/260100023-00-2013-xml.xml")
person = getPerson('verwaltungsleitung')
varlist = []

# select a tag and then iterate over it
for element in person:
 	if not element.name == None:
 		varlist.append(element.string)

var_string = "%s, %s, %s, %s"
query_string = '''INSERT INTO tbl_pflegedienstleitung (titel, vorname, nachname, position) VALUES (%s);''' % var_string
cur.execute(query_string, varlist)

conn.commit()
cur.close() 
conn.close()