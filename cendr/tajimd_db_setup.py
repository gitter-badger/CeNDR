from collections import OrderedDict
from peewee import *
import re
import requests
import json
import datetime
from dateutil.parser import parse
import os
import StringIO
import csv
import MySQLdb
import _mysql
import sys

credentials = json.loads(open("credentials.json", 'r').read())
reset_db = False

if (os.getenv('SERVER_SOFTWARE') and
        os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
    db = MySQLDatabase('cegwas_v2', unix_socket='/cloudsql/andersen-lab:cegwas-data', user='root')
else:
    credentials = json.loads(open("credentials.json",'r').read())
    db =  MySQLDatabase(
      'cegwas_v2',
      **credentials
      )

db.connect()

import models
with db.atomic():
  db.create_tables([tajimaD], safe=True)


with open('tajima.csv', 'rb') as csvfile:
  print dir(csvfile)
  lines = csv.DictReader(csvfile, delimiter='\t')

  tajima_d = []
  for index,line in enumerate(lines):
      for k,v in line.items():
        if k !='CHROM' and k != 'TajimaD':
          line[k] = int(v)

      line['TajimaD'] = round(float(line['TajimaD']),3)
      if line:
        tajima_d.append(line)

with db.atomic():
  tajimaD.insert_many(tajima_d).execute()
