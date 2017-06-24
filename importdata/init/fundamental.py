from  pymongo import MongoClient
import pandas as pd
import tushare as ts


client = MongoClient()
client = MongoClient('localhost', 27017)
db = client['stock']

cursor = db.instrument.find({})
instrument = pd.DataFrame(list(cursor))

industry = ts.get_industry_classified()[['code', 'name']].rename(columns = {'name':'industry'})
#concept = ts.get_concept_classified()
area = ts.get_area_classified()[['code', 'name']].rename(columns = {'name': 'area'})
small_cap = ts.get_hs300s()[['code']]
small_cap['small'] = 'true'
gem = ts.get_gem_classified()[['code']]
gem['gem'] = 'true'
hs = ts.get_hs300s()[['code']]
hs['hs300'] = 'true'
#sz = ts.get_sz50s()
#zz = ts.get_zz500s()
#ts.get_terminated()
#ts.get_suspended()

data = pd.merge(instrument, industry, on='code')
data = pd.merge(data, area, on= 'code')
data = pd.merge(data, gem, on = 'code')

db.test.insert_many(data.to_dict('records'))