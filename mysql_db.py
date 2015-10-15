#!/usr/bin/env python
# -*- coding: utf-8 -*-


# PART I - loading libraries
from bs4 import BeautifulSoup
from urllib import urlopen
import pymysql


# PART II - defining functions
def connectDB(host, username, database):
	pw = raw_input('Enter DB password')
	conn = pymysql.connect(host=host, user=username, passwd= pw, db=database, charset='utf8mb4')
	return(conn)
# create tables for person data (director of nursing, medical administration, business administration)
def createTablePersons(nameList):
	for table_names in nameList:
		cur.execute('''
			CREATE TABLE IF NOT EXISTS %s (
				id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
				titel VARCHAR(255) NOT NULL,
				vorname VARCHAR(255) NOT NULL,
				nachname VARCHAR(255) NOT NULL,
				position VARCHAR(255) NOT NULL,
				created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)
			''' % table_names)
# function to open a xml file and create a beatifulSoup object
def openQualiBerichte(file):
	xml_path = file
	with open(xml_path) as xml:
		xml = xml.read()
		bsObj = BeautifulSoup(xml)
		return(bsObj)
# function to select person tags
def getPerson(person): 
	person = bsObj.find(person).person_kontakt.person
	return person
# function to insert data
def insertData():
	# create list to store data from the xml document
	varlist = []
	# iterate over tags in person tag
	for element in person:
	 	if not element.name == None:
	 		varlist.append(element.string)
	var_string = "%s, %s, %s, %s"
	query_string = "INSERT INTO pflegedienstleitung (titel, vorname, nachname, position) VALUES (%s);" % var_string
	cur.execute(query_string, varlist)


# PART III - executing task
# MYSQL DDL COMMANDS (DATA DEFINITION)
# open database with function connectDB
conn = connectDB(host = 'l4asrv-mysql.wi.hs-osnabrueck.de', database = 'huesers', username = 'huesers')
# create cursor
cur = conn.cursor()
# list of table names
nameList = ['pflegedienstleitung', 'aerztliche_leitung', 'verwaltungsleitung']
# create tables for person with function createTablePerson
createTablePersons(nameList)


# BEAUTIFULSOUP XML PARSING
# open xml file
bsObj = openQualiBerichte("./qualit_berichte/260100023-00-2013-xml.xml")
# select pflegedienstleitung tag
person = getPerson('pflegedienstleitung')

# MYSQL DML COMMANDS (DATA MANIPULATION)
insertData()

conn.commit()
cur.close()
conn.close()