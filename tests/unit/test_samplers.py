from echopages.domain import model
from echopages.infrastructure.delivery import samplers


def test_simple_content_sampler() -> None:
    contents = [
        model.Content(id=0, text="content unit 1"),
        model.Content(id=1, text="content unit 2"),
        model.Content(id=2, text="content unit 3"),
    ]

    content_sampler = samplers.SimpleContentSampler()
    sampled_contents = content_sampler.sample(contents, 8)

    assert len(sampled_contents) == 8
    for n in range(8):
        assert sampled_contents[n].id == (n % 3)
