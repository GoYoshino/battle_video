from typing import List

import cv2
import numpy

from ocr.image_chunk import ImageChunk
from ocr.preprocess.swsh.swsh_message_window_filter import SwShMessageWindowFilter


class SwShPreprocessor:

    def __init__(self):
        self.__window_filter = SwShMessageWindowFilter()

    def preprocess(self, images: List[numpy.ndarray]) -> List[ImageChunk]:
        images = self.__window_filter.filter(images)
        images = self.__thresh(images)
        images = self.__after_thresh_filter(images)

        assert len(images) > 0
        # TODO: 将来的にここで重複を除く
        chunks = []
        chunk = ImageChunk()
        padding = numpy.zeros((24, images[0].shape[1]), dtype="uint8")
        for image in images:
            image_with_padding = cv2.vconcat([padding, image, padding])
            if chunk.can_append(image_with_padding):
                chunk.append(image_with_padding)
            else:
                chunks.append(chunk)
                chunk = ImageChunk()

        chunks.append(chunk)
        return chunks

    def __thresh(self, images: List[numpy.ndarray]) -> List[numpy.ndarray]:
        result = []
        for image in images:
            im_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, im_threshed = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY)
            result.append(im_threshed)
        return result

    def __after_thresh_filter(self, images: List[numpy.ndarray]) -> List[numpy.ndarray]:
        result = []
        for image in images:
            score = float(numpy.count_nonzero(image == 0)) / float(image.shape[0] * image.shape[1])
            if score < 0.8 or score > 0.999:
                continue
            result.append(image)
        return result
