from typing import Dict

import numpy as np
from .classifier import classify_by_color

class SwShMessageWindowFilter:

    def filter(self, frames: Dict[int, np.ndarray]) -> Dict[int, np.ndarray]:
        """
        与えられた画像リストから、最低限の構成になるようメッセージウィンドウの画像を抜き出す
        :param frames: 画像の辞書　key=フレーム数
        :return: 抜き出した結果の辞書 key=フレーム数
        """
        result: Dict[int, np.ndarray] = {}
        for index, image in frames.items():
            if not classify_by_color(image):
                continue
            result[index] = image

        return result
