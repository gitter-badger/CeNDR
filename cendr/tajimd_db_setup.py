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

from models import *
with db.atomic():
  db.create_tables(['wi_20160326'], safe=True)


with open('tajima.csv', 'rb') as csvfile:
  csv_reader = csv.reader(csvfile, delimiter='\t', quotechar='|')

  tajima_d = []
  for line in csv_reader:
    tajima_d.append(line)


with db.atomic():
  wi_20160326.insert_many(strain_data).execute()

