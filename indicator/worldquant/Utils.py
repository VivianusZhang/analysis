import numpy
import talib


class Utils:

    @staticmethod
    def returns(close):
        roc = talib.ROC(close, 1)
        return roc

    @staticmethod
    def stddev(data, period):
        return numpy.std(data[:period])

    @staticmethod
    def signedPower(data, power):
        return numpy.power(data, power)

    @staticmethod
    def Ts_ArgMax(data, period):
        return data.size - data.index(max(data)) + 1


