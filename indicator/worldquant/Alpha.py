import pandas

from indicator.MongoUtils import *


class Alpha:
    @staticmethod
    def alpha_001(enddate, index):

        codes = MongoUtils.find_instrument_list()

        dic = {}
        for code in codes:
            close = MongoUtils.find_close_on_or_before(code, enddate, 21)

            if close[:1] < 0:
                signed_power_data = Utils.stddev(Utils.returns(close), 20)
            else:
                signed_power_data = close[0]

            dic[code] = Utils.Ts_ArgMax(Utils.signedPower(signed_power_data, 2), 5)

        df = pandas.DataFrame.from_dict(dic.items(), columns=['code', 'value']).sort_values(['value'], inplace=True)

        df.loc(df['code'] == index)
