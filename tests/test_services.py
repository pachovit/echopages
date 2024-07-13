from typing import List

from echopages.application import services
from echopages.domain import model, repositories
from echopages.infrastructure import samplers, schedulers


class FakeContentRepository(repositories.ContentRepository):
    def __init__(self, content_units: List[model.ContentUnit]):
        self.content_units = content_units

    def get_all(self) -> List[model.ContentUnit]:
        return self.content_units

    def add(self, content_unit: model.ContentUnit):
        self.content_units.append(content_unit)


class FakeDigestRepository(repositories.DigestRepository):
    def __init__(self, digests: List[model.Digest]):
        self.digests = digests

    def get(self, digest_id: str) -> model.Digest:
        return next(d for d in self.digests if d.id == digest_id)

    def get_all(self) -> List[model.Digest]:
        return self.digests

    def add(self, digest: model.ContentUnit):
        self.digests.append(digest)


class FakeDigestDeliverySystem(model.DigestDeliverySystem):
    sent_contents = ""

    def deliver_digest(self, digest: model.Digest) -> None:
        self.sent_contents = ",".join([content.data for content in digest.contents])


def test_user_can_add_content_units():
    # Given: Some content units
    content_units = [
        model.ContentUnit(id="1", data="content unit 1"),
        model.ContentUnit(id="2", data="content unit 2"),
    ]
    contents_repo = FakeContentRepository(content_units)

    # When: User adds content units
    services.add_content(contents_repo, "content unit 3")

    # Then: Content units are added
    available_content = contents_repo.get_all()
    assert len(available_content) == 3
    assert {"content unit 1", "content unit 2", "content unit 3"} == set(
        content.data for content in available_content
    )


def test_configure_schedule():
    # Given: Some schedule
    scheduler = schedulers.SimpleScheduler(lambda: None)
    assert scheduler.schedule.time_of_day.hour == 0
    assert scheduler.schedule.time_of_day.minute == 0

    # When: User configures schedule
    services.configure_schedule(scheduler, "07:00")

    # Then: Schedule is changed
    assert scheduler.schedule.time_of_day.hour == 7
    assert scheduler.schedule.time_of_day.minute == 0


def test_generate_digest():
    digest_repo = FakeDigestRepository([])
    content_sampler = samplers.SimpleContentSampler()
    content_units = [
        model.ContentUnit(id="1", data="content unit 1"),
        model.ContentUnit(id="2", data="content unit 2"),
        model.ContentUnit(id="3", data="content unit 3"),
    ]
    content_repo = FakeContentRepository(content_units)
    number_of_units = 2
    assert len(digest_repo.get_all()) == 0

    digest_id = services.generate_digest(
        digest_repo, content_repo, content_sampler, number_of_units
    )

    digests = digest_repo.get_all()
    assert len(digests) == 1
    assert digest_id == digests[0].id
    assert digests[0].contents == content_units[:2]
    assert digests[0].sent is False


def test_send_digest():
    content_units = [
        model.ContentUnit(id="1", data="content unit 1"),
        model.ContentUnit(id="2", data="content unit 2"),
        model.ContentUnit(id="3", data="content unit 3"),
    ]
    delivery_system = FakeDigestDeliverySystem()
    digest = model.Digest(id="d1", contents=content_units)
    digest_repo = FakeDigestRepository([digest])

    services.send_digest(delivery_system, digest_repo, "d1")

    digests = digest_repo.get_all()
    assert (
        delivery_system.sent_contents == "content unit 1,content unit 2,content unit 3"
    )
    assert digests[0].sent is True
