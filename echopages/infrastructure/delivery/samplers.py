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

        # Start sampling from the last content sent
        if len(digests) == 0:
            content_sampler_index = -1
        else:
            # Get digest with the last content sent
            previously_sent_digests = [
                digest for digest in digests if digest.sent_at is not None
            ]
            if len(previously_sent_digests) == 0:
                last_digest = digests[-1]
            else:
                digest_timestamps = [
                    digest.sent_at
                    for digest in previously_sent_digests
                    if digest.sent_at is not None
                ]
                last_digest_index = digest_timestamps.index(max(digest_timestamps))
                last_digest = previously_sent_digests[last_digest_index]

            last_sent_content_id = max(last_digest.content_ids)
            content_ids = [content.id for content in contents]
            if last_sent_content_id not in content_ids:
                content_sampler_index = -1
            else:
                content_sampler_index = content_ids.index(last_sent_content_id)

        contents_length = len(contents)
        sampled_contents = []

        for _ in range(number_of_units):
            content_sampler_index = (content_sampler_index + 1) % contents_length
            sampled_contents.append(contents[content_sampler_index])

        return sampled_contents
