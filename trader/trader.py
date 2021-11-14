
from ibapi.contract import Contract

import logging
import random
import time
import threading

from .ibapi import IBApi
from .processor import Processor


logger = logging.getLogger(__name__)


class Trader:
    def __init__(
        self, ib_gateway_host, ib_gateway_port, client_id, tick_processor, tickers, real=True
    ):
        self.tick_processor: Processor = tick_processor
        self.api = IBApi(market_data_type=3, tick_processor=self.tick_processor)
        self.ib_gateway_host = ib_gateway_host
        self.ib_gateway_port = ib_gateway_port
        self.client_id = client_id
        self.tickers = tickers
        self.real = real

    @staticmethod
    def create_contract(symbol, sec_type, exchange, currency, prim_exch=None):
        """Create contract object"""
        contract = Contract()
        contract.symbol = symbol
        contract.secType = sec_type
        contract.exchange = exchange
        contract.currency = currency
        if prim_exch:
            contract.primaryExchange = prim_exch

        return contract


    def _fake_things(self):
        timestamp = 1000
        counter = 0
        while True:
            price = random.uniform(1.4, 1.5)
            self.tick_processor.process_tick(1, 2, price, {}, timestamp)
            counter += 1
            if counter == 5:
                counter = 0
                timestamp += 1
                time.sleep(0.1)

    def _start_real(self):
        logger.info("waiting 10 seconds before connecting...")
        time.sleep(10)
        self.api.connect(self.ib_gateway_host, self.ib_gateway_port, self.client_id)
        thread = threading.Thread(target=self.api.run, daemon=True)
        thread.start()
        return thread

    def _start_fake(self):
        thread = threading.Thread(target=self._fake_things, daemon=True)
        thread.start()
        return thread

    def start(self):
        """ Start the socket in a thread"""
        if self.real:
            thread = self._start_real()
            time.sleep(1) 
        else:
            thread = self._start_fake()
         # Sleep interval to allow time for connection to server
        logger.info("requesting some data...")
        for ticker in self.tickers:
            self.request_market_data(
                request_id=ticker.req_id,
                symbol=ticker.symbol,
                sec_type=ticker.sec_type,
                exchange=ticker.exchange,
                currency=ticker.currency,
            )
        
        thread.join()

    def request_market_data(
        self, request_id, symbol, sec_type, exchange, currency, prim_exch=None
    ):
        contract = self.create_contract(
            symbol=symbol,
            sec_type=sec_type,
            exchange=exchange,
            currency=currency,
            prim_exch=prim_exch,
        )
        # Request Market Data
        tick_type = ""
        unsubscribed_snapshot = False  # no market data subscription yet
        subscribed_snapshot = False
        self.api.reqMktData(
            request_id,
            contract,
            tick_type,
            unsubscribed_snapshot,
            subscribed_snapshot,
            [],
        )

    def disconnect(self):
        self.api.disconnect()
