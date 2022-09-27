from typing import List

import numpy

from ocr.image_chunk import ImageChunk
from ocr.preprocess.swsh.swsh_message_window_filter import SwShMessageWindowFilter


class SwShPreprocessor:

    def __init__(self):
        self.__window_filter = SwShMessageWindowFilter()

    def preprocess(self, images: List[numpy.ndarray]) -> List[ImageChunk]:
        window_images = self.__window_filter.filter(images)
        # TODO: 将来的にここで重複を除く
        chunks = []
        chunk = ImageChunk()
        for image in images:
            if chunk.can_append(image):
                chunk.append(image)
            else:
                chunks.append(chunk)
                chunk = ImageChunk()

        chunks.append(chunk)
        return chunks