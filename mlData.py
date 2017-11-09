# -*- coding:utf-8 -*-

from datetime import datetime

import numpy as np
import pandas as pd
from  pymongo import MongoClient

from indicator.ta.label import compute_label_rank
from utils.MongoUtils import find_instument_by_industry, find_raito_by_code_list_between

client = MongoClient('localhost', 27017)
db = client['stock']


class initData:
    def __init__(self):
        pass

    def prepare_data(self, industry):
        test_start_datetime = datetime(2016, 1, 1, 0, 0, 0)
        test_end_datetime = datetime(2017, 3, 1, 0, 0, 0)

        test_set, test_label = self.prepare_data_set('test.csv', industry, test_start_datetime, test_end_datetime)

        validate_start_datetime = datetime(2017, 3, 1, 0, 0, 0)
        validate_end_datetime = datetime(2017, 10, 1, 0, 0, 0)
        validate_set, validate_label = self.prepare_data_set('validate.csv', industry, validate_start_datetime,
                                                             validate_end_datetime)
        return test_set, test_label, validate_set, validate_label

    def prepare_data_set(self, filename, industry, start_date, end_date):
        print ('start to prepare data from %s to %s' % (start_date, end_date))

        instruments = find_instument_by_industry(industry)

        ratio = find_raito_by_code_list_between(instruments.code.tolist(), start_date, end_date)
        ratio = ratio.dropna(axis=0)
        ratio['label'] = np.NAN
        ratio.drop(['_id'], 1, inplace=True)

        data_set = pd.DataFrame()
        for date in ratio.datetime.unique():
            data_set = data_set.append(compute_label_rank(ratio.loc[ratio['datetime'] == date]), ignore_index=True)

        data_set.drop(['datetime'], 1, inplace=True)
        # only select open high low close volume
        # {'_id': 0, 'close': 1, 'open': 1, 'high': 1, 'low': 1, 'date': 1, 'volume': 1, 'code': 1, 'label': 1}
        data_set = data_set.dropna(axis=0)

        # data.set_index(data['date'].values, inplace=True)

        # selected_data = pd.concat([data, stockIndex], axis=1, join='inner')
        # selected_data = self.compute_cor(selected_data)
        data_set.to_csv(filename)
        label = data_set.label.tolist()
        data_set.drop(['label'], 1, inplace=True)
        data_set = data_set.apply(pd.to_numeric).to_dict('records')

        ret = []
        for _ in data_set:
            ret.append(_.values())

        print ('end to prepare data from %s to %s' % (start_date, end_date))
        return ret, label

    def compute_cor(self, data):
        index_close = data['index_close'].as_matrix()
        close = data['close'].as_matrix()
        data['cor'] = np.corrcoef(index_close, close)[0, 1]
        return data

    def prepare_index(self, startDatetime, endDatetime):
        # stockIndex = pd.DataFrame(
        #     list(db.index.find(
        #         {'code': '000001', 'date': {'$gte': startDatetime, '$lt': endDatetime}, 'label': {'$ne': -1}},
        #         {'_id': 0, 'close': 1, 'close_sma5': 1, 'close_sma15': 1, 'close_sma30': 1,
        #          'volume': 1, 'roc1': 1, 'roc2': 1, 'roc3': 1, 'date': 1, })))

        stockIndex = pd.DataFrame(
            list(db.index.find(
                {'code': '000001', 'date': {'$gte': startDatetime, '$lt': endDatetime}, 'label': {'$ne': -1}})))

        stockIndex = stockIndex.dropna(axis=0)
        stockIndex.set_index(stockIndex['date'].values, inplace=True)
        stockIndex.drop(['date', '_id'], 1, inplace=True)
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
