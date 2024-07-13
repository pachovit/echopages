import uuid
from typing import List

from echopages.domain import model, repositories


def add_content(content_repo: repositories.ContentRepository, content: str) -> None:
    content_repo.add(model.ContentUnit(id=str(uuid.uuid4()), data=content))


def configure_schedule(scheduler: model.Scheduler, time_of_day_str: str) -> None:
    schedule = model.Schedule(
        days_of_week=[0, 1, 2, 3, 4, 5, 6], time_of_day_str=time_of_day_str
    )
    scheduler.configure_schedule(schedule)


def sample_contents(
    content_repo: repositories.ContentRepository,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> List[model.ContentUnit]:
    content_units = content_repo.get_all()
    return content_sampler.sample(content_units, number_of_units)


def generate_digest(
    digest_repo: repositories.DigestRepository,
    content_repo: repositories.ContentRepository,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> str:
    contents = sample_contents(content_repo, content_sampler, number_of_units)

    digest = model.Digest(id=str(uuid.uuid4()), contents=contents)
    digest_repo.add(digest)

    return digest.id


def send_digest(
    digest_delivery_system: model.DigestDeliverySystem,
    digest_repo: repositories.DigestRepository,
    digest_id: str,
) -> None:
    digest = digest_repo.get(digest_id)
    digest_delivery_system.deliver_digest(digest)
    digest.mark_as_sent()
