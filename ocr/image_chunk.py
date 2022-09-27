from io import BytesIO
from typing import List

import cv2
import numpy as np
from PIL import Image

PIXELS_LIMIT = 75000000
ROWS_LIMIT = 10000

class ImageChunk:

    def __init__(self, google=False):
        """

        :param google: TrueのときGoogle(ピクセル数で制限)、FalseのときAzure(幅で制限)
        """
        self.__images: List[np.ndarray] = []
        self.__google = google

    def can_append(self, new_image: np.ndarray):
        if self.__google:
            pixels = 0
            for image in self.__images:
                pixels += image.shape[0]*image.shape[1]
            return pixels + new_image.shape[0]*new_image.shape[1] <= PIXELS_LIMIT
        else:
            rows = 0
            for image in self.__images:
                rows += image.shape[0]
            return rows + new_image.shape[0] <= ROWS_LIMIT

    def append(self, new_image: np.ndarray):
        assert self.can_append(new_image)
        self.__images.append(new_image)

    def get_concatted(self) -> np.ndarray:
        assert len(self.__images) > 0
        out_image = cv2.vconcat(self.__images)
        return out_image

    def pop(self):
        self.__images.pop()

    def count(self):
        return len(self.__images)

    def to_concatted_png_buffer(self) -> bytes:
        out_image = self.get_concatted()
        out_image_pil = Image.fromarray(out_image)
        buffer = BytesIO()
        out_image_pil.save(buffer, format="PNG")
        return buffer.getvalue()