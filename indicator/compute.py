import functools
from datetime import datetime

import pymongo
from pymongo import MongoClient

from indicator.gtja.gtja import *
from indicator.ta import overlap
from indicator.ta.label import *
from indicator.ta.momentum import *
from utils.MongoUtils import find_by_code_on_and_after

client = MongoClient('localhost', 27017)
db = client['stock']


def compute_gtja(date):
    cursor = db.instrument.find({'industry': 'industry'})
    cursor = [{'code':'002230'}]
    for document in cursor:
        code = document['code']

        data = find_by_code_on_and_after(code, date)
        for i, row in data.iterrows():
            ret = data.iloc[[i]]
            ret['gtja_110'] = gtja_110(code, row.datetime)
            ret['gtja_9'] = gtja_9(code, row.datetime)
            ret['gtja_2'] = gtja_2(code, row.datetime)
            ret['gtja_97'] = gtja_97(code, row.datetime)
            ret['gtja_68'] = gtja_68(code, row.datetime)
            ret['gtja_31'] = gtja_31(code, row.datetime)
            ret['gtja_29'] = gtja_29(code, row.datetime)
            ret['gtja_80'] = gtja_80(code, row.datetime)
            ret['gtja_60'] = gtja_60(code, row.datetime)
            ret['gtja_71'] = gtja_71(code, row.datetime)
            ret['gtja_34'] = gtja_34(code, row.datetime)
            ret['gtja_57'] = gtja_57(code, row.datetime)
            ret['gtja_88'] = gtja_88(code, row.datetime)
            ret['gtja_14'] = gtja_14(code, row.datetime)
            ret['gtja_81'] = gtja_81(code, row.datetime)
            ret['gtja_18'] = gtja_18(code, row.datetime)
            ret['gtja_95'] = gtja_95(code, row.datetime)
            ret['gtja_11'] = gtja_11(code, row.datetime)
            ret['gtja_78'] = gtja_78(code, row.datetime)
            ret['gtja_70'] = gtja_70(code, row.datetime)
            ret['gtja_82'] = gtja_82(code, row.datetime)
            ret['gtja_96'] = gtja_96(code, row.datetime)
            ret['gtja_20'] = gtja_20(code, row.datetime)
            ret['gtja_46'] = gtja_46(code, row.datetime)
            ret['gtja_24'] = gtja_24(code, row.datetime)
            ret['gtja_109'] = gtja_109(code, row.datetime)
            ret['gtja_158'] = gtja_158(code, row.datetime)
            ret['gtja_126'] = gtja_126(code, row.datetime)
            ret['gtja_100'] = gtja_100(code, row.datetime)
            ret['gtja_153'] = gtja_153(code, row.datetime)
            ret['gtja_139'] = gtja_139(code, row.datetime)
            ret['gtja_106'] = gtja_106(code, row.datetime)
            ret['gtja_178'] = gtja_178(code, row.datetime)
            ret['gtja_134'] = gtja_134(code, row.datetime)
            ret['gtja_188'] = gtja_188(code, row.datetime)
            ret['gtja_189'] = gtja_189(code, row.datetime)
            ret['gtja_171'] = gtja_171(code, row.datetime)
            ret['gtja_132'] = gtja_132(code, row.datetime)
            db.ratio.insert_many(ret.to_dict('records'))


def compute_indicators():
    for value in db.instrumentDailyData.distinct('code'):

        data = list(db.instrumentDailyData.find({'code': value}, {'_id': 0, 'amount': 0, 'label': 0}).sort('date',
                                                                                                           pymongo.ASCENDING))
        # ignore IPO
        if len(data) < 50:
            continue

        if db.ratio.find({'code': value}).count() > 0:
            continue

        print('------starting-----------' + value)

        feed = functools.reduce(lambda x, y: {key: np.append(x[key], [y[key]]) for key in x}, data,
                                {'close': np.array([]), 'high': np.array([]), 'low': np.array([]), 'open': np.array([]),
                                 'volume': np.array([])})

        for value in data:
            value['ratio_open'] = value['close'] - value['open']
            value['ratio_high'] = value['close'] - value['high']
            value['ratio_low'] = value['close'] - value['low']

        ret = pd.DataFrame(data)

        close_ma = overlap.compute_ma_indicator(feed['close'], False)
        close_ma.rename(columns=dict(zip(close_ma.columns, map(lambda x: 'close_' + x, close_ma.columns))),
                        inplace=True)

        bb = overlap.compute_bb(feed['close'], False)
        performance = compute_performance(feed['close'], False)
        rsi = compute_rsi(feed['close'], False)
        di = compute_di(feed['high'], feed['low'], feed['close'], feed['volume'])
        ret['obv'] = talib.OBV(feed['close'], feed['volume'])
        ret[bb.columns.values] = bb
        ret[close_ma.columns.values] = close_ma
        ret[performance.columns.values] = performance
        ret[rsi.columns.values] = rsi
        ret[di.columns.values] = di
        ret['cycle'] = talib.HT_DCPERIOD(feed['close'])
        ret['label'] = compute_label(data)

        if db.ratio.find({'code': value}).count() == 0:
            db.ratio.insert_many(ret.to_dict('records'))


if __name__ == '__main__':
    # compute_indicators()

    compute_gtja(datetime(2017, 3, 1, 0, 0, 0))
