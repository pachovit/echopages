from typing import List

from echopages.domain import model


class SimpleContentSampler(model.ContentSampler):
    def sample(
        self, content_units: List[model.ContentUnit], number_of_units: int
    ) -> List[model.ContentUnit]:
        return content_units[:number_of_units]
