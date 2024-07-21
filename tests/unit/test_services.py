from datetime import datetime, timedelta
from time import sleep
from typing import List, Tuple

from time_machine import travel
from zoneinfo import ZoneInfo

from echopages.application import services
from echopages.domain import model
from echopages.infrastructure.delivery import samplers, schedulers
from echopages.infrastructure.fakes import (
    FakeContentRepository,
    FakeDigestDeliverySystem,
    FakeDigestFormatter,
    FakeDigestRepository,
)


def setup_contents(
    contents: List[str],
) -> Tuple[FakeContentRepository, List[model.Content]]:
    content_repo = FakeContentRepository([])
    content_objects = []

    for n_, content in enumerate(contents):
        content_object = model.Content(id=n_, text=content)
        content_repo.add(content_object)

        content_objects.append(content_object)

    return content_repo, content_objects


def test_user_can_add_contents() -> None:
    # Given: Some content units
    content_repo, _ = setup_contents(["content unit 1", "content unit 2"])

    # When: User adds content units
    services.add_content(content_repo, "content unit 3")

    # Then: Content units are added
    available_content = content_repo.get_all()
    assert len(available_content) == 3
    assert {"content unit 1", "content unit 2", "content unit 3"} == set(
        content.text for content in available_content
    )


def test_user_can_get_contents() -> None:
    content_repo = FakeContentRepository([])
    content_id = services.add_content(content_repo, "content unit 3")

    content = services.get_content_by_id(content_repo, content_id)

    assert content is not None
    assert content.text == "content unit 3"


def test_user_can_get_digests() -> None:
    digest_repo = FakeDigestRepository([])

    digest_repo.add(
        model.Digest(id=123, contents=[model.Content(id=1, text="content unit 3")])
    )

    digest = services.get_digest_by_id(digest_repo, 123)

    assert digest is not None
    assert digest.contents is not None
    assert digest.contents[0].text == "content unit 3"


def test_configure_schedule() -> None:
    # Given: Some schedule
    scheduler = schedulers.SimpleScheduler(lambda: None)
    assert scheduler.time_of_day == "00:00"

    # When: User configures schedule
    services.configure_schedule(scheduler, "07:00")

    # Then: Schedule is changed
    assert scheduler.time_of_day == "07:00"


def test_generate_digest() -> None:
    contents = ["content unit 1", "content unit 2", "content unit 3"]
    content_repo, content_objects = setup_contents(contents)
    digest_repo = FakeDigestRepository([])
    content_sampler = samplers.SimpleContentSampler()
    samplers.CountIndex.value = 0

    number_of_units = 2

    assert len(digest_repo.get_all()) == 0

    digest_id = services.generate_digest(
        content_repo, digest_repo, content_sampler, number_of_units
    )

    digests = digest_repo.get_all()
    assert len(digests) == 1
    assert digest_id == digests[0].id
    assert digests[0].contents == content_objects[:2]
    assert digests[0].sent is False


def test_deliver_digest() -> None:
    contents = ["content unit 1", "content unit 2", "content unit 3"]
    _, content_objects = setup_contents(contents)
    digest_repo = FakeDigestRepository([])

    delivery_system = FakeDigestDeliverySystem()
    digest = model.Digest(id=1, contents=content_objects)
    digest.contents_str = "content unit 1,content unit 2,content unit 3"

    services.deliver_digest(delivery_system, digest_repo, digest)

    assert delivery_system.sent_contents == [
        "content unit 1,content unit 2,content unit 3"
    ]
    assert digest.sent is True


def test_all_flow() -> None:
    content_repo = FakeContentRepository([])
    digest_repo = FakeDigestRepository([])
    digest_formatter = FakeDigestFormatter()
    delivery_system = FakeDigestDeliverySystem()
    content_sampler = samplers.SimpleContentSampler()
    samplers.CountIndex.value = 0

    # Populate contents
    services.add_content(content_repo, "content unit 1")
    services.add_content(content_repo, "content unit 2")

    assert len(digest_repo.get_all()) == 0

    # Let the scheduler do 4 deliveries
    with travel(
        datetime(2020, 1, 1, 19, 0, 0, tzinfo=ZoneInfo("Europe/Berlin")),
        tick=False,
    ) as traveller:
        # Configure Scheduler
        scheduler = schedulers.SimpleScheduler(
            lambda: services.delivery_service(
                content_repo,
                digest_repo,
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

        assert len(digest_repo.get_all()) == 4
        assert len(delivery_system.sent_contents) == 4
        assert delivery_system.sent_contents == [
            "content unit 1",
            "content unit 2",
            "content unit 1",
            "content unit 2",
        ]
