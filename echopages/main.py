import logging

import uvicorn

import echopages.config
from echopages import bootstrap
from echopages.application import services
from echopages.infrastructure import samplers, schedulers, web
from echopages.infrastructure.fakes import (
    FakeDigestDeliverySystem,
    FakeDigestRepository,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    content_repo = bootstrap.get_content_repo(echopages.config.DB_URI)
    digest_repo = FakeDigestRepository([])
    delivery_system = FakeDigestDeliverySystem()
    content_sampler = samplers.SimpleContentSampler()

    # Configure Scheduler
    scheduler = schedulers.SimpleScheduler(
        lambda: services.delivery_service(
            digest_repo, content_repo, content_sampler, 1, delivery_system
        ),
        time_of_day="14:33",
    )
    scheduler.start()
    uvicorn.run(web.app, host="0.0.0.0", port=8000)
