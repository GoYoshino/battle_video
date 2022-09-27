from typing import List, Dict, Tuple

import cv2
import numpy

from ocr.image_chunk import ImageChunk
from ocr.preprocess.swsh.swsh_message_window_filter import SwShMessageWindowFilter


class SwShPreprocessor:

    def __init__(self):
        self.__window_filter = SwShMessageWindowFilter()

    def preprocess(self, frames: Dict[int, numpy.ndarray]) -> Tuple[List[ImageChunk], List[int]]:
        frames = self.__window_filter.filter(frames)
        frames = self.__thresh(frames)
        frames = self.__after_thresh_filter(frames)

        assert len(frames.keys()) > 0
        # TODO: 将来的にここで重複を除く
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

    def __after_thresh_filter(self, frames: Dict[int, numpy.ndarray]) -> Dict[int, numpy.ndarray]:
        result: Dict[int, numpy.ndarray] = {}
        for index, image in frames.items():
            score = float(numpy.count_nonzero(image == 0)) / float(image.shape[0] * image.shape[1])
            if score < 0.8 or score > 0.999:
                continue
            result[index] = image
        return result
