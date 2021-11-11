import logging
import math
import time
from threading import Thread
from .models.timeframe import Timeframe

logger = logging.getLogger(__name__)


class Processor:
    def __init__(self, seconds):
        self.timeframes = []
        self.seconds = seconds
        self.create_timeframes()
        self.last_tick = None
        self.start_checked_thread()

    def process_tick(self, req_id, tick_type, price, attrib, timestamp):
        self.last_tick = timestamp
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

        for timeframe in self.timeframes:
            timeframe.tick(price, timestamp)
        logger.info(
            "processed %d timeframes in %d seconds",
            len(self.timeframes),
            time.time() - timestamp,
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

    def _bar_checker(self):
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

    def start_checked_thread(self):
        """start thread to check for new bars"""
        self.bar_checker_thread = Thread(target=self._bar_checker)
        self.bar_checker_thread.start()
