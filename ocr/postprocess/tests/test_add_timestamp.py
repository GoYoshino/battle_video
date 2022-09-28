from unittest import TestCase

from ocr.postprocess.add_timestamp import add_timestamp


class AddTimestampTest(TestCase):

    def test_ordinary_case(self):
        result = [{
            0: "レッドは\nカバルドンを くりだした'",
            1: 'ゆけっ! ウオノラゴン!',
            2: '砂あらしが 吹き始めた!'
        }]

        timestamps = [100, 400, 900]

        timestamped = add_timestamp(result, timestamps, 68)

        self.assertDictEqual({
            100: "レッドは\nカバルドンを くりだした'",
            400: 'ゆけっ! ウオノラゴン!',
            900: '砂あらしが 吹き始めた!'
        }, timestamped)

    def test_works_on_multiple_pages(self):
        result = [{
            0: "レッドは\nカバルドンを くりだした'",
            1: 'ゆけっ! ウオノラゴン!'
        }, {
            0: '砂あらしが 吹き始めた!',
            1: "ウオノラゴンの\nエラがみ!",
        }, {
            0: "効果は バツグンだ!"
        }]

        timestamps = [100, 400, 900, 1600, 2500]

        timestamped = add_timestamp(result, timestamps, 2)

        self.assertDictEqual({
            100: "レッドは\nカバルドンを くりだした'",
            400: 'ゆけっ! ウオノラゴン!',
            900: '砂あらしが 吹き始めた!',
            1600: "ウオノラゴンの\nエラがみ!",
            2500: "効果は バツグンだ!"
        }, timestamped)

    def test_works_on_multiple_pages_with_multiple_of_blocks_per_page(self):
        result = [{
            0: "レッドは\nカバルドンを くりだした'",
            1: 'ゆけっ! ウオノラゴン!'
        }, {
            0: '砂あらしが 吹き始めた!',
            1: "ウオノラゴンの\nエラがみ!"
        }]

        timestamps = [100, 400, 900, 1600]

        timestamped = add_timestamp(result, timestamps, 2)

        self.assertDictEqual({
            100: "レッドは\nカバルドンを くりだした'",
            400: 'ゆけっ! ウオノラゴン!',
            900: '砂あらしが 吹き始めた!',
            1600: "ウオノラゴンの\nエラがみ!"
        }, timestamped)

    def test_skips_empty_block(self):
        result = [{
            0: "レッドは\nカバルドンを くりだした'",
            1: 'ゆけっ! ウオノラゴン!',
        }, {
            1: "ウオノラゴンの\nエラがみ!"
        }]

        timestamps = [100, 400, 900, 1600]

        timestamped = add_timestamp(result, timestamps, 2)

        self.assertDictEqual({
            100: "レッドは\nカバルドンを くりだした'",
            400: 'ゆけっ! ウオノラゴン!',
            1600: "ウオノラゴンの\nエラがみ!"
        }, timestamped)
