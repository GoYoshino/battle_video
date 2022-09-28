from typing import List, Union

import numpy


class MockImageBuilder:

    def __init__(self):
        self.row = []

    def add(self, number_added: int, pixel: Union[int, List[int]]):
        assert isinstance(pixel, int) or len(pixel) == 3
        for i in range(number_added):
            self.row.append(pixel)

    def __len__(self) -> int:
        return len(self.row)

    def to_image(self) -> numpy.ndarray:
        return numpy.array([self.row])

    def reset(self):
        self.row = []
