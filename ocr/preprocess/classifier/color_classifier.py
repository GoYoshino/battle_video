from typing import Tuple, List

import cv2
import numpy

def classify_by_color(image: numpy.ndarray, colors: List[Tuple[int, int, int]], tolerance: int) -> float:
    """
    画像が指定された許容誤差の範囲で指定された色を含んでいる割合をスコアとして算出する
    :param image: 画像
    :param colors: 判定する色の配列。複数指定した場合の結果はUnionとして計算する。
    :param tolerance: 許容誤差。uint8での数値で指定。プラスマイナス
    :return: スコア。[0-1]の範囲
    """
    assert image.ndim == 3 and image.shape[2] == 3

    sum_mask = numpy.zeros((image.shape[0], image.shape[1]), dtype="uint8")
    for color in colors:
       sum_mask += __create_mask(image, color, tolerance)

    score = numpy.count_nonzero(sum_mask) / (image.shape[0] * image.shape[1])
    return score

def __create_mask(image: numpy.ndarray, target_color_bgr: Tuple[int, int, int], tolerance: int):
    return cv2.inRange(image,
                       (target_color_bgr[0] - tolerance, target_color_bgr[1] - tolerance, target_color_bgr[2] - tolerance),
                       (target_color_bgr[0] + tolerance, target_color_bgr[1] + tolerance, target_color_bgr[2] + tolerance))