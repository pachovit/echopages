import glob
from typing import Dict

import echopages.config
from echopages.application import services
from echopages.bootstrap import (
    get_digest_delivery_system,
    get_digest_formatter,
    get_sampler,
    get_unit_of_work,
)
from echopages.infrastructure.delivery.delivery_system import FileDigestDeliverySystem


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
    assert isinstance(delivery_system, FileDigestDeliverySystem)

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
    echopages.config.get_config().number_of_units_per_digest = 3
    services.delivery_service(
        uow,
        content_sampler,
        digest_formatter,
        delivery_system,
    )

    # Then: A digest with 3 contents is generated and stored
    with uow:
        digest = uow.digest_repo.get_all()[0]
        assert digest.sent_at is not None
    digest_file = next(iter(glob.glob(f"{delivery_system.directory}/*.html")))
    with open(digest_file) as delivered_digest:
        delivered_digest_content = delivered_digest.read()
        for content in contents:
            assert content["source"] in delivered_digest_content
            assert content["author"] in delivered_digest_content
            assert content["location"] in delivered_digest_content
            assert content["text"] in delivered_digest_content
