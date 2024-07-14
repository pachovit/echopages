from datetime import datetime, timedelta
from time import sleep

from time_machine import travel
from zoneinfo import ZoneInfo

from echopages.application import services
from echopages.domain import model
from echopages.infrastructure import samplers, schedulers
from echopages.infrastructure.fakes import (
    FakeContentRepository,
    FakeDigestDeliverySystem,
    FakeDigestRepository,
)


def test_user_can_add_contents():
    # Given: Some content units
    contents = [
        model.Content(id="1", text="content unit 1"),
        model.Content(id="2", text="content unit 2"),
    ]
    contents_repo = FakeContentRepository(contents)

    # When: User adds content units
    services.add_content(contents_repo, "content unit 3")

    # Then: Content units are added
    available_content = contents_repo.get_all()
    assert len(available_content) == 3
    assert {"content unit 1", "content unit 2", "content unit 3"} == set(
        content.text for content in available_content
    )


def test_configure_schedule():
    # Given: Some schedule
    scheduler = schedulers.SimpleScheduler(lambda: None)
    assert scheduler.time_of_day == "00:00"

    # When: User configures schedule
    services.configure_schedule(scheduler, "07:00")

    # Then: Schedule is changed
    assert scheduler.time_of_day == "07:00"


def test_generate_digest():
    digest_repo = FakeDigestRepository([])
    content_sampler = samplers.SimpleContentSampler()
    contents = [
        model.Content(id="1", text="content unit 1"),
        model.Content(id="2", text="content unit 2"),
        model.Content(id="3", text="content unit 3"),
    ]
    content_repo = FakeContentRepository(contents)
    number_of_units = 2
    assert len(digest_repo.get_all()) == 0

    digest_id = services.generate_digest(
        digest_repo, content_repo, content_sampler, number_of_units
    )

    digests = digest_repo.get_all()
    assert len(digests) == 1
    assert digest_id == digests[0].id
    assert digests[0].contents == contents[:2]
    assert digests[0].sent is False


def test_send_digest():
    contents = [
        model.Content(id="1", text="content unit 1"),
        model.Content(id="2", text="content unit 2"),
        model.Content(id="3", text="content unit 3"),
    ]
    delivery_system = FakeDigestDeliverySystem()
    digest = model.Digest(id="d1", contents=contents)
    digest_repo = FakeDigestRepository([digest])

    services.send_digest(delivery_system, digest_repo, "d1")

    digests = digest_repo.get_all()
    assert delivery_system.sent_contents == [
        "content unit 1,content unit 2,content unit 3"
    ]
    assert digests[0].sent is True


def test_all_flow():
    content_repo = FakeContentRepository([])
    digest_repo = FakeDigestRepository([])
    delivery_system = FakeDigestDeliverySystem()
    content_sampler = samplers.SimpleContentSampler()

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
                digest_repo, content_repo, content_sampler, 1, delivery_system
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
