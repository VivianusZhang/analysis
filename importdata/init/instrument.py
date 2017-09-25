import time

import pymongo
import tushare as ts
from  pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['stock']

db.instrumentDailyData.create_index([('code', pymongo.ASCENDING)])

cursor = db.instrument.find({})
for document in cursor:
    code = document['code']

    if db.instrumentDailyData.find({'code': code}).count() == 0:
        try:
            print('downloading : ' + code)
            dailyData = ts.get_h_data(code, start='2015-01-01', end=time.strftime("%Y-%m-%d"))
            dailyData['code'] = code
            dailyData['date'] = dailyData.index
            db.instrumentDailyData.insert_many(dailyData.to_dict('records'))
        except Exception:
            continue

print('end of import instrument index')
