from datetime import datetime, timedelta
from time import sleep
from typing import Dict, List

from time_machine import travel
from zoneinfo import ZoneInfo

from echopages.application import services
from echopages.domain import model
from echopages.infrastructure.delivery import samplers, schedulers
from tests.fakes import (
    FakeDigestDeliverySystem,
    FakeDigestFormatter,
    FakeUnitOfWork,
)


def sample_content_data(id: int) -> Dict[str, str]:
    return {
        "source": f"source {id}",
        "author": f"author {id}",
        "location": f"location {id}",
        "text": f"text {id}",
    }


def setup_contents(
    uow: FakeUnitOfWork,
    content_datas: List[Dict[str, str]],
) -> List[model.Content]:
    content_objects = []

    for n_, content_data in enumerate(content_datas):
        content_object = model.Content(
            id=n_,
            source=content_data["source"],
            author=content_data["author"],
            location=content_data["location"],
            text=content_data["text"],
        )
        uow.content_repo.add(content_object)

        content_objects.append(content_object)

    return content_objects


def test_user_can_add_contents() -> None:
    # Given: Some content units
    uow = FakeUnitOfWork()
    content_data_1 = sample_content_data(1)
    content_data_2 = sample_content_data(2)
    content_data_3 = sample_content_data(3)
    _ = setup_contents(uow, [content_data_1, content_data_2])

    # When: User adds content units
    services.add_content(uow, content_data_3)

    # Then: Content units are added
    available_content = uow.content_repo.get_all()
    assert len(available_content) == 3
    assert {f"source {id}" for id in range(1, 4)} == set(
        content.source for content in available_content
    )
    assert {f"author {id}" for id in range(1, 4)} == set(
        content.author for content in available_content
    )
    assert {f"location {id}" for id in range(1, 4)} == set(
        content.location for content in available_content
    )
    assert {f"text {id}" for id in range(1, 4)} == set(
        content.text for content in available_content
    )


def test_user_can_get_contents() -> None:
    uow = FakeUnitOfWork()
    content_data = sample_content_data(3)
    content_id = services.add_content(uow, content_data)

    saved_content = services.get_content_by_id(uow, content_id)

    assert saved_content is not None
    saved_content.pop("id")
    assert saved_content == content_data


def test_configure_schedule() -> None:
    # Given: Some schedule
    scheduler = schedulers.SimpleScheduler(lambda: None)
    assert scheduler.time_of_day == "00:00"

    # When: User configures schedule
    services.configure_schedule(scheduler, "07:00")

    # Then: Schedule is changed
    assert scheduler.time_of_day == "07:00"


def test_generate_digest() -> None:
    uow = FakeUnitOfWork()
    contents = [sample_content_data(1), sample_content_data(2), sample_content_data(3)]
    content_objects = setup_contents(uow, contents)

    content_sampler = samplers.SimpleContentSampler()

    number_of_units = 2

    assert len(uow.digest_repo.get_all()) == 0

    digest_id = services.generate_digest(uow, content_sampler, number_of_units)

    digests = uow.digest_repo.get_all()
    assert len(digests) == 1
    assert digest_id == digests[0].id
    assert digests[0].content_ids == [
        content.id for content in content_objects[:number_of_units]
    ]
    assert digests[0].sent is False


def test_deliver_digest() -> None:
    uow = FakeUnitOfWork()
    contents = [sample_content_data(1), sample_content_data(2), sample_content_data(3)]
    content_objects = setup_contents(uow, contents)

    delivery_system = FakeDigestDeliverySystem()

    digest = model.Digest(id=1, content_ids=[content.id for content in content_objects])  # type: ignore
    digest.contents_str = "content unit 1,content unit 2,content unit 3"
    uow.digest_repo.add(digest)

    services.deliver_digest(delivery_system, uow, 1)

    assert delivery_system.sent_contents == [
        "content unit 1,content unit 2,content unit 3"
    ]
    assert digest.sent is True


def test_format_digest() -> None:
    uow = FakeUnitOfWork()
    digest_formatter = FakeDigestFormatter()
    uow.content_repo.add(
        model.Content(
            id=1,
            source="source 1",
            author="author 1",
            location="location 1",
            text="content unit 1",
        )
    )
    digest = model.Digest(id=1, content_ids=[1])
    uow.digest_repo.add(digest)

    services.format_digest(uow, digest_formatter, 1)

    assert (
        digest.contents_str
        == "{'id': 1, 'text': 'content unit 1', 'source': 'source 1', 'author': 'author 1', 'location': 'location 1'}"
    )


def test_trigger_digest() -> None:
    uow = FakeUnitOfWork()
    digest_formatter = FakeDigestFormatter()
    delivery_system = FakeDigestDeliverySystem()

    content_sampler = samplers.SimpleContentSampler()

    # Given: 3 contents
    contents = [sample_content_data(1), sample_content_data(2), sample_content_data(3)]
    for content in contents:
        services.add_content(uow, content)

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
    digest = uow.digest_repo.get_all()[0]
    for content in contents:
        assert content["source"] in digest.contents_str
        assert content["author"] in digest.contents_str
        assert content["location"] in digest.contents_str
        assert content["text"] in digest.contents_str
    assert digest.sent


def test_all_flow() -> None:
    uow = FakeUnitOfWork()
    digest_formatter = FakeDigestFormatter()
    delivery_system = FakeDigestDeliverySystem()
    content_sampler = samplers.SimpleContentSampler()

    # Populate contents
    services.add_content(uow, sample_content_data(1))
    services.add_content(uow, sample_content_data(2))

    assert len(uow.digest_repo.get_all()) == 0

    # Let the scheduler do 4 deliveries
    with travel(
        datetime(2020, 1, 1, 19, 0, 0, tzinfo=ZoneInfo("Europe/Berlin")),
        tick=False,
    ) as traveller:
        # Configure Scheduler
        scheduler = schedulers.SimpleScheduler(
            lambda: services.delivery_service(
                uow,
                content_sampler,
                1,
                digest_formatter,
                delivery_system,
            ),
            sleep_interval=0.05,
        )
        services.configure_schedule(scheduler, "07:00")
        scheduler.start()

        # Move time forward to trigger 4 deliveries
        for _ in range(4):
            traveller.shift(delta=timedelta(days=1))
            sleep(0.1)
        scheduler.stop()

        assert len(uow.digest_repo.get_all()) == 4
        assert len(delivery_system.sent_contents) == 4
        assert delivery_system.sent_contents == [
            "{'id': 1, 'text': 'text 1', 'source': 'source 1', 'author': 'author 1', 'location': 'location 1'}",
            "{'id': 2, 'text': 'text 2', 'source': 'source 2', 'author': 'author 2', 'location': 'location 2'}",
            "{'id': 1, 'text': 'text 1', 'source': 'source 1', 'author': 'author 1', 'location': 'location 1'}",
            "{'id': 2, 'text': 'text 2', 'source': 'source 2', 'author': 'author 2', 'location': 'location 2'}",
        ]
