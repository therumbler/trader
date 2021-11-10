import os
import logging
import sys

from trader import Trader

IB_GATEWAY_HOST = os.environ["IB_GATEWAY_HOST"]
IB_GATEWAY_PORT = int(os.environ["IB_GATEWAY_PORT"])
CLIENT_ID = 888


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    trader = Trader(IB_GATEWAY_HOST, IB_GATEWAY_PORT, CLIENT_ID)
    trader.start()


if __name__ == "__main__":
    main()
