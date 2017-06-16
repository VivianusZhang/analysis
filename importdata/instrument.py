import tushare as ts
from  pymongo import MongoClient

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']

df = ts.get_stock_basics()
df['code'] = df.index
db.instrument.insert_many(df.to_dict('records'))

print('end of import instrument data')
