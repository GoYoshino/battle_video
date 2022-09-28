import logging
from unittest import TestCase

from ocr.bounding_interval import BoundingInterval
from ocr.postprocess.ocr_text_index_estimator import TextIndexEstimator

logging.basicConfig(level=logging.DEBUG)

estimator = TextIndexEstimator(8.0, 1.0, 20)


class EstimateBlockIndexTest(TestCase):

    def test_block_estimation_works_on_idx14_image(self):
        self.assertEqual(14, estimator.estimate_block_index(BoundingInterval(140, 150), 0.99))

    def test_block_estimation_thresh_is_effective(self):
        bi = BoundingInterval(142, 152)
        self.assertEqual(14, estimator.estimate_block_index(bi, 0.6))
        with self.assertRaises(RuntimeError):
            estimator.estimate_block_index(bi, 0.8)

    def test_block_estimation_rejects_out_of_bound(self):
        with self.assertRaises(AssertionError):
            estimator.estimate_block_index(BoundingInterval(210, 220), 0.99)

    def test_block_estimation_rejects_thresh_under_05(self):
        with self.assertRaises(AssertionError):
            estimator.estimate_block_index(BoundingInterval(140, 150), 0.4)

    def test_line_estimation_works_on_first_line(self):
        self.assertEqual(0, estimator.estimate_line_index(BoundingInterval(1.0, 5.0), 0, 0.99))

    def test_line_estimation_works_on_first_line_at_block_14(self):
        self.assertEqual(0, estimator.estimate_line_index(BoundingInterval(141.0, 145.0), 14, 0.99))

    def test_line_estimation_works_on_second_line(self):
        self.assertEqual(1, estimator.estimate_line_index(BoundingInterval(5.0, 9.0), 0, 0.99))

    def test_line_estimation_thresh_is_effective(self):
        bi = BoundingInterval(6.0, 10.0)
        self.assertEqual(1, estimator.estimate_line_index(bi, 0, 0.6))
        with self.assertRaises(RuntimeError):
            estimator.estimate_line_index(bi, 0, 0.8)

    def test_line_estimation_rejects_out_of_bound(self):
        with self.assertRaises(AssertionError):
            estimator.estimate_line_index(BoundingInterval(11.0, 12.0), 0, 0.99)

    def test_line_estimation_rejects_thresh_under_05(self):
        with self.assertRaises(AssertionError):
            estimator.estimate_line_index(BoundingInterval(1.0, 10.0), 0, 0.4)
