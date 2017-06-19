import tushare as ts
from  pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']

ts.get_today_all()

df = ts.get_today_all()
df1 = df[['code', 'volume', 'high', 'low', 'date', 'close', 'open']]

print('start to import data on :' + df1.at[3, 'date'])
db.test.insert_many(df1.to_dict('records'))

