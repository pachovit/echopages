import echopages.config
from echopages.domain.model import DigestDeliverySystem, DigestFormatter
from echopages.domain.repositories import UnitOfWork
from echopages.infrastructure.database.file_db import FileUnitOfWork
from echopages.infrastructure.delivery import delivery_system, samplers


def get_unit_of_work() -> UnitOfWork:
    return FileUnitOfWork(echopages.config.DB_URI)


def get_digest_delivery_system() -> DigestDeliverySystem:
    if echopages.config.DELIVERY_SYSTEM == "DiskDigestDeliverySystem":
        return delivery_system.DiskDigestDeliverySystem(
            echopages.config.DISK_DELIVERY_SYSTEM_DIRECTORY
        )

    if echopages.config.DELIVERY_SYSTEM == "PostmarkDigestDeliverySystem":
        return delivery_system.PostmarkDigestDeliverySystem(
            echopages.config.RECIPIENT_EMAIL
        )
    raise NotImplementedError("No such delivery system")


def get_sampler() -> samplers.SimpleContentSampler:
    return samplers.SimpleContentSampler()


def get_digest_formatter() -> DigestFormatter:
    return delivery_system.HTMLDigestFormatter()
