from io import BytesIO
from unittest import TestCase

from mock import MagicMock, PropertyMock, patch
import numpy as np
from PIL import Image

from ocr.image_chunk import ImageChunk

im1 = np.array([
    [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ],
    [ [10, 11, 12], [13, 14, 15], [16, 17, 18] ],
    [ [19, 20, 21], [22, 23, 24], [25, 26, 27] ],
], dtype="uint8")
im2 = np.array([
    [ [28, 29, 30], [31, 32, 33], [34, 35, 36] ],
    [ [37, 38, 39], [40, 41, 42], [43, 44, 45] ],
    [ [46, 47, 48], [49, 50, 51], [52, 53, 54] ],
], dtype="uint8")

im1_plus_im2 = np.array([
    [ [1, 2, 3], [4, 5, 6], [7, 8, 9] ],
    [ [10, 11, 12], [13, 14, 15], [16, 17, 18] ],
    [ [19, 20, 21], [22, 23, 24], [25, 26, 27] ],
    [ [28, 29, 30], [31, 32, 33], [34, 35, 36] ],
    [ [37, 38, 39], [40, 41, 42], [43, 44, 45] ],
    [ [46, 47, 48], [49, 50, 51], [52, 53, 54] ],
], dtype="uint8")

class ImageChunkTest(TestCase):

    def test_concat_works(self):
        chunk = ImageChunk()
        chunk.append(im1)
        chunk.append(im2)
        result = chunk.get_concatted()

        self.assertTrue(np.array_equal(im1_plus_im2, result))

    def test_to_png_works(self):
        chunk = ImageChunk()
        chunk.append(im1)
        chunk.append(im2)
        result = chunk.to_concatted_png_buffer()

        buffer = BytesIO(result)
        constructed_array = np.array(Image.open(buffer))
        self.assertTrue(np.array_equal(im1_plus_im2, constructed_array))

    def test_can_append_works(self):
        chunk = ImageChunk()
        self.assertTrue(chunk.can_append(im1))

    def test_cannot_append_an_image_exceeding_limit(self):
        chunk = ImageChunk()
        mega_image = np.zeros((75000001, 1), dtype="uint8")

        self.assertFalse(chunk.can_append(mega_image))

    def test_cannot_append_when_full(self):
        chunk = ImageChunk()
        mega_image = np.zeros((75000000, 1), dtype="uint8")
        chunk.append(mega_image)

        self.assertFalse(chunk.can_append(np.zeros((1, 1))))

    def test_refuses_at_capacity_limit(self):
        chunk = ImageChunk()
        mega_image = np.zeros((75000000, 1), dtype="uint8")
        chunk.append(mega_image)

        with self.assertRaises(AssertionError):
            chunk.append(np.zeros((1, 1)))