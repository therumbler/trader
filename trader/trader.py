from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract

import os
import threading
import time

import logging

logger = logging.getLogger(__name__)


class IBApi(EWrapper, EClient):
    def __init__(self, market_data_type=1):
        EClient.__init__(self, self)
        self.reqMarketDataType = market_data_type

    def tickPrice(self, reqId, tickType, price, attrib):
        if tickType == 2 and reqId == 1:
            print("The current ask price is: ", price)


class Trader:
    def __init__(self, ib_gateway_host, ib_gateway_port, client_id):
        self.api = IBApi(market_data_type=3)
        # self.api.client_trader.reqMarketDataType = 1

        self.ib_gateway_host = ib_gateway_host
        self.ib_gateway_port = ib_gateway_port
        self.client_id = client_id

    #

    @staticmethod
    def create_contract(symbol, sec_type, exchange, currency, prim_exch=None):
        # Create contract object
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
        self.api.connect(self.ib_gateway_host, self.ib_gateway_port, self.client_id)
        api_thread = threading.Thread(target=self.api.run, daemon=True)
        api_thread.start()

        time.sleep(1)  # Sleep interval to allow time for connection to server

        # contract = self.create_contract(
        #     symbol="AAPL", sec_type="STK", exchange="SMART", currency="USD"
        # )
        contract = self.create_contract(
            symbol="EUR", sec_type="CASH", exchange="IDEALPRO", currency="USD"
        )
        # Request Market Data
        tick_type = ""
        unsubscribed_snapshot = False
        subscribed_snapshot = False
        request_id = 1
        self.api.reqMktData(
            request_id,
            contract,
            tick_type,
            unsubscribed_snapshot,
            subscribed_snapshot,
            [],
        )

        time.sleep(10)  # Sleep interval to allow time for incoming price data
        self.api.disconnect()
