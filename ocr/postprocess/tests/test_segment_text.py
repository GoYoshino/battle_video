from typing import List
from unittest import TestCase

import mock
from mock import MagicMock, patch

from ocr.postprocess import segment_texts


def fabricate_result(texts: List[str]):
    results = []
    for text in texts:
        result_mock = MagicMock()
        type(result_mock).text = mock.PropertyMock(return_value=text)
        results.append(result_mock)

    return results


@patch("ocr.postprocess.ocr_text_index_estimator.TextIndexEstimator.estimate_block_index")
@patch("ocr.postprocess.ocr_text_index_estimator.TextIndexEstimator.estimate_line_index")
class SegmentTextTest(TestCase):

    def test_segments_standard_text(self, line_mock, block_mock):
        block_mock.side_effect = [0, 0, 0]
        line_mock.side_effect = [0, 0, 1]
        result = segment_texts(fabricate_result(["hoge", "fuga", "hai"]), 10, 2)

        self.assertEqual("hoge fuga\nhai", result[0])

    def test_segments_one_line_text(self, line_mock, block_mock):
        block_mock.side_effect = [0, 0]
        line_mock.side_effect = [0, 0]
        result = segment_texts(fabricate_result(["hoge", "fuga"]), 10, 2)

        self.assertEqual("hoge fuga", result[0])

    def test_segments_one_line_text_line2(self, line_mock, block_mock):
        block_mock.side_effect = [0, 0]
        line_mock.side_effect = [1, 1]
        result = segment_texts(fabricate_result(["hoge", "fuga"]), 10, 2)

        self.assertEqual("hoge fuga", result[0])

    def test_segments_multiple_texts(self, line_mock, block_mock):
        block_mock.side_effect = [0, 0, 1, 1]
        line_mock.side_effect = [0, 1, 0, 1]
        result = segment_texts(fabricate_result([
            "ピカチュウの", "でんきショック!",
            "ミミッキュは", "たおれた!"
        ]), 10, 2)

        self.assertEqual("ピカチュウの\nでんきショック!", result[0])
        self.assertEqual("ミミッキュは\nたおれた!", result[1])

    def test_skips_empty_block(self, line_mock, block_mock):
        block_mock.side_effect = [1, 1]
        line_mock.side_effect = [0, 1]
        result = segment_texts(fabricate_result([
            "ミミッキュは", "たおれた!"
        ]), 10, 2)

        self.assertEqual("ミミッキュは\nたおれた!", result[1])
