from typing import List

from echopages.domain import model

COUNT_INDEX = 0


class SimpleContentSampler(model.ContentSampler):
    def __init__(self) -> None:
        super().__init__()

    def sample(
        self, contents: List[model.Content], number_of_units: int
    ) -> List[model.Content]:
        """
        Returns `number_of_units` content units starting from the current count index.
        If there are not enough content units available, it loops back to the beginning of the list.
        """
        global COUNT_INDEX
        if len(contents) == 0:
            raise ValueError("No content units available")

        contents_length = len(contents)
        sampled_contents = []

        for _ in range(number_of_units):
            sampled_contents.append(contents[COUNT_INDEX])
            COUNT_INDEX = (COUNT_INDEX + 1) % contents_length

        return sampled_contents
