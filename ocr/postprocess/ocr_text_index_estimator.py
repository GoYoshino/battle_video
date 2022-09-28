import logging

from ocr.bounding_interval import BoundingInterval

logger = logging.getLogger(__name__)

class TextIndexEstimator:

    def __init__(self, block_height: float, num_blocks: int):
        assert block_height > 0
        assert num_blocks > 0

        self.__block_height = block_height
        self.__num_blocks = num_blocks

    def estimate_block_index(self, y_bounding_interval: BoundingInterval, threshold: float):
        """
        与えられたBoundingIntervalにあるテキストが、1点の画像の中でどの「ブロック」にあるかを推定する
        「ブロック」とはOCRに読ませる画像を構成する領域で、上padding+ウィンドウ本体+下paddingの3つの画像からなる。
        :param y_bounding_interval: テキストのBoundingBoxのY部分の領域
        :param threshold: スコアがこれを超えないとインデックスを与えない
        :return:
        """

        assert threshold > 0.5  # 0.5を超えないと複数の候補が出てくることになってしまう

        estimated_index_lower_bound = max(0, int(
            y_bounding_interval.high / self.__block_height) - 1)  # ループ回数を節約するため、明らかに範囲外のブロックを候補から切る
        assert estimated_index_lower_bound < self.__num_blocks

        highest_score = -1
        index_at_highest = -1
        bound_at_highest = None

        for block_index in range(estimated_index_lower_bound, self.__num_blocks):
            candidate_block = BoundingInterval(block_index * self.__block_height, (block_index + 1) * self.__block_height)
            score = y_bounding_interval.get_coverage(candidate_block)
            logger.debug(f"candidate_block={candidate_block} score={score}")
            if highest_score < score:
                highest_score = score
                index_at_highest = block_index
                bound_at_highest = candidate_block
                if score > threshold:
                    return index_at_highest

        raise RuntimeError(
            f"block indexを見つけられませんでした: message_bound={y_bounding_interval}, highest_score={highest_score}, most_likely_block={bound_at_highest}, most_likely_index={index_at_highest}")
