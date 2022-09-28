from unittest import TestCase

from ocr.bounding_interval import BoundingInterval


class BoundingIntervalTest(TestCase):

    def refuses_zero_boundingbox(self):
        with self.assertRaises(AssertionError):
            BoundingInterval(0.0, 0.0)

    def test_same(self):
        contained = BoundingInterval(0.0, 100.0)
        container = BoundingInterval(0.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 1.0)

    def test_completely_contained(self):
        contained = BoundingInterval(0.0, 100.0)
        container = BoundingInterval(-1.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 1.0)

    def test_extruding(self):
        contained = BoundingInterval(-20.0, 120.0)
        container = BoundingInterval(0.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 100.0 / 140.0)

    def test_out_of_bound(self):
        contained = BoundingInterval(-100.0, 0.0)
        container = BoundingInterval(0.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 0.0)

    # 実際のユースケースに近い
    def test_barely_intersecting(self):
        contained = BoundingInterval(48.0, 97.0)
        container = BoundingInterval(49.0, 98.0)

        self.assertAlmostEqual(contained.get_coverage(container), 0.9795918367346939)
