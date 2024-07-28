from typing import List

from echopages.domain import model
from echopages.infrastructure.delivery import samplers


def test_simple_content_sampler_no_digests() -> None:
    contents = [
        model.Content(id=0, text="content unit 1"),
        model.Content(id=1, text="content unit 2"),
        model.Content(id=2, text="content unit 3"),
    ]
    digests: List[model.Digest] = []

    content_sampler = samplers.SimpleContentSampler()
    sampled_contents = content_sampler.sample(digests, contents, 8)

    assert len(sampled_contents) == 8
    for n in range(8):
        assert sampled_contents[n].id == (n % 3)


def test_simple_content_sampler_previous_digests() -> None:
    content_ids = [1, 3, 5]
    contents = [
        model.Content(id=1, text="content unit 1"),
        model.Content(id=3, text="content unit 3"),
        model.Content(id=5, text="content unit 5"),
    ]
    digests = [
        model.Digest(id=0, content_ids=[5]),
        model.Digest(id=1, content_ids=[1, 3]),
    ]

    content_sampler = samplers.SimpleContentSampler()
    sampled_contents = content_sampler.sample(digests, contents, 8)

    assert len(sampled_contents) == 8
    for n in range(8):
        assert sampled_contents[n].id == content_ids[(n + 2) % 3]
