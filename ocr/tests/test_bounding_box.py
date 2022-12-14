from unittest import TestCase

from ocr.bounding_box import BoundingBox


class BoundingBoxTest(TestCase):

    def refuses_zero_boundingbox(self):
        with self.assertRaises(AssertionError):
            BoundingBox(0.0, 0.0, 1.0, 0.0)
        with self.assertRaises(AssertionError):
            BoundingBox(0.0, 0.0, 0.0, 1.0)

    def test_same(self):
        contained = BoundingBox(0.0, 0.0, 100.0, 100.0)
        container = BoundingBox(0.0, 0.0, 100.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 1.0)

    def test_completely_contained_x(self):
        contained = BoundingBox(0.0, 0.0, 100.0, 100.0)
        container = BoundingBox(-1.0, 0.0, 101.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 1.0)

    def test_completely_contained_y(self):
        contained = BoundingBox(0.0, 0.0, 100.0, 100.0)
        container = BoundingBox(0.0, -1.0, 100.0, 101.0)

        self.assertAlmostEqual(contained.get_coverage(container), 1.0)

    def test_completely_contained_xy(self):
        contained = BoundingBox(0.0, 0.0, 100.0, 100.0)
        container = BoundingBox(-1.0, -1.0, 101.0, 101.0)

        self.assertAlmostEqual(contained.get_coverage(container), 1.0)

    def test_x_is_extruding(self):
        contained = BoundingBox(-20.0, 0.0, 120.0, 100.0)
        container = BoundingBox(0.0, 0.0, 100.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 100.0 / 140.0)

    def test_y_is_extruding(self):
        contained = BoundingBox(0.0, -20.0, 100.0, 120.0)
        container = BoundingBox(0.0, 0.0, 100.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 100.0 / 140.0)

    def test_x_is_out_of_bound(self):
        contained = BoundingBox(-100.0, 0.0, 0.0, 100.0)
        container = BoundingBox(0.0, 0.0, 100.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 0.0)

    def test_y_is_out_of_bound(self):
        contained = BoundingBox(0.0, -100.0, 100.0, 0.0)
        container = BoundingBox(0.0, 0.0, 100.0, 100.0)

        self.assertAlmostEqual(contained.get_coverage(container), 0.0)

    # ????????????????????????????????????
    def test_y_is_barely_intersecting(self):
        contained = BoundingBox(6.0, 48.0, 427.0, 97.0)
        container = BoundingBox(0.0, 49.0, 1070.0, 98.0)

        self.assertAlmostEqual(contained.get_coverage(container), 0.9795918367346939)
