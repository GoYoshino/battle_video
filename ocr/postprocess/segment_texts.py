import logging
from collections import OrderedDict
from typing import List, Dict

from ocr.azure_read_result import AzureReadResult

from ocr.postprocess.ocr_text_index_estimator import TextIndexEstimator

# いったん定数
THRESHOLD = 0.65
AZURE_Y_LIMIT = 10000

logger = logging.getLogger(__name__)


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


def segment_texts(ocr_results: List[AzureReadResult], window_height: int, padding_height: int) -> Dict[
    int, str]:
    container = SegmentedTextContainer()

    block_height = float(window_height) + float(padding_height)*2.0
    num_blocks = int(AZURE_Y_LIMIT / block_height)

    estimator = TextIndexEstimator(window_height, padding_height, num_blocks)

    for ocr_result in ocr_results:
        block_index = estimator.estimate_block_index(ocr_result.y_bounding_interval, THRESHOLD)

        line_index = estimator.estimate_line_index(ocr_result.y_bounding_interval, block_index, THRESHOLD)
        container.append(block_index, line_index, ocr_result.text)
        logger.debug(f"{ocr_result.text} is imidx={block_index}, lidx={line_index}")

    return container.build_to_text_dict()
