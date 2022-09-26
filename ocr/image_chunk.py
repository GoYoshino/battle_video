from io import BytesIO
from typing import List

import cv2
import numpy as np
from PIL import Image

PIXELS_LIMIT = 75000000

class ImageChunk:

    def __init__(self):
        self.__images: List[np.ndarray] = []

    def can_append(self, new_image: np.ndarray):
        pixels = 0
        for image in self.__images:
            pixels += image.shape[0]*image.shape[1]
        return pixels + new_image.shape[0]*new_image.shape[1] <= PIXELS_LIMIT

    def append(self, new_image: np.ndarray):
        assert self.can_append(new_image)
        self.__images.append(new_image)

    def to_png(self) -> bytes:
        assert len(self.__images) > 0

        out_image = cv2.vconcat(self.__images)
        out_image_pil = Image.fromarray(out_image)
        buffer = BytesIO()
        out_image_pil.save(buffer, format="PNG")
        return buffer.getvalue()