from typing import List

from echopages.domain import model


class SimpleContentSampler(model.ContentSampler):
    def __init__(self):
        super().__init__()
        self.count_index = 0

    def sample(
        self, content_units: List[model.ContentUnit], number_of_units: int
    ) -> List[model.ContentUnit]:
        """
        Returns `number_of_units` content units starting from the current count index.
        If there are not enough content units available, it loops back to the beginning of the list.
        """
        if len(content_units) == 0:
            raise ValueError("No content units available")

        content_units_length = len(content_units)
        sampled_content_units = []

        for _ in range(number_of_units):
            sampled_content_units.append(content_units[self.count_index])
            self.count_index = (self.count_index + 1) % content_units_length

        return sampled_content_units
