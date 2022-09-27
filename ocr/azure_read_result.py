from ocr.bounding_box import BoundingBox


class AzureReadResult:
    def __init__(self, text: str, bounding_box: BoundingBox):
        self.text = text
        self.bounding_box = bounding_box

    def __repr__(self):
        return f'"{self.text}"{self.bounding_box}'
