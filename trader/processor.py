import logging
import time
from threading import Thread
from .models.ticker import Ticker

logger = logging.getLogger(__name__)


class Processor:
    def __init__(self):
        self.tickers = {}
        self.last_tick = None
        self.start_checked_thread()

    def process_tick(self, req_id, tick_type, price, attrib, timestamp):
        self.last_tick = timestamp
        start_time = time.time()
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

        self.tickers[req_id].tick(price, timestamp)

        logger.info(
            "processed %d tickers in %d seconds",
            len(self.tickers),
            time.time() - start_time,
        )

    def add_ticker(self, ticker: Ticker) -> None:
        self.tickers[ticker.req_id] = ticker

    def _bar_checker(self):
        """check whether bars need to be created"""
        while True:
            time.sleep(1)
            if not self.last_tick:
                continue
            try:
                for _, t in self.tickers.items():
                    t.bar_checker()
            except Exception as ex:
                logger.exception(ex)

        logger.error("bar_checker exited")

    def start_checked_thread(self):
        """start thread to check for new bars"""
        self.bar_checker_thread = Thread(target=self._bar_checker)
        self.bar_checker_thread.start()
