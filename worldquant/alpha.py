from mongoUtils import *
from .utils import *
import pymongo

class alpha:
    def alpha_101(enddate, index):
        close = mongoUtils.findCloseOnorBofore(index, enddate, 21)

        utils.returns(close[:1]) < 0?utils.stddev(utils.returns(close , 20) : close[0])

        (rank(
            Ts_ArgMax(
                SignedPower(
                    ((returns < 0) ? stddev(returns, 20): close)
                    , 2.)
                , 5)
            )
        - 0.5)
