#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from dbfpy import dbf

#DUMP FILE TO CSV
def dumpfile(name):
	db = dbf.Dbf(name)
	csv=open(name+".csv","w")
	#print db
	cnt=0

	for key in db.fieldNames:
		csv.write('"%s",'%key)
	csv.write("\n\r")

	for rec in db:
		for key in db.fieldNames:
			try:
				value=rec[key].replace('"','\\"')
			except:
				value=rec[key]
			csv.write('"%s",'%value)
		csv.write("\n\r")
		cnt+=1
	csv.close()
	print "Traité %s avec %d Enregistrements "%(name,cnt)



#dumpfile("dpgift.DBF")
dumpfile("dp.DBF")
dumpfile("DPADD.DBF")
dumpfile("dpphone.DBF")
dumpfile("dpother.DBF")
