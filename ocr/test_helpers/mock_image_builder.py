from typing import List

import numpy


class MockImageBuilder:

    def __init__(self):
        self.row = []

    def add(self, number_added: int, pixel: List[int]):
        assert len(pixel) == 3
        for i in range(number_added):
            self.row.append(pixel)

    def __len__(self) -> int:
        return len(self.row)

    def to_image(self) -> numpy.ndarray:
        return numpy.array([self.row])
