import logging as log
import pickle

from hyperloglog import HyperLogLog


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


if __name__ == "__main__":
    log.basicConfig(format="%(asctime)s %(levelname)s"
                    " [%(module)s/%(funcName)s]"
                    " (%(processName)s) %(message)s",
                    level=log.DEBUG)

    hll = HyperLogLogEventCounter(0.005, f"HLL-0")

    print(type(hll))
    dump = pickle.dumps(hll)
    hll_deser = pickle.loads(dump)
    print(type(hll_deser))

    # this works fine
    hll.add("test")
    # this fails
    hll_deser.add("test")
