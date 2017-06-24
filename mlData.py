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
        data = list(db.ratio.find({'close_sma120': {'$ne': np.nan}, 'label': {'$ne': 0},
                                   'date': {'$gte': datetime(2016, 01, 01, 0, 0, 0),
                                            '$lt': datetime(2017, 04, 01, 0, 0, 0)}}))
        data = pd.DataFrame(data)
        stockIndex = self.prepare_index(datetime(2016, 01, 01, 0, 0, 0), datetime(2017, 04, 01, 0, 0, 0))
        data = self.combine_index_dailydata(stockIndex, data)

        selected_data = data.drop(['label', 'date', '_id'], axis=1)
        test_set = selected_data.values
        test_label = data['label'].values

        validate_data = list(db.ratio.find({'label': {'$ne': 0}, 'close_sma120': {'$ne': np.nan},
                                            'date': {'$gte': datetime(2017, 04, 01, 0, 0, 0)}}))
        validate_data = pd.DataFrame(validate_data)
        validate_stockIndex = self.prepare_index(datetime(2017, 04, 01, 0, 0, 0), datetime(2017, 06, 01, 0, 0, 0))
        validate_data = self.combine_index_dailydata(validate_stockIndex, validate_data)

        selected_validate_data = validate_data.drop(['label', 'date', '_id'], axis=1)
        validate_set = selected_validate_data.values
        validate_label = validate_data['label'].values
        return test_set, test_label, validate_set, validate_label


    def prepare_index(self, startDatetime, endDatetime):
        stockIndex = pd.DataFrame(list(db.index.find({'code': '000001', 'date': {'$gte': startDatetime, '$lt': endDatetime}},
                                                {'_id': 0, 'close': 1, 'close_sma5': 1, 'close_sma15': 1, 'close_sma30': 1,
                                                 'volume': 1, 'roc1': 1, 'roc2': 1, 'roc3': 1, 'date': 1})))
        stockIndex.set_index(stockIndex['date'].values, inplace=True)
        stockIndex = stockIndex.drop('date', 1)
        stockIndex.rename(columns=dict(zip(stockIndex.columns, map(lambda x: 'index_' + x, stockIndex.columns))),
                     inplace=True)


        # data = test_index['close_sma5'].as_matrix()
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

        return pd.DataFrame(ret)



