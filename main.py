import json
import os
import logging
import sys

from trader import Trader
from trader import Processor
from trader.models.ticker import Ticker

IB_GATEWAY_HOST = os.environ["IB_GATEWAY_HOST"]
IB_GATEWAY_PORT = int(os.environ["IB_GATEWAY_PORT"])
CLIENT_ID = 888


logger = logging.getLogger(__name__)


def create_tickers():
    with open("config.json") as f:
        config = json.load(f)

    req_id = 1
    tickers = []
    for t in config["tickers"]:
        ticker = Ticker(
            req_id=req_id,
            symbol=t["symbol"],
            exchange=t["exchange"],
            currency=t["currency"],
            sec_type=t["sec_type"],
        )
        tickers.append(ticker)
        req_id += 1

    return tickers


def main():
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(module)s: %(message)s",
    )
    tickers = create_tickers()
    tick_processor = Processor()
    [tick_processor.add_ticker(ticker) for ticker in tickers]
    trader = Trader(
        IB_GATEWAY_HOST,
        IB_GATEWAY_PORT,
        CLIENT_ID,
        tick_processor=tick_processor,
        tickers=tickers,
    )
    try:
        trader.start()
    except KeyboardInterrupt as ex:
        logger.info("KeyboardInterrupt")
        trader.disconnect()


if __name__ == "__main__":
    main()
