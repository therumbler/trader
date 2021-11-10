import logging
import time

from .bar import Bar

logger = logging.getLogger(__name__)

MAX_BARS = 100


class Timeframe:
    def __init__(self, seconds):
        self.bars = []
        self.seconds = seconds
        self.last_tick = time.time()

    def tick(self, price, timestamp):
        self.last_tick = timestamp
        # logger.info("Timeframe tick %s", price)
        if len(self.bars) == 0:
            self.bars.append(self.new_bar(price))
        resp = self.bars[0].tick(price)
        if not resp:
            self.bars.insert(0, self.new_bar(price))
            self.bars[0].tick(price)
        logger.info("Timeframe %r", self)

    def new_bar(self, price):
        if price:
            return Bar(seconds=self.seconds, o=price, c=price, h=price, l=price)
        else:
            return Bar(seconds=self.seconds, o=price, c=price)

    def trim_bars(self) -> None:
        if len(self.bars) > MAX_BARS:
            self.bars = self.bars[:MAX_BARS]

    def bar_checker(self):
        if len(self.bars) == 0:
            return
        if self.bars[0].should_close():
            # logger.info("closed %s", self.bars[0])
            self.bars.insert(0, self.new_bar(0.0))
            self.trim_bars()

    def highest_high(self):
        price = max(self.bars, key=lambda x: x.h).h
        index = self.bars.index([b for b in self.bars if b.h == price][0])
        # logger.info("highest_high index = %d", index)
        return {"index": index, "price": price}

    def lowest_low(self):
        price = min(self.bars, key=lambda x: x.l).l
        index = self.bars.index([b for b in self.bars if b.l == price][0])
        # logger.info("lowest_low index = %d", index)
        return {"index": index, "price": price}

    def stats(self):
        return {"highest_high": self.highest_high(), "lowest_low": self.lowest_low()}

    def __repr__(self):
        return "Timeframe(seconds={}, bar_count={} stats={})".format(
            self.seconds, len(self.bars), self.stats()
        )
