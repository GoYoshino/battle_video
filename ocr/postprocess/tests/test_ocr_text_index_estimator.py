import logging
from unittest import TestCase

from ocr.bounding_interval import BoundingInterval
from ocr.postprocess.ocr_text_index_estimator import TextIndexEstimator

logging.basicConfig(level=logging.DEBUG)

estimator = TextIndexEstimator(10.0, 20)

class EstimateBlockIndexTest(TestCase):

    def test_works_on_idx14_image(self):
        self.assertEqual(14, estimator.estimate_block_index(BoundingInterval(140, 150), 0.99))

    def test_thresh_is_effective(self):
        bi = BoundingInterval(142, 152)
        self.assertEqual(14, estimator.estimate_block_index(bi, 0.6))
        with self.assertRaises(RuntimeError):
            estimator.estimate_block_index(bi, 0.8)

    def test_rejects_out_of_bound(self):
        with self.assertRaises(AssertionError):
            estimator.estimate_block_index(BoundingInterval(210, 220), 0.99)

    def test_rejects_thresh_under_05(self):
        with self.assertRaises(AssertionError):
            estimator.estimate_block_index(BoundingInterval(140, 150), 0.4)
