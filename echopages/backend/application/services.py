import logging
from typing import Any, Dict, List, Optional, Tuple

import echopages.backend.config
from echopages.backend.domain import model, repositories

logger = logging.getLogger(__name__)


def add_content(
    uow: repositories.UnitOfWork,
    content_data: Dict[str, str],
) -> int:
    """Adds a new content to the content repository.

    Args:
        uow (repositories.UnitOfWork): The unit of work instance.
        content_data (Dict[str, str]): A dictionary containing the content data.

    Returns:
        int: The ID of the newly added content.

    Raises:
        None.
    """
    logger.info("Adding content")
    with uow:
        content = model.Content(id=None, **content_data)
        content_id = uow.content_repo.add(content)
        uow.commit()
    return content_id


def get_content_by_id(
    uow: repositories.UnitOfWork,
    content_id: int,
) -> Optional[Dict[str, Any]]:
    logger.debug(f"Getting content {content_id} by ID")
    with uow:
        content = uow.content_repo.get_by_id(content_id)

        if content is None:
            return None
        content_data = content.__dict__
    return content_data


def get_all_content(
    uow: repositories.UnitOfWork,
) -> Optional[List[Dict[str, Any]]]:
    logger.debug("Getting all content")
    with uow:
        content = uow.content_repo.get_all()

        if content is None:
            return None

        all_content_data = [c.__dict__ for c in content]

    return all_content_data


def configure_schedule(scheduler: model.Scheduler, time_of_day: str) -> None:
    scheduler.configure_schedule(time_of_day)


def sample_contents(
    uow: repositories.UnitOfWork,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> List[model.Content]:
    logger.debug(
        (
            f"Using sampler {content_sampler.__class__.__name__} to "
            f"sample '{number_of_units}' content units"
        )
    )
    with uow:
        contents = uow.content_repo.get_all()
        digests = uow.digest_repo.get_all()
    return content_sampler.sample(digests, contents, number_of_units)


def generate_digest(
    uow: repositories.UnitOfWork,
    content_sampler: model.ContentSampler,
    number_of_units: int,
) -> int:
    logger.debug(f"Generating a digest of {number_of_units} content units")
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
    digest_repr: model.DigestRepr,
) -> None:
    logger.debug(f"Delivering digest of id {digest_id}, and title {digest_repr.title}")
    with uow:
        digest = uow.digest_repo.get_by_id(digest_id)
        assert digest is not None

        digest_delivery_system.deliver_digest(digest_repr)
        digest.mark_as_sent()
        uow.digest_repo.update(digest)
        uow.commit()


def format_digest(
    uow: repositories.UnitOfWork,
    digest_formatter: model.DigestFormatter,
    digest_id: int,
) -> Tuple[model.DigestTitle, model.DigestContentStr]:
    logger.debug(f"Formatting digest of id {digest_id}")
    with uow:
        digest = uow.digest_repo.get_by_id(digest_id)
        assert digest is not None

        contents = []
        for content_id in digest.content_ids:
            content = uow.content_repo.get_by_id(content_id)
            assert content is not None
            contents.append(content)

        digest_repr = digest_formatter.format(contents)

    return digest_repr.title, digest_repr.contents_str


def delivery_service(
    uow: repositories.UnitOfWork,
    content_sampler: model.ContentSampler,
    digest_formatter: model.DigestFormatter,
    digest_delivery_system: model.DigestDeliverySystem,
) -> Tuple[model.DigestTitle, model.DigestContentStr]:
    logger.info(
        (
            f"Triggering a digest delivery, with sampler {content_sampler}",
            f"formatter {digest_formatter} and delivery {digest_delivery_system}",
        )
    )

    with uow:
        number_of_units = (
            echopages.backend.config.get_config().number_of_units_per_digest
        )

        digest_id = generate_digest(uow, content_sampler, number_of_units)

        digest_title, digest_content_str = format_digest(
            uow, digest_formatter, digest_id
        )
        deliver_digest(
            digest_delivery_system,
            uow,
            digest_id,
            model.DigestRepr(digest_title, digest_content_str),
        )

    return digest_title, digest_content_str


def update_digest_config(
    scheduler: model.Scheduler,
    number_of_units_per_digest: int,
    daily_time_of_digest: str,
) -> None:
    logger.info(
        (
            "Updating digest config with "
            f"number_of_units_per_digest={number_of_units_per_digest}, "
            f"daily_time_of_digest={daily_time_of_digest}"
        )
    )
    config = echopages.backend.config.get_config()
    config.number_of_units_per_digest = number_of_units_per_digest
    config.daily_time_of_digest = daily_time_of_digest
    echopages.backend.config.write_config(config)
    scheduler.configure_schedule(daily_time_of_digest)
