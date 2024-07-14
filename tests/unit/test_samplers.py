from echopages.domain import model
from echopages.infrastructure import samplers


def test_simple_content_sampler():
    content_units = [
        model.ContentUnit(id="0", text="content unit 1"),
        model.ContentUnit(id="1", text="content unit 2"),
        model.ContentUnit(id="2", text="content unit 3"),
    ]

    content_sampler = samplers.SimpleContentSampler()
    sampled_content_units = content_sampler.sample(content_units, 8)

    assert len(sampled_content_units) == 8
    for n in range(8):
        assert sampled_content_units[n].id == str(n % 3)
