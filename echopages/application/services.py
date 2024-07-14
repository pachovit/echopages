from typing import List

from echopages.domain import model, repositories


def add_content(content_repo: repositories.ContentRepository, content: str) -> int:
    content_id = content_repo.add(model.Content(text=content))
    return content_id


def configure_schedule(scheduler: model.Scheduler, time_of_day: str) -> None:
    scheduler.configure_schedule(time_of_day)


def sample_contents(
    content_repo: repositories.ContentRepository,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> List[model.Content]:
    contents = content_repo.get_all()
    return content_sampler.sample(contents, number_of_units)


def generate_digest(
    digest_repo: repositories.DigestRepository,
    content_repo: repositories.ContentRepository,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> int:
    contents = sample_contents(content_repo, content_sampler, number_of_units)

    digest = model.Digest(contents=contents)
    digest_id = digest_repo.add(digest)

    return digest_id


def send_digest(
    digest_delivery_system: model.DigestDeliverySystem,
    digest_repo: repositories.DigestRepository,
    digest_id: int,
) -> None:
    digest = digest_repo.get_by_id(digest_id)
    if digest is None:
        raise ValueError(f"Digest with id {digest_id} not found")
    digest_delivery_system.deliver_digest(digest)
    digest.mark_as_sent()


def delivery_service(
    digest_repo: repositories.DigestRepository,
    content_repo: repositories.ContentRepository,
    content_sampler: model.ContentSampler,
    number_of_units: int,
    digest_delivery_system: model.DigestDeliverySystem,
) -> None:
    digest_id = generate_digest(
        digest_repo, content_repo, content_sampler, number_of_units
    )
    send_digest(digest_delivery_system, digest_repo, digest_id)
