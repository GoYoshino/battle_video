def normalize(text: str) -> str:
    result = text.replace("ぁ", "あ").replace("ぃ", "い").replace("ぅ", "う").replace("ぇ", "え").replace("ぉ", "お") \
        .replace("っ", "つ").replace("ゃ", "や").replace("ゅ", "ゆ").replace("ょ", "よ") \
        .replace("ァ", "ア").replace("ィ", "イ").replace("ゥ", "ウ").replace("ェ", "エ").replace("ォ", "オ") \
        .replace("ッ", "ツ").replace("ャ", "ヤ").replace("ュ", "ユ").replace("ョ", "ヨ")

    return result
