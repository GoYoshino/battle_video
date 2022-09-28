from unittest import TestCase

from ocr.preprocess.classifier import classify_by_color
from ocr.test_helpers.mock_image_builder import MockImageBuilder


class ColorClassifierTest(TestCase):

    def test_counts_at_zero_tolerance(self):
        im = MockImageBuilder()
        im.add(7, [10, 20, 30])
        im.add(4, [100, 150, 200])
        self.assertAlmostEqual(7.0 / len(im), classify_by_color(im.to_image(), [(10, 20, 30)], 0))

    def test_counts_with_tolerance(self):
        im = MockImageBuilder()
        im.add(2, [10, 20, 30])
        im.add(4, [9, 19, 29])
        im.add(8, [11, 21, 31])
        im.add(16, [8, 18, 28])

        self.assertAlmostEqual((2.0 + 4.0 + 8.0) / len(im), classify_by_color(im.to_image(), [(10, 20, 30)], 1))

    def test_calculates_sum(self):
        im = MockImageBuilder()
        im.add(2, [10, 20, 30])
        im.add(4, [100, 200, 300])

        self.assertAlmostEqual(1.0, classify_by_color(im.to_image(), [(10, 20, 30), (100, 200, 300)], 0))

    def test_cuts_off_overlap(self):
        im = MockImageBuilder()
        im.add(2, [10, 20, 30])
        im.add(4, [20, 30, 40])

        self.assertAlmostEqual(1.0, classify_by_color(im.to_image(), [(10, 20, 30)], 20))
