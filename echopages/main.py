import logging

import uvicorn

import echopages.config
from echopages.api import endpoints
from echopages.application import services
from echopages.infrastructure.database import sql
from echopages.infrastructure.delivery import samplers, schedulers
from echopages.infrastructure.fakes import (
    FakeDigestDeliverySystem,
    FakeDigestFormatter,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    content_repo = sql.get_content_repo(echopages.config.DB_URI)
    digest_repo = sql.get_digest_repo(echopages.config.DB_URI)
    digest_formatter = FakeDigestFormatter()
    delivery_system = FakeDigestDeliverySystem()
    content_sampler = samplers.SimpleContentSampler()

    # Configure Scheduler
    scheduler = schedulers.SimpleScheduler(
        lambda: services.delivery_service(
            content_repo,
            digest_repo,
            content_sampler,
            echopages.config.NUMBER_OF_UNITS_PER_DIGEST,
            digest_formatter,
            delivery_system,
        ),
        time_of_day="07:00",
    )
    scheduler.start()
    uvicorn.run(endpoints.app, host="0.0.0.0", port=8000)
