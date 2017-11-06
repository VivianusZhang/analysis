import pymongo
import tushare as ts
from  pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']

cons = ts.get_apis()

db.instrumentDailyData.create_index([('code', pymongo.ASCENDING)])

cursor = db.instrument.find({})
for document in cursor:
    code = document['code']

    if db.instrumentDailyData.find({'code': code}).count() == 0:
        try:
            print('downloading : ' + code)
            dailyData = ts.bar(code, conn=cons, start_date='2015-01-01', end_date='2017/10/31')
            dailyData['code'] = code
            dailyData['volume'] = dailyData['vol']
            dailyData.drop('vol', 1)
            dailyData['datetime'] = dailyData.index
            db.instrumentDailyData.insert_many(dailyData.to_dict('records'))
        except Exception:
            continue

print('end of import instrument index')
