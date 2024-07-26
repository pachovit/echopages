from typing import Any, Dict, List, Optional

from echopages.domain import model, repositories


def add_content(
    uow: repositories.UnitOfWork,
    content_data: Dict[str, str],
) -> int:
    with uow:
        content_id = uow.content_repo.add(model.Content(id=None, **content_data))
        uow.commit()
    return content_id


def get_content_by_id(
    uow: repositories.UnitOfWork,
    content_id: int,
) -> Optional[Dict[str, Any]]:
    with uow:
        content = uow.content_repo.get_by_id(content_id)

        if content is None:
            return None
        content_data = content.__dict__
    return content_data


def configure_schedule(scheduler: model.Scheduler, time_of_day: str) -> None:
    scheduler.configure_schedule(time_of_day)


def sample_contents(
    uow: repositories.UnitOfWork,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> List[model.Content]:
    with uow:
        contents = uow.content_repo.get_all()
    return content_sampler.sample(contents, number_of_units)


def generate_digest(
    uow: repositories.UnitOfWork,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> int:
    contents = sample_contents(uow, content_sampler, number_of_units)

    content_ids = [c.id for c in contents]

    digest = model.Digest(content_ids=content_ids)  # type: ignore
    with uow:
        digest_id = uow.digest_repo.add(digest)
        uow.commit()

    return digest_id


def deliver_digest(
    digest_delivery_system: model.DigestDeliverySystem,
    uow: repositories.UnitOfWork,
    digest_id: int,
) -> None:
    with uow:
        digest = uow.digest_repo.get_by_id(digest_id)
        assert digest is not None
        digest_delivery_system.deliver_digest(digest.contents_str)
        digest.mark_as_sent()
        uow.digest_repo.update(digest)
        uow.commit()


def format_digest(
    uow: repositories.UnitOfWork,
    digest_formatter: model.DigestFormatter,
    digest_id: int,
) -> str:
    with uow:
        digest = uow.digest_repo.get_by_id(digest_id)
        assert digest is not None

        contents = []
        for content_id in digest.content_ids:
            content = uow.content_repo.get_by_id(content_id)
            assert content is not None
            contents.append(content)

        digest_str = digest_formatter.format(contents)
        digest.store_content_str(digest_str)
        uow.digest_repo.update(digest)
        uow.commit()
        content_str = digest.contents_str
    return content_str


def delivery_service(
    uow: repositories.UnitOfWork,
    content_sampler: model.ContentSampler,
    number_of_units: int,
    digest_formatter: model.DigestFormatter,
    digest_delivery_system: model.DigestDeliverySystem,
) -> str:
    with uow:
        digest_id = generate_digest(uow, content_sampler, number_of_units)

        content_str = format_digest(uow, digest_formatter, digest_id)
        deliver_digest(digest_delivery_system, uow, digest_id)
    return content_str
