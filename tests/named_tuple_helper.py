from collections import namedtuple

MQLTradeResultNamedTuple = namedtuple('MQLTradeResultNamedTuple',
                                      'retcode deal order volume price bid ask comment request_id retcode_external',
                                      defaults = [10009, 0, 0, 0.0, 0.0, 0.0, 0.0, "", 1, 10009])

PositionNamedTuple = namedtuple('PositionNamedTuple',
                                      'profit symbol ticket type volume',
                                      defaults = [0, "", 1, 1, 1.0])