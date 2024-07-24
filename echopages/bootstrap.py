import echopages.config
from echopages.domain.model import DigestDeliverySystem
from echopages.domain.repositories import UnitOfWork
from echopages.infrastructure.database.file_db import FileUnitOfWork
from echopages.infrastructure.delivery.delivery_system import DiskDigestDeliverySystem
from echopages.infrastructure.fakes import FakeDigestDeliverySystem


def get_unit_of_work() -> UnitOfWork:
    return FileUnitOfWork(echopages.config.DB_URI)


def get_digest_delivery_system() -> DigestDeliverySystem:
    if echopages.config.DELIVERY_SYSTEM == "DiskDigestDeliverySystem":
        return DiskDigestDeliverySystem(echopages.config.DISK_DELIVERY_SYSTEM_DIRECTORY)

    return FakeDigestDeliverySystem()
