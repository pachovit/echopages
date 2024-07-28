from typing import Dict

from echopages.application import services
from echopages.bootstrap import (
    get_digest_delivery_system,
    get_digest_formatter,
    get_sampler,
    get_unit_of_work,
)


def sample_content_data(id: int) -> Dict[str, str]:
    return {
        "source": f"source {id}",
        "author": f"author {id}",
        "location": f"location {id}",
        "text": f"text {id}",
    }


def test_trigger_digest() -> None:
    uow = get_unit_of_work()
    digest_formatter = get_digest_formatter()
    delivery_system = get_digest_delivery_system()

    content_sampler = get_sampler()

    with uow:
        assert len(uow.digest_repo.get_all()) == 0
        assert len(uow.content_repo.get_all()) == 0

    # Given: 3 contents
    contents = [sample_content_data(1), sample_content_data(2), sample_content_data(3)]
    for content in contents:
        services.add_content(uow, content)
    with uow:
        assert len(uow.content_repo.get_all()) == 3

    # When: A digest with 3 contents is triggered
    n_samples = 3
    services.delivery_service(
        uow,
        content_sampler,
        n_samples,
        digest_formatter,
        delivery_system,
    )

    # Then: A digest with 3 contents is generated and stored
    with uow:
        digest = uow.digest_repo.get_all()[0]
        for content in contents:
            assert content["source"] in digest.contents_str
            assert content["author"] in digest.contents_str
            assert content["location"] in digest.contents_str
            assert content["text"] in digest.contents_str
        assert digest.sent
