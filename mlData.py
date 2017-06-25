import matplotlib.pyplot as plt
from  pymongo import MongoClient
from datetime import datetime
import pandas as pd
import numpy as np
import pymongo
import collections

client = MongoClient('localhost', 27017)
db = client['stock']

class initData:
    def __init__(self):
        pass

    def prepare_data(self):
        test_start_datetime = datetime(2016, 1, 1, 0, 0, 0)
        test_end_datetime = datetime(2017, 4, 1, 0, 0, 0)
        test_set, test_label = self.prepare_data_set('test.csv', test_start_datetime, test_end_datetime)

        validate_start_datetime = datetime(2017, 4, 1, 0, 0, 0)
        validate_end_datetime = datetime(2017, 6, 1, 0, 0, 0)
        validate_set, validate_label = self.prepare_data_set('validate.csv',validate_start_datetime, validate_end_datetime)
        return test_set, test_label, validate_set, validate_label

    def prepare_data_set(self, filename, startDatetime, endDatetime):
        data = list(db.ratio.find({'close_sma120': {'$ne': np.nan}, 'close_tema':{'$ne': np.nan},'label': {'$ne': 0},
                                   'date': {'$gte': startDatetime,
                                            '$lt':endDatetime}}))
        data = pd.DataFrame(data)
        data = data.dropna(thresh=1)
        #data.set_index(data['date'].values, inplace=True)
        stockIndex = self.prepare_index(startDatetime, endDatetime)
        #selected_data = pd.concat([data, stockIndex], axis=1, join='inner')

        selected_data = self.combine_index_dailydata(stockIndex, data)
        selected_data = self.compute_cor(selected_data)
        selected_data.to_csv(filename)

        label = selected_data['label'].values.astype(np.float32)

        selected_data = selected_data.drop(['label', 'date', '_id', 'code'], axis=1)
        selected_data = pd.DataFrame(selected_data).astype(np.float32)
        data_set = pd.DataFrame(selected_data).astype(np.float32).values
        return data_set , label

    def compute_cor(self, data):
        index_close = data['index_close'].as_matrix()
        close = data['close'].as_matrix()
        data['cor']= np.corrcoef(index_close, close)[0,1]
        return data

    def prepare_index(self, startDatetime, endDatetime):
        stockIndex = pd.DataFrame(list(db.index.find({'code': '000001', 'date': {'$gte': startDatetime, '$lt': endDatetime}},
                                                {'_id': 0, 'close': 1, 'close_sma5': 1, 'close_sma15': 1, 'close_sma30': 1,
                                                 'volume': 1, 'roc1': 1, 'roc2': 1, 'roc3': 1, 'date': 1,})))
        stockIndex = stockIndex.dropna(thresh=1)
        stockIndex.set_index(stockIndex['date'].values, inplace=True)
        stockIndex = stockIndex.drop('date', 1)
        stockIndex.rename(columns=dict(zip(stockIndex.columns, map(lambda x: 'index_' + x, stockIndex.columns))),
                     inplace=True)

        return stockIndex

    def combine_index_dailydata(self, stockIndex, dailydata):
        ret = []
        for id, data in dailydata.iterrows():
            try:
                indexData = stockIndex.loc[data['date']]
                data = data.append(indexData)
                ret.append(data)
            except Exception:
                continue

        return pd.DataFrame(ret).dropna(thresh=1)


