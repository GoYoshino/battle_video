from typing import List, Dict, Tuple

import cv2
import numpy

from ocr.image_chunk import ImageChunk
from ocr.preprocess.swsh.swsh_message_window_filter import SwShMessageWindowFilter

COLOR_SCORE_THRESHOLD = 0.9
COLOR_TOLERANCE = 8

TWOBIT_FILTER_LOWER_BOUND = 0.8
TWOBIT_FILTER_HIGHER_BOUND = 0.999

class SwShMessageWindowPreprocessor:
    """
    剣盾のウィンドウ部分専用のプリプロセッサ
    ウィンドウ部分の画像からいらないものを除いたり、OCRにかけやすい状態にする
    """

    def __init__(self):
        self.__window_filter = SwShMessageWindowFilter()

    def preprocess(self, frames: Dict[int, numpy.ndarray]) -> Tuple[List[ImageChunk], List[int]]:
        """
        与えられた画像からウィンドウと思われる画像のみを抽出し、OCRにかけやすいよう2値化した状態で返す
        :param frames: フレーム画像の集合。辞書形式でkeyがフレーム数
        :return: [0]=処理後の画像チャンク(API送信用) [1]=プリプロセスの結果残ったフレーム数のリスト
        """
        frames = self.__window_filter.filter_by_color(frames, COLOR_TOLERANCE, COLOR_SCORE_THRESHOLD)
        frames = self.__thresh(frames)
        frames = self.__window_filter.filter_threshed_by_black_percentage(frames, TWOBIT_FILTER_LOWER_BOUND, TWOBIT_FILTER_HIGHER_BOUND)

        assert len(frames.keys()) > 0
        # TODO: 将来的にここで重複を除く→重複はあえて冗長性のために残すという可能性もある
        chunks = []
        chunk = ImageChunk()
        padding = numpy.zeros((24, list(frames.values())[0].shape[1]), dtype="uint8")
        for index, image in frames.items():
            image_with_padding = cv2.vconcat([padding, image, padding])
            if chunk.can_append(image_with_padding):
                chunk.append(image_with_padding)
            else:
                chunks.append(chunk)
                chunk = ImageChunk()
                chunk.append(image_with_padding)

        chunks.append(chunk)
        return chunks, list(frames.keys())

    def __thresh(self, frames: Dict[int, numpy.ndarray]) -> Dict[int, numpy.ndarray]:
        result: Dict[int, numpy.ndarray] = {}
        for index, image in frames.items():
            im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, im_threshed = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY)
            result[index] = im_threshed
        return result

