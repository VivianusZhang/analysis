import pymongo
import tushare as ts
from  pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']

cons = ts.get_apis()

db.instrumentHourData.create_index([('code', pymongo.ASCENDING)])

code = '002230'
hourlyData = ts.bar(code, conn=cons, freq='1min', start_date='2017-10-31', end_date='2017/10/31')
hourlyData['code'] = code
hourlyData['volume'] = hourlyData['vol']
hourlyData.drop('vol', 1)
hourlyData['date'] = hourlyData.index
db.instrumentHourData.insert_many(hourlyData.to_dict('records'))

print 'end'
