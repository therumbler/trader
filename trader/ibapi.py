from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import time

class IBApi(EWrapper, EClient):
    def __init__(self, tick_processor, market_data_type=1):
        EClient.__init__(self, self)
        self.tick_processor = tick_processor
        self.reqMarketDataType = market_data_type

    def tickPrice(self, reqId, tickType, price, attrib):
        timestamp = time.time()
        self.tick_processor.process_tick(reqId, tickType, price, attrib, timestamp)