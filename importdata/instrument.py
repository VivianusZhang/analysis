from  pymongo import MongoClient
import json
import pymongo
import tushare as ts
import numpy as np

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']

df = ts.get_today_all()
df1 = df[['code', 'name']]
db.instrument.insert_many(df1.to_dict('records'))

print('end of import instrument data')
