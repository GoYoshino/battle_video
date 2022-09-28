import traceback
from collections import OrderedDict
from typing import List, Dict

from ocr.azure_read_result import AzureReadResult

# いったん定数
from ocr.bounding_interval import BoundingInterval
from ocr.postprocess.ocr_text_index_estimator import TextIndexEstimator

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


def __find_line_index(bounding_box: BoundingInterval, block_width: int, block_height: int, threshold: float,
                      padding_height: int) -> int:
    half_of_padding_height = float(padding_height / 2.0)
    line_bounding_boxes = [
        BoundingInterval(half_of_padding_height,
                         half_of_padding_height + float(block_height / 2.0)),
        BoundingInterval(
            half_of_padding_height + float(block_height / 2.0),
            float(block_height + padding_height))
    ]
    highest_score = -1
    bbox_at_highest = None
    highest_index = -1
    for line_index in range(len(line_bounding_boxes)):
        score = bounding_box.get_coverage(line_bounding_boxes[line_index])
        if score > highest_score:
            highest_score = score
            bbox_at_highest = line_bounding_boxes[line_index]
            if score > threshold:
                highest_index = line_index

    if highest_index != -1:
        return highest_index

    raise Exception(
        f"line indexを見つけられませんでした: text_bbox={bounding_box}, block_size=({block_width}, {block_height}), highest_score={highest_score}, bbox={bbox_at_highest}")


def segment_texts(ocr_results: List[AzureReadResult], block_width: int, window_height: int, padding_height: int) -> Dict[
    int, str]:
    container = SegmentedTextContainer()
    block_height = float(window_height + padding_height)

    num_blocks = int(AZURE_Y_LIMIT / block_height)

    estimator = TextIndexEstimator(block_height, num_blocks)

    for ocr_result in ocr_results:
        block_index = estimator.estimate_block_index(ocr_result.y_bounding_interval, THRESHOLD)

        relative_bounding_interval = ocr_result.y_bounding_interval.transposed(-block_index * block_height)
        line_index = __find_line_index(relative_bounding_interval, block_width, window_height, THRESHOLD, padding_height)
        container.append(block_index, line_index, ocr_result.text)
        # print(f"{ocr_result.text} is imidx={block_index}, lidx={line_index}")

    return container.build_to_text_dict()
