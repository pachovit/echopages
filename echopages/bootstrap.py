import echopages.config
from echopages.domain.model import DigestDeliverySystem, DigestFormatter
from echopages.domain.repositories import UnitOfWork
from echopages.infrastructure.database.file_db import FileUnitOfWork
from echopages.infrastructure.delivery import delivery_system, samplers


def get_unit_of_work() -> UnitOfWork:
    config = echopages.config.get_config()
    return FileUnitOfWork(config.db_uri)


def get_digest_delivery_system() -> DigestDeliverySystem:
    config = echopages.config.get_config()
    if config.delivery_system == "DiskDigestDeliverySystem":
        return delivery_system.DiskDigestDeliverySystem(
            config.disk_delivery_system_directory
        )

    if config.delivery_system == "PostmarkDigestDeliverySystem":
        return delivery_system.PostmarkDigestDeliverySystem(config.recipient_email)
    raise NotImplementedError("No such delivery system")


def get_sampler() -> samplers.SimpleContentSampler:
    return samplers.SimpleContentSampler()


def get_digest_formatter() -> DigestFormatter:
    return delivery_system.HTMLDigestFormatter()
