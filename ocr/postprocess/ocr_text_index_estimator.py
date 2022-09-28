import logging

from ocr.bounding_interval import BoundingInterval

logger = logging.getLogger(__name__)

class TextIndexEstimator:
    """
    BoudingBoxつきテキストのインデックスをバウンディングボックスの位置から推定する。
    """

    def __init__(self, window_height: float, padding_height: float, num_blocks: int):
        """
        block = { padding, window, padding }
        :param window_height: ウィンドウの高さ
        :param padding_height: パディングの高さ
        :param num_blocks: 画像1枚あたりのブロック数
        """
        assert window_height > 0
        assert padding_height > 0
        assert num_blocks > 0

        self.__window_height = float(window_height)
        self.__padding_height = float(padding_height)
        self.__block_height = window_height + padding_height*2.0
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

        logger.debug(f"finding block index for {y_bounding_interval}")
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

    def estimate_line_index(self, bounding_interval: BoundingInterval, block_index: int, threshold: float) -> int:
        """
        与えられたBoundingInterval値域が何行目に属するかを推定する
        :param bounding_interval: BoundingBoxのY部分
        :param: block_index: 対象テキストが属するブロックのインデックス
        :param threshold: 閾値
        :return: 行番号
        """

        assert threshold > 0.5

        relative_bounding_interval = bounding_interval.transposed(-block_index * self.__block_height)

        assert relative_bounding_interval.low < self.__block_height
        assert relative_bounding_interval.high < self.__block_height*2

        line_bounding_intervals = [
            BoundingInterval(self.__padding_height,
                             self.__block_height / 2.0),
            BoundingInterval(
                self.__block_height / 2.0,
                self.__block_height - self.__padding_height)
        ]
        highest_score = -1
        index_at_highest = -1
        bound_at_highest = None
        logger.debug(f"finding line index for {relative_bounding_interval}")
        for line_index in range(2):
            candidate_line = line_bounding_intervals[line_index]
            score = relative_bounding_interval.get_coverage(candidate_line)
            logger.debug(f"candidate_line={candidate_line} score={score}")
            if score > highest_score:
                highest_score = score
                index_at_highest = line_index
                bound_at_highest = line_bounding_intervals[line_index]
                if score > threshold:
                    return index_at_highest

        raise RuntimeError(
            f"line_indexを見つけられませんでした: window_rel_bound={relative_bounding_interval}, highest_score={highest_score}, most_likely_block={bound_at_highest}, most_likely_index={index_at_highest}")
