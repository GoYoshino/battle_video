class BoundingBox:

    def __init__(self, left: float, top: float, right: float, bottom: float):
        assert left < right
        assert top < bottom

        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def get_area(self) -> float:
        return (self.right - self.left) * (self.bottom - self.top)

    def get_intersection_coverage(self, container) -> float:
        left = max(self.left, container.left)
        top = max(self.top, container.top)
        right = min(self.right, container.right)
        bottom = min(self.bottom, container.bottom)

        if right < left or bottom < top:
            return 0.0

        intersection_area = (right - left) * (bottom - top)

        coverage = intersection_area / (self.get_area())
        assert coverage >= 0.0
        return coverage
