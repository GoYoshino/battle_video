from ocr.bounding_box import BoundingBox
from ocr.bounding_interval import BoundingInterval


class AzureReadResult:
    def __init__(self, text: str, bounding_box: BoundingBox):
        self.text = text
        self.bounding_box = bounding_box
        self.y_bounding_interval = BoundingInterval(bounding_box.top, bounding_box.bottom)

    def __repr__(self):
        return f'"{self.text}"{self.bounding_box}'
