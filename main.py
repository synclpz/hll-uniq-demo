from hyperloglog import HyperLogLog
from random import randint
from string import digits
import logging
import multiprocessing as mp


class HyperLogLogEventCounter(HyperLogLog):
    """
    HyperLogLog cardinality counter with event counter
    """
    def __init__(self, error_rate, name):
        """
        Create a HyperLogLog with event counter

         Keyword arguments:
        error_rate -- desired maximum error rate
        name -- object name for reference
        """
        super(HyperLogLogEventCounter, self).__init__(error_rate)
        self.count = 0
        self.name = name

    def add(self, value):
        """
        Add the item to the HyperLogLog and count event
        """
        self.count += 1
        return super(HyperLogLogEventCounter, self).add(value)


def add_print100000(hll: HyperLogLogEventCounter, value):
    """
    Add value to hll HyperLogLog and prints every 100000 count
    """
    hll.add(value)
    if not hll.count % 100000:
        logging.debug(f"Count: {hll.count}, "
                      f"current value: {value}, "
                      f"cardinality: {len(hll)}")


def fill_hll(hll: HyperLogLogEventCounter, max_count):
    [
        add_print100000(
            hll,
            "".join([digits[randint(0,
                                    len(digits) - 1)] for n in range(4)]))
        for m in range(max_count)
    ]


if __name__ == "__main__":
    logging.basicConfig(format="%(asctime)s %(levelname)s"
                        " [%(module)s/%(funcName)s]"
                        " (%(processName)s) %(message)s",
                        level=logging.DEBUG)
    num_hlls = 8
    logging.info(f"Creating {num_hlls} HLLs...")
    hlls = [
        HyperLogLogEventCounter(0.005, f"HLL-{i}") for i in range(num_hlls)
    ]
    processes = [
        mp.Process(target=fill_hll,
                   args=(hll, 500000),
                   daemon=True,
                   name=f"Process for {hll.name}") for hll in hlls
    ]
    logging.info("Starting processes...")
    [process.start() for process in processes]
    [process.join() for process in processes]
    logging.info("Done")
