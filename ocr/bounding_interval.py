from abc import ABCMeta, abstractmethod


class IBoundingInterval(metaclass=ABCMeta):

    def __init__(self, low: float, high: float):
        assert low < high
        self.low = low
        self.high = high

class BoundingInterval(IBoundingInterval):
    """
    Boundingboxの1次元版。1次元の値のみを考慮する。
    """

    def __init__(self, low: float, high: float):
        super().__init__(low, high)

    def length(self) -> float:
        return self.high - self.low

    def get_coverage(self, container: IBoundingInterval) -> float:
        low = max(self.low, container.low)
        high = min(self.high, container.high)

        if high < low:
            return 0.0

        intersection = high - low

        coverage = intersection / self.length()
        assert coverage >= 0.0
        return coverage

    def transposed(self, amount: float):
        return BoundingInterval(self.low + amount, self.high + amount)

    def __repr__(self):
        return f"[{self.low}, {self.high}]"
