from typing import List

from echopages.domain import model


class SimpleContentSampler(model.ContentSampler):
    def __init__(self) -> None:
        super().__init__()

    def sample(
        self,
        digests: List[model.Digest],
        contents: List[model.Content],
        number_of_units: int,
    ) -> List[model.Content]:
        """
        Returns `number_of_units` content units starting from the last content sent.
        If there are not enough content units available, it loops back to the beginning of the list.
        """
        if len(contents) == 0:
            raise ValueError("No content units available")

        # TODO: Indices are not a direct match to IDs, neither for digests nor for contents.

        # Start sampling from the last content sent
        if len(digests) == 0:
            content_sampler_index = -1
        else:
            last_sent_content_id = max(digests[-1].content_ids)
            content_sampler_index = [content.id for content in contents].index(
                last_sent_content_id
            )
            print()

        contents_length = len(contents)
        sampled_contents = []

        for _ in range(number_of_units):
            content_sampler_index = (content_sampler_index + 1) % contents_length
            sampled_contents.append(contents[content_sampler_index])

        return sampled_contents
