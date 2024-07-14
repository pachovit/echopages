from typing import List

from echopages.domain import model, repositories


def add_content(unit_of_work: repositories.UnitOfWork, content: str) -> int:
    with unit_of_work:
        content_id = unit_of_work.content_repo.add(model.Content(text=content))
        unit_of_work.commit()
    return content_id


def get_content_by_id(
    unit_of_work: repositories.UnitOfWork, content_id: int
) -> model.Content:
    with unit_of_work:
        content = unit_of_work.content_repo.get_by_id(content_id)
        new_content = model.Content(id=content.id, text=content.text)
    return new_content


def get_digest_by_id(
    unit_of_work: repositories.UnitOfWork, digest_id: int
) -> model.Digest:
    with unit_of_work:
        digest = unit_of_work.digest_repo.get_by_id(digest_id)
        new_content = model.Digest(
            id=digest.id,
            contents=[
                model.Content(id=content.id, text=content.text)
                for content in digest.contents
            ],
        )
    return new_content


def configure_schedule(scheduler: model.Scheduler, time_of_day: str) -> None:
    scheduler.configure_schedule(time_of_day)


def sample_contents(
    unit_of_work: repositories.UnitOfWork,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> List[model.Content]:
    with unit_of_work:
        contents = unit_of_work.content_repo.get_all()
    return content_sampler.sample(contents, number_of_units)


def generate_digest(
    unit_of_work: repositories.UnitOfWork,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> int:
    contents = sample_contents(unit_of_work, content_sampler, number_of_units)

    digest = model.Digest(contents=contents)
    with unit_of_work:
        digest_id = unit_of_work.digest_repo.add(digest)
        unit_of_work.commit()

    return digest_id


def send_digest(
    digest_delivery_system: model.DigestDeliverySystem,
    unit_of_work: repositories.UnitOfWork,
    digest_id: int,
) -> None:
    with unit_of_work:
        digest = unit_of_work.digest_repo.get_by_id(digest_id)
        if digest is None:
            raise ValueError(f"Digest with id {digest_id} not found")
        digest_delivery_system.deliver_digest(digest)
        digest.mark_as_sent()
        unit_of_work.commit()


def delivery_service(
    unit_of_work: repositories.UnitOfWork,
    content_sampler: model.ContentSampler,
    number_of_units: int,
    digest_delivery_system: model.DigestDeliverySystem,
) -> model.Digest:
    digest_id = generate_digest(unit_of_work, content_sampler, number_of_units)
    send_digest(digest_delivery_system, unit_of_work, digest_id)

    return get_digest_by_id(unit_of_work, digest_id)
