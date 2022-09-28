import re
from typing import AnyStr, Pattern

from ocr.normalization_ja import normalize


def normalized_search(pattern: Pattern[AnyStr], text: str):
    return re.search(normalize(str(pattern)), normalize(text))

