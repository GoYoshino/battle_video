from unittest import TestCase

import numpy

from ocr.preprocess.swsh.swsh_message_window_filter import SwShMessageWindowFilter
from ocr.test_helpers.mock_image_builder import MockImageBuilder

filter = SwShMessageWindowFilter()

class SwShMessageWindowFilterTest(TestCase):

    def test_accepts_only_rgb_image(self):
        with self.assertRaises(AssertionError):
            filter.filter_by_color({1: numpy.array([[1]])}, 0, 0.9)
        with self.assertRaises(AssertionError):
            filter.filter_by_color({1: numpy.array([[1]])}, 0, 0.9)

    def test_denies_low_score(self):
        b = MockImageBuilder()
        b.add(10, [252, 252, 252])
        im_text = b.to_image()

        b.reset()
        b.add(10, [251, 251, 251])
        im_other = b.to_image()

        result = filter.filter_by_color({
            1: im_text,
            2: im_other
        }, 0, 0.9)

        self.assertEqual(1, len(result))
        self.assertIs(im_text, result[1])

    def test_thresh_effective(self):
        b = MockImageBuilder()
        b.add(10, [252, 252, 252])
        b.add(9, [251, 251, 251])
        im_accepted = b.to_image()

        b.reset()
        b.add(9, [252, 252, 252])
        b.add(10, [251, 251, 251])
        im_rejected = b.to_image()

        result = filter.filter_by_color({
            1: im_rejected,
            2: im_accepted
        }, 0, 0.5)

        self.assertEqual(1, len(result))
        self.assertIs(im_accepted, result[2])

    def test_tolerance_is_effective(self):
        b = MockImageBuilder()
        b.add(10, [252, 252, 252])
        im_just = b.to_image()

        b.reset()
        b.add(10, [251, 251, 251])
        im_distance_of_1 = b.to_image()

        b.reset()
        b.add(10, [250, 251, 251])
        im_distance_of_2 = b.to_image()

        result = filter.filter_by_color({
            1: im_just,
            2: im_distance_of_2,
            3: im_distance_of_1
        }, 1, 0.9)

        self.assertEqual(2, len(result))
        self.assertIs(im_just, result[1])
        self.assertIs(im_distance_of_1, result[3])

    def test_accepts_text_color(self):
        b = MockImageBuilder()
        b.add(10, [252, 252, 252])

        result = filter.filter_by_color({1: b.to_image()}, 0, 0.9)

        self.assertEqual(1, len(result))

    def test_accepts_window_color(self):
        b = MockImageBuilder()
        b.add(10, [52, 52, 52])

        result = filter.filter_by_color({1: b.to_image()}, 0, 0.9)

        self.assertEqual(1, len(result))

    def test_accepts_red_text_color(self):
        b = MockImageBuilder()
        b.add(10, [81, 130, 255])

        result = filter.filter_by_color({1: b.to_image()}, 0, 0.9)

        self.assertEqual(1, len(result))

    def test_sums_up_multiple_target(self):
        b = MockImageBuilder()
        b.add(10, [52, 52, 52])
        im_window = b.to_image()

        b.reset()
        b.add(10, [252, 252, 252])
        im_text = b.to_image()

        b.reset()
        b.add(10, [4, 4, 4])
        im_other = b.to_image()

        result = filter.filter_by_color({
            1: im_window,
            2: im_text,
            3: im_other
        }, 0, 0.9)

        self.assertEqual(2, len(result))
        self.assertIs(im_window, result[1])
        self.assertIs(im_text, result[2])

    ### 2値フィルタのテスト ###

    def test_2bit_denies_non_grayscale_image(self):
        with self.assertRaises(AssertionError):
            filter.filter_threshed_by_black_percentage({1: numpy.array([[[1, 1, 1]]])}, 0.8, 0.999)

    def test_2bit_denies_invalid_bound(self):
        with self.assertRaises(AssertionError):
            filter.filter_threshed_by_black_percentage({1: numpy.array([[1]])}, 0.8, 0.7)

    def test_2bit_accepts_windows(self):
        b = MockImageBuilder()
        b.add(10, 0)
        b.add(1, 255)
        im = b.to_image()

        result = filter.filter_threshed_by_black_percentage({1: im}, 0.8, 0.999)
        self.assertEqual(1, len(result))

    def test_2bit_denies_anything_but_windows(self):
        b = MockImageBuilder()
        b.add(5, 0)
        b.add(5, 255)
        im = b.to_image()

        result = filter.filter_threshed_by_black_percentage({1: im}, 0.8, 0.999)
        self.assertEqual(0, len(result))

    def test_2bit_higher_thresh_is_effective(self):
        b = MockImageBuilder()
        b.add(8, 0)
        b.add(3, 255)
        im_accepted = b.to_image()

        b.reset()
        b.add(8, 0)
        b.add(1, 255)
        im_rejected = b.to_image()

        result = filter.filter_threshed_by_black_percentage({1: im_accepted, 2: im_rejected}, 0.0, 0.8)
        self.assertEqual(1, len(result))
        self.assertIs(result[1], im_accepted)

    def test_2bit_lower_thersh_is_effective(self):
        b = MockImageBuilder()
        b.add(8, 0)
        b.add(3, 255)
        im_rejected = b.to_image()

        b.reset()
        b.add(8, 0)
        b.add(1, 255)
        im_accepted = b.to_image()

        result = filter.filter_threshed_by_black_percentage({1: im_rejected, 2: im_accepted}, 0.8, 1.0)
        self.assertEqual(1, len(result))
        self.assertIs(result[2], im_accepted)
