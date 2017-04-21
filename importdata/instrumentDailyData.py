from  pymongo import MongoClient

import json
import pymongo
import pprint
import tushare as ts
import unicodecsv as csv
import numpy as np
import time

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']


cursor = db.instrument.find({})
for document in cursor:
    code = document['code']
    print('downloading : ' + code)
    dailyData = ts.get_k_data(code, '2000-01-01', time.strftime("%Y-%m-%d"))
    if not dailyData.empty:
        db.instrumentDailyData.insert_many(dailyData.to_dict('records'))

print('end of import instrument data')
