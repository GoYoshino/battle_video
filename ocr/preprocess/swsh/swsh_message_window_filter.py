from typing import Dict

import numpy as np
from ocr.preprocess.classifier import classify_by_color

# 今のところ他のヴァリアントを作る予定がないのでいったんすべて定数
WINDOW_COLOR_BGR = (52, 52, 52)
TEXT_COLOR_BGR = (252, 252, 252)
RED_TEXT_COLOR_BGR = (81, 130, 255)
TOLERANCE = 8
COLOR_SCORE_THRESHOLD = 0.9

class SwShMessageWindowFilter:

    def filter(self, frames: Dict[int, np.ndarray]) -> Dict[int, np.ndarray]:
        """
        与えられた画像リストから、メッセージウィンドウの画像だけを抜き出して返す
        :param frames: 画像の辞書　key=フレーム数
        :return: 抜き出した結果の辞書 key=フレーム数　
        """
        assert len(frames) > 0
        assert frames[0].ndim == 2
        assert frames[0].shape[2] == 3

        result: Dict[int, np.ndarray] = {}
        for index, image in frames.items():
            # ウィンドウ色、テキスト色でセグメンテーション
            if classify_by_color(image, [WINDOW_COLOR_BGR, TEXT_COLOR_BGR, RED_TEXT_COLOR_BGR], 8) < COLOR_SCORE_THRESHOLD:
                continue
            result[index] = image

        return result

    # TODO: after_thresh_filterをここに
