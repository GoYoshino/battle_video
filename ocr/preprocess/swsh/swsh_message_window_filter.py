from typing import Dict

import numpy
from ocr.preprocess.classifier import classify_by_color

# 今のところ他のヴァリアントを作る予定がないのでいったんすべて定数
WINDOW_COLOR_BGR = (52, 52, 52)
TEXT_COLOR_BGR = (252, 252, 252)
RED_TEXT_COLOR_BGR = (81, 130, 255)

class SwShMessageWindowFilter:
# Review: クラスである必要は？

    def filter_by_color(self, frames: Dict[int, numpy.ndarray], tolerance: int, color_score_threshold: float) -> Dict[int, numpy.ndarray]:
        """
        与えられた画像辞書から、メッセージウィンドウの画像だけを抜き出して返す
        :param frames: 画像の辞書　key=フレーム数
        :return: 抜き出した結果の辞書 key=フレーム数　
        """
        assert len(frames) > 0

        result: Dict[int, numpy.ndarray] = {}
        for index, image in frames.items():
            assert image.ndim == 3
            assert image.shape[2] == 3

            # ウィンドウ色、テキスト色でセグメンテーション
            if classify_by_color(image, [WINDOW_COLOR_BGR, TEXT_COLOR_BGR, RED_TEXT_COLOR_BGR], tolerance) <= color_score_threshold:
                continue
            result[index] = image

        return result

    def filter_threshed_by_black_percentage(self, frames: Dict[int, numpy.ndarray], lower_thresh: float, higher_thresh: float) -> Dict[int, numpy.ndarray]:
        """
        与えられた画像(2値グレースケール)の辞書から、メッセージウィンドウの画像だけを抜き出して返す
        アルゴリズムとしては、
        「(2値化後に)黒の面積の割合が一定未満ならウィンドウではないとみなして棄却」
        「黒の面積の割合があまりにも大きい場合、空のウィンドウとみなして棄却」
        :param frames: 画像の辞書　key=フレーム数
        :param lower_thresh: 下限
        :param higher_thresh: 上限
        :return: ウィンドウでないものおよび空のウィンドウが除かれた画像辞書
        """
        assert lower_thresh < higher_thresh
        result: Dict[int, numpy.ndarray] = {}
        for index, image in frames.items():
            assert image.ndim == 2
            score = float(numpy.count_nonzero(image == 0)) / float(image.shape[0] * image.shape[1])
            if score < lower_thresh or score > higher_thresh:
                continue
            result[index] = image
        return result
