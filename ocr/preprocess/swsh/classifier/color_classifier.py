from typing import Tuple

import cv2
import numpy

# 今のところ他のヴァリアントを作る予定がないのでいったんすべて定数
WINDOW_COLOR_BGR = (52, 52, 52)
TEXT_COLOR_BGR = (252, 252, 252)
RED_TEXT_COLOR_BGR = (81, 130, 255)
TOLERANCE = 8
SCORE_THRESHOLD = 0.9


def classify_by_color(image: numpy.ndarray) -> bool:
    """
    剣盾専用の"ウィンドウかどうか判別メソッド"
    ウィンドウ色とテキスト色でセグメンテーションをかけて割合を見る
    :param image: 画像
    :return: ウィンドウかどうか
    """
    mask_window = __create_mask(image, WINDOW_COLOR_BGR, TOLERANCE)
    mask_text = __create_mask(image, TEXT_COLOR_BGR, TOLERANCE)
    mask_red_text = __create_mask(image, RED_TEXT_COLOR_BGR, TOLERANCE)

    mask = mask_window + mask_text + mask_red_text

    score = numpy.count_nonzero(mask) / (image.shape[0] * image.shape[1])
    return score > SCORE_THRESHOLD

def __create_mask(image: numpy.ndarray, target_color_bgr: Tuple[int, int, int], tolerance: int):
    return cv2.inRange(image,
                       (target_color_bgr[0] - tolerance, target_color_bgr[1] - tolerance, target_color_bgr[2] - tolerance),
                       (target_color_bgr[0] + tolerance, target_color_bgr[1] + tolerance, target_color_bgr[2] + tolerance))