from typing import List

from echopages.domain import model


class SimpleContentSampler(model.ContentSampler):
    def __init__(self) -> None:
        super().__init__()
        self.count_index = 0

    def sample(
        self, contents: List[model.Content], number_of_units: int
    ) -> List[model.Content]:
        """
        Returns `number_of_units` content units starting from the current count index.
        If there are not enough content units available, it loops back to the beginning of the list.
        """
        if len(contents) == 0:
            raise ValueError("No content units available")

        contents_length = len(contents)
        sampled_contents = []

        for _ in range(number_of_units):
            sampled_contents.append(contents[self.count_index])
            self.count_index = (self.count_index + 1) % contents_length

        return sampled_contents
