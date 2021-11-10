import logging
from .models.bar import Bar

logger = logging.getLogger(__name__)


class Processor:
    def __init__(self, seconds):
        self.bars = []
        self.seconds = seconds

    def process_tick(self, req_id, tick_type, price, attrib):
        logger.info(
            "process_tick: req_id: %s tick_type: %s price: %s attrib: %s",
            req_id,
            tick_type,
            price,
            attrib,
        )
        if tick_type == 2:
            # ask
            pass
        self._tick(price)
        logger.info("processor = %r", self)

    def _tick(self, price):
        logger.info("_tick processing %s", price)
        if len(self.bars) == 0:
            self.bars.append(Bar(seconds=self.seconds, o=price))
        resp = self.bars[-1].tick(price)
        if not resp:
            self.bars.append(Bar(seconds=self.seconds, o=price))
            self.bars[-1].tick(price)

    def __repr__(self):
        return "Processor(seconds={}, bars={})".format(self.seconds, self.bars)
