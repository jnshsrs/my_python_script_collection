#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib import urlopen
import pymysql

def connectDB(host, username, database):
	pw = raw_input('Enter DB password')
	conn = pymysql.connect(host=host, user=username, passwd= pw, db=database, charset='utf8mb4')
	return(conn)

conn = connectDB(host = 'l4asrv-mysql.wi.hs-osnabrueck.de', database = 'huesers', username = 'huesers')
cur = conn.cursor()

# INSERT DATA

conn.commit()
cur.close()
conn.close()