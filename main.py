import pickle

from hyperloglog import HyperLogLog


class HyperLogLogEventCounter(HyperLogLog):
    """
    HyperLogLog cardinality counter with event counter
    """

    __slots__ = HyperLogLog.__slots__ + ("count", "name")

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
    hll = HyperLogLogEventCounter(0.005, "HLL-0")

    [hll.add(i) for i in range(10000)]  # to test "non-new" object ser/deser
    print(type(hll))
    dump = pickle.dumps(hll)
    hll_deser = pickle.loads(dump)
    print(type(hll_deser))

    # this works fine
    hll.add("test")
    # this also works fine now
    hll_deser.add("test")
