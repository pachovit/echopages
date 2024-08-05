import echopages.config
from echopages.domain.model import DigestDeliverySystem, DigestFormatter, Scheduler
from echopages.domain.repositories import UnitOfWork
from echopages.infrastructure.database.file_db import FileUnitOfWork
from echopages.infrastructure.delivery import delivery_system, samplers
from echopages.infrastructure.delivery import schedulers
from echopages.application import services


def get_unit_of_work() -> UnitOfWork:
    """Get a unit of work for the application based on the configuration."""
    config = echopages.config.get_config()
    return FileUnitOfWork(config.db_uri)


def get_digest_delivery_system() -> DigestDeliverySystem:
    """Get the digest delivery system based on the configuration."""
    config = echopages.config.get_config()
    if config.delivery_system == "FileDigestDeliverySystem":
        return delivery_system.FileDigestDeliverySystem(
            config.file_delivery_system_directory
        )

    if config.delivery_system == "PostmarkDigestDeliverySystem":
        return delivery_system.PostmarkDigestDeliverySystem(config.recipient_email)
    raise NotImplementedError("No such delivery system")


def get_sampler() -> samplers.SimpleContentSampler:
    """Get the content sampler based on the configuration."""
    return samplers.SimpleContentSampler()


def get_digest_formatter() -> DigestFormatter:
    """Get the digest formatter based on the configuration."""
    return delivery_system.HTMLDigestFormatter()


scheduler = None


def get_scheduler() -> Scheduler:
    global scheduler
    if scheduler is not None:
        return scheduler
    # TODO: This should be outside
    uow = get_unit_of_work()
    digest_formatter = get_digest_formatter()
    digest_delivery_system = get_digest_delivery_system()
    content_sampler = get_sampler()
    config = echopages.config.get_config()

    scheduler = schedulers.SimpleScheduler(
        lambda: services.delivery_service(
            uow,
            content_sampler,
            digest_formatter,
            digest_delivery_system,
        ),
        time_of_day=config.daily_time_of_digest,
    )
    return scheduler
