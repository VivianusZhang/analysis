import talib
import numpy

class utils:

    @staticmethod
    def returns(self, close):
        return talib.ROC(close, 1)

    @staticmethod
    def stddev(self, data, period):
        return numpy.std(data[:period])

    @staticmethod
    def signedPower(self, data, power):
        return numpy.power(data, power)

    @staticmethod
    def Ts_ArgMax(self, data):
        return data.size - data.index(max(data)) + 1