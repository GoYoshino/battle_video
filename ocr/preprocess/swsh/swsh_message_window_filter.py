from typing import List

import numpy as np
from .classifier import classify_by_color

class SwShMessageWindowFilter:

    def filter(self, images: List[np.ndarray]) -> List[np.ndarray]:
        """
        与えられた画像リストから、最低限の構成になるようメッセージウィンドウの画像を抜き出す
        :param images: 画像のリスト
        :return: 抜き出した結果のリスト
        """
        result = []
        for image in images:
            if not classify_by_color(image):
                continue
            result.append(image)

        return result
