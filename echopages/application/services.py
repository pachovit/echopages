from typing import List, Optional

from echopages.domain import model, repositories


def add_content(
    content_repo: repositories.ContentRepository,
    content: str,
) -> int:
    content_id = content_repo.add(model.Content(text=content))

    return content_id


def get_content_by_id(
    content_repo: repositories.ContentRepository,
    content_id: int,
) -> Optional[model.Content]:
    content = content_repo.get_by_id(content_id)

    if content is None:
        return None
    new_content = model.Content(id=content_id, text=content.text)
    return new_content


def get_digest_by_id(
    digest_repo: repositories.DigestRepository,
    digest_id: int,
) -> Optional[model.Digest]:
    digest = digest_repo.get_by_id(digest_id)
    if digest is None:
        return None
    contents = digest.contents
    if contents is None:
        contents = []
    new_content = model.Digest(
        id=digest.id,
        contents=[
            model.Content(id=content.id, text=content.text) for content in contents
        ],
    )
    return new_content


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
    content_repo: repositories.ContentRepository,
    digest_repo: repositories.DigestRepository,
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
    digest_repo.update(digest)


def delivery_service(
    content_repo: repositories.ContentRepository,
    digest_repo: repositories.DigestRepository,
    content_sampler: model.ContentSampler,
    number_of_units: int,
    digest_delivery_system: model.DigestDeliverySystem,
) -> model.Digest:
    digest_id = generate_digest(
        content_repo, digest_repo, content_sampler, number_of_units
    )
    send_digest(digest_delivery_system, digest_repo, digest_id)
    digest = get_digest_by_id(digest_repo, digest_id)
    assert digest is not None
    return digest
