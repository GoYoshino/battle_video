from typing import Dict

import numpy as np
from ocr.preprocess.classifier import classify_by_color

# 今のところ他のヴァリアントを作る予定がないのでいったんすべて定数
WINDOW_COLOR_BGR = (52, 52, 52)
TEXT_COLOR_BGR = (252, 252, 252)
RED_TEXT_COLOR_BGR = (81, 130, 255)

class SwShMessageWindowFilter:
# Review: クラスである必要は？

    def filter_by_color(self, frames: Dict[int, np.ndarray], tolerance: int, color_score_threshold: float) -> Dict[int, np.ndarray]:
        """
        与えられた画像リストから、メッセージウィンドウの画像だけを抜き出して返す
        :param frames: 画像の辞書　key=フレーム数
        :return: 抜き出した結果の辞書 key=フレーム数　
        """
        assert len(frames) > 0

        result: Dict[int, np.ndarray] = {}
        for index, image in frames.items():
            assert image.ndim == 3
            assert image.shape[2] == 3

            # ウィンドウ色、テキスト色でセグメンテーション
            if classify_by_color(image, [WINDOW_COLOR_BGR, TEXT_COLOR_BGR, RED_TEXT_COLOR_BGR], tolerance) <= color_score_threshold:
                continue
            result[index] = image

        return result

    # TODO: after_thresh_filterをここに
