from dataclasses import dataclass, field
import logging
import time


logger = logging.getLogger(__name__)


@dataclass
class Bar:
    """
    A bar is a unit of time.
    """

    seconds: int
    o: float
    h: float = 0.0
    l: float = 99999999999999999999
    c: float = 0.0
    timestamp: int = field(default_factory=time.time)

    def tick(self, price: float) -> None:
        """
        Update the bar with a new tick.
        """
        if time.time() - self.timestamp > self.seconds:
            logger.info("time expired")
            return
        self.c = price

        if price > self.h:
            self.h = price
        if price < self.l:
            self.l = price
