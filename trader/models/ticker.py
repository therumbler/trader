import logging
import math
import time
from threading import Thread
from .timeframe import Timeframe

logger = logging.getLogger(__name__)


class Ticker:
    def __init__(self, req_id, symbol, sec_type, exchange, currency):
        self.req_id = req_id
        self.symbol = symbol
        self.sec_type = sec_type
        self.exchange = exchange
        self.currency = currency

        self.timeframes = []
        self.create_timeframes()
        self.last_tick = None

    def tick(self, price, timestamp):
        self.last_tick = timestamp
        start = time.time()
        for timeframe in self.timeframes:
            timeframe.tick(price, timestamp)
        logger.info(
            "processed %d timeframes in %d seconds",
            len(self.timeframes),
            time.time() - start,
        )

    def create_timeframes(self):
        seconds = 1
        for i in range(120):
            self.timeframes.append(Timeframe(seconds=seconds))
            new_seconds = int(seconds * 1.06)
            if new_seconds == seconds:
                seconds = new_seconds + 1
            else:
                seconds = new_seconds

    def bar_checker(self):
        """check whether bars need to be created"""
        while True:
            time.sleep(1)
            if not self.last_tick:
                continue
            try:
                for t in self.timeframes:
                    t.bar_checker()
            except Exception as ex:
                logger.exception(ex)

        logger.error("bar_checker exited")

