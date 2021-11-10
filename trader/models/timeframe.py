import logging
import time

from .bar import Bar

logger = logging.getLogger(__name__)


class Timeframe:
    def __init__(self, seconds):
        self.bars = []
        self.seconds = seconds
        self.last_tick = time.time()

    def tick(self, price, timestamp):
        self.last_tick = timestamp
        # logger.info("Timeframe tick %s", price)
        if len(self.bars) == 0:
            self.bars.append(Bar(seconds=self.seconds, o=price))
        resp = self.bars[0].tick(price)
        if not resp:
            self.bars.insert(0, Bar(seconds=self.seconds, o=price))
            self.bars[0].tick(price)
        # logger.info("Timeframe %s", self)

    def should_close_last_bar(self):
        """runs a thread to close a bar if needed"""
        pass

    def bar_checker(self):
        if len(self.bars) == 0:
            return
        if self.bars[0].should_close():
            logger.info("closed bar %s", self.bars[0])
            self.bars.insert(0, Bar(seconds=self.seconds, o=0.0))

    def __repr__(self):
        return "Timeframe(seconds={}, bar_count={})".format(
            self.seconds, len(self.bars)
        )
