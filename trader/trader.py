from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import os
import threading
import time

import logging

logger = logging.getLogger(__name__)


class IBApi(EWrapper, EClient):
    def __init__(self, tick_processor, market_data_type=1):
        EClient.__init__(self, self)
        self.tick_processor = tick_processor
        self.reqMarketDataType = market_data_type

    def tickPrice(self, reqId, tickType, price, attrib):
        timestamp = time.time()
        self.tick_processor.process_tick(reqId, tickType, price, attrib, timestamp)


class Trader:
    def __init__(self, ib_gateway_host, ib_gateway_port, client_id, tick_processor):
        self.api = IBApi(market_data_type=3, tick_processor=tick_processor)
        self.ib_gateway_host = ib_gateway_host
        self.ib_gateway_port = ib_gateway_port
        self.client_id = client_id

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

    def start(self):
        """ Start the socket in a thread"""
        logger.info("waiting 10 seconds before connecting...")
        time.sleep(10)
        self.api.connect(self.ib_gateway_host, self.ib_gateway_port, self.client_id)
        api_thread = threading.Thread(target=self.api.run, daemon=True)
        api_thread.start()

        time.sleep(1)  # Sleep interval to allow time for connection to server
        logger.info("requesting some data...")
        self.request_market_data(
            request_id=1,
            symbol="EUR",
            sec_type="CASH",
            exchange="IDEALPRO",
            currency="USD",
        )
        # self.request_market_data(
        #     request_id=2,
        #     symbol="AAPL",
        #     sec_type="STK",
        #     exchange="SMART",
        #     currency="USD",
        # )
        api_thread.join()

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
