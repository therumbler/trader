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
    first_tick: int = field(default_factory=time.time)
    closed: bool = False

    def tick(self, price: float) -> None:
        """
        Update the bar with a new tick.
        """
        if self.should_close():
            return None
        self.c = price
        if not self.o:
            self.o = price

        if price > self.h:
            self.h = price
        if price < self.l:
            self.l = price
        return self

    def should_close(self) -> bool:
        """
        Check if the bar should be closed.
        """
        if time.time() - self.first_tick > self.seconds:
            # logger.info("time expired for %d", self.seconds)
            self.closed = True
            return True
        return False
