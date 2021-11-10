import os
import logging
import sys

from trader import Trader
from trader import Processor

IB_GATEWAY_HOST = os.environ["IB_GATEWAY_HOST"]
IB_GATEWAY_PORT = int(os.environ["IB_GATEWAY_PORT"])
CLIENT_ID = 888


logger = logging.getLogger(__name__)


def main():
    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="%(asctime)s:%(levelname)s:%(module)s: %(message)s",
    )
    tick_processor = Processor(seconds=2)
    trader = Trader(
        IB_GATEWAY_HOST, IB_GATEWAY_PORT, CLIENT_ID, tick_processor=tick_processor
    )
    try:
        trader.start()
    except KeyboardInterrupt as ex:
        logger.info("KeyboardInterrupt")
        trader.disconnect()


if __name__ == "__main__":
    main()
