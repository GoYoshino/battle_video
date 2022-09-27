import traceback
from collections import OrderedDict
from typing import List, Dict

from ocr.bounding_box import BoundingBox
from ocr.azure_read_result import AzureReadResult

# いったん定数
THRESHOLD = 0.65
AZURE_Y_LIMIT = 10000

class SegmentedTextContainer:

    def __init__(self):
        self.__blocks: OrderedDict[int, OrderedDict[int, List[str]]] = OrderedDict()

    def append(self, block_index: int, line_index: int, text: str):
        if block_index not in self.__blocks.keys():
            self.__blocks[block_index] = OrderedDict()

        if line_index not in self.__blocks[block_index].keys():
            self.__blocks[block_index][line_index] = []

        self.__blocks[block_index][line_index].append(text)

    def build_to_text_dict(self) -> Dict[int, str]:
        output_dict: Dict[int, str] = {}

        for block_index in self.__blocks.keys():
            text_block = []
            for line_index in self.__blocks[block_index].keys():
                line = self.__blocks[block_index][line_index]
                text_line = " ".join(line)
                text_block.append(text_line)

            output_dict[block_index] = "\n".join(text_block)

        return output_dict

def __find_block_index(bounding_box: BoundingBox, block_width: int, block_height: int, threshold: float, padding_height: int) -> int:
    section_height = float(block_height) + float(padding_height)
    estimated_block_index_lower_bound = max(0, int(bounding_box.top / section_height) - 1)

    boxes = []
    loops = int(AZURE_Y_LIMIT / section_height) + 1
    highest_score = -1
    highest_index = -1
    bbox_at_highest = None
    for block_index in range(estimated_block_index_lower_bound, loops):
        image_area = BoundingBox(0, block_index * section_height, block_width, (block_index + 1) * section_height)
        boxes.append(image_area)
        score = bounding_box.get_intersection_coverage(image_area)
        if highest_score < score:
            highest_score = score
            bbox_at_highest = image_area
            if score > threshold:
                highest_index = block_index

    if highest_index != -1:
        return highest_index

    image_region_all = BoundingBox(0, estimated_block_index_lower_bound * block_height, block_width, AZURE_Y_LIMIT)
    raise Exception(f"image indexを見つけられませんでした: highest_score={highest_score}, bbox={bbox_at_highest}, bbox={bounding_box}, image_size=({block_width}, {block_height}), highest_score={highest_score}")

def __find_line_index(bounding_box: BoundingBox, block_width: int, block_height: int, threshold: float, padding_height: int) -> int:
    half_of_padding_height = float(padding_height / 2.0)
    line_bounding_boxes = [
        BoundingBox(0.0,
                    half_of_padding_height,
                    float(block_width),
                    half_of_padding_height + float(block_height / 2.0)),
        BoundingBox(0.0,
                    half_of_padding_height + float(block_height / 2.0),
                    float(block_width),
                    float(block_height + padding_height))
    ]
    highest_score = -1
    bbox_at_highest = None
    highest_index = -1
    for line_index in range(len(line_bounding_boxes)):
        score = bounding_box.get_intersection_coverage(line_bounding_boxes[line_index])
        if score > highest_score:
            highest_score = score
            bbox_at_highest = line_bounding_boxes[line_index]
            if score > threshold:
                highest_index = line_index

    if highest_index != -1:
        return highest_index

    raise Exception(f"line indexを見つけられませんでした: text_bbox={bounding_box}, block_size=({block_width}, {block_height}), highest_score={highest_score}, bbox={bbox_at_highest}")

def segment_texts(ocr_results: List[AzureReadResult], block_width: int, block_height: int, padding_height: int) -> Dict[int, str]:
    container = SegmentedTextContainer()
    section_height = float(block_height + padding_height)

    for ocr_result in ocr_results:
        block_index = __find_block_index(ocr_result.bounding_box, block_width, block_height, THRESHOLD,
                                         padding_height)

        relative_bounding_box = ocr_result.bounding_box.y_transposed(-block_index * section_height)
        line_index = __find_line_index(relative_bounding_box, block_width, block_height, THRESHOLD, padding_height)
        container.append(block_index, line_index, ocr_result.text)
        #print(f"{ocr_result.text} is imidx={block_index}, lidx={line_index}")

    return container.build_to_text_dict()