from collections import OrderedDict
from typing import List, Dict

from ocr.bounding_box import BoundingBox
from ocr.azure_read_result import AzureReadResult

# いったん定数
THRESHOLD = 0.8

def __find_image_index(bounding_box: BoundingBox, image_width: int, image_height: int, threshold: float) -> int:
    estimated_image_index_lower_bound = max(0, int(bounding_box.top / image_height) - 1)

    boxes = []
    for image_index in range(estimated_image_index_lower_bound, estimated_image_index_lower_bound + 3):
        image_area = BoundingBox(0, image_index*image_height, image_width, (image_index + 1) * image_height)
        boxes.append(image_area)
        score = bounding_box.get_intersection_coverage(image_area)

        if score > threshold:
            return image_index

    image_region_all = BoundingBox(0, estimated_image_index_lower_bound * image_height, image_width, (estimated_image_index_lower_bound + 4) * image_height)
    raise Exception(f"image indexを見つけられませんでした: containing_bbox={image_region_all}, bbox={bounding_box}, image_size=({image_width}, {image_height})")

def __find_line_index(bounding_box: BoundingBox, image_width: int, image_height: int, threshold: float) -> int:
    line_bounding_boxes = [
        BoundingBox(0.0, 0.0, float(image_width), float(image_height) / 2.0),
        BoundingBox(0.0, float(image_height / 2.0), float(image_width), float(image_height)),
    ]
    for line_index in range(len(line_bounding_boxes)):
        score = bounding_box.get_intersection_coverage(line_bounding_boxes[line_index])

        if score > threshold:
            return line_index

    raise Exception(f"line indexを見つけられませんでした: {bounding_box}, image_size=({image_width}, {image_height})")

class SegmentedTextContainer:

    def __init__(self):
        self.__blocks: OrderedDict[int, OrderedDict[int, List[str]]] = OrderedDict()

    def append(self, image_index: int, line_index: int, text: str):
        if image_index not in self.__blocks.keys():
            self.__blocks[image_index] = OrderedDict()

        if line_index not in self.__blocks[image_index].keys():
            self.__blocks[image_index][line_index] = []

        self.__blocks[image_index][line_index].append(text)

    def build_to_text_list(self) -> List[str]:
        output_list = []

        for image_index in self.__blocks.keys():
            text_block = []
            for line_index in self.__blocks[image_index].keys():
                line = self.__blocks[image_index][line_index]
                text_line = " ".join(line)
                text_block.append(text_line)
            output_list.append("\n".join(text_block))

        return output_list


def segment_texts(ocr_results: List[AzureReadResult], image_width: int, image_height: int) -> List[str]:
    container = SegmentedTextContainer()
    for ocr_result in ocr_results:
        image_index = __find_image_index(ocr_result.bounding_box, image_width, image_height, THRESHOLD)
        relative_bounding_box = ocr_result.bounding_box.y_transposed(-image_index*image_height)
        line_index = __find_line_index(relative_bounding_box, image_width, image_height, THRESHOLD)
        container.append(image_index, line_index, ocr_result.text)

    return container.build_to_text_list()
