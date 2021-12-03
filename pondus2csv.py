#!/usr/bin/python3
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as et
from datetime import date, datetime
import locale

loc = locale.getlocale()
locale.setlocale(locale.LC_ALL, loc)

weight_list = []
sqldate_list = []
date_list = []

tree = et.parse('user_data.xml')

root = tree.getroot()
print("root tag:", root.tag)
print("konvertiere zu CSV")
for child in root.findall('*'):
    for a in child.findall('*'):
        for b in a.findall('*'):
            for c in b.findall('*'):
                valueline = c.text
                tag = c.tag
                if c.tag == "date":
                    sqldate = valueline.replace("-", "")
                    sqldate_list.append(sqldate)
                    t = datetime.strptime(sqldate, "%Y%m%d")
                    date = t.strftime('%A, %d.%B %Y')
                    date_list.append(date)
                elif c.tag == "weight":
                    weight_list.append(valueline)

pondusliste = []
liste = []

for x in range(len(sqldate_list)):
    pondusliste.append(f"{date_list[x]}\t{weight_list[x]}\t\t{sqldate_list[x]}\n")


for lines in pondusliste:
    line = lines.split("\t")
    datum = datetime.strptime(line[0], "%A, %d.%B %Y")
    gewicht = line[1]
    gewicht = str(float(gewicht))
    d = datum.strftime("%A, %d.%B %Y")
    sqldatum = datum.strftime("%Y%m%d")
    entry = f"{d}\t{gewicht}\t\t{sqldatum}"
    if not entry in liste:
        liste.append(entry)
        
slist=sorted(liste,key = lambda x:x[-8])

with open("PondusImport.csv", "w") as f:
    f.write('\n'.join(slist))
    
