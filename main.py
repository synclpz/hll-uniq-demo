import logging as log
import dill
import pickle
from random import randint
from string import ascii_letters

from hyperloglog import HyperLogLog
from pathos.multiprocessing import ProcessingPool as Pool


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
        self.count = 0
        self.name = name
        super(HyperLogLogEventCounter, self).__init__(error_rate)

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
        log.debug(f"Count: {hll.count}, "
                  f"current value: {value}, "
                  f"cardinality: {len(hll)}")


def fill_hll(hll: HyperLogLogEventCounter, max_count, size):
    [
        add_print100000(
            hll, "".join([
                ascii_letters[randint(0,
                                      len(ascii_letters) - 1)]
                for n in range(size)
            ])) for m in range(max_count)
    ]


if __name__ == "__main__":
    log.basicConfig(format="%(asctime)s %(levelname)s"
                    " [%(module)s/%(funcName)s]"
                    " (%(processName)s) %(message)s",
                    level=log.DEBUG)
    num_processes = 1
    num_hlls = 1
    num_events = 500000
    record_size = 3

    pool = Pool(num_processes)

    log.info(f"Creating {num_hlls} HLLs...")
    hlls = [
        HyperLogLogEventCounter(0.005, f"HLL-{i}") for i in range(num_hlls)
    ]

    print(type(hlls[0]))
    dump = dill.dumps(hlls[0])
    p_dump = pickle.dumps(hlls[0])
    hll_deser = dill.loads(dump)
    p_hll_deser = pickle.loads(p_dump)
    print(type(hll_deser))
    print(type(p_hll_deser))

    #дальше не смотри

    #log.info("Starting processes...")
    #with pool:
    #    pool.map(fill_hll, [hll for hll in hlls], [num_events] * len(hlls),
    #             [record_size] * len(hlls))

    #log.info("Done")
