from typing import List, Dict

from ocr.normalization_ja import normalize


def create_reverse_normalization_dictionary(words: List[str]) -> Dict[str, str]:
    """
    [正規化後の単語]→[正規化前の単語]の逆引き辞書を作成する
    :param words: 正規化前の単語
    :return: 逆引き辞書
    """

    result: Dict[str, str] = {}
    for word in words:
        normalized = normalize(word)
        assert normalized not in result.keys()
        result[normalized] = word
    return result
