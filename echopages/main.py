import logging

import uvicorn

import echopages.bootstrap as bootstrap
import echopages.config
from echopages.api import endpoints
from echopages.application import services
from echopages.infrastructure.delivery import schedulers

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    uow = bootstrap.get_unit_of_work()
    digest_formatter = bootstrap.get_digest_formatter()
    digest_delivery_system = bootstrap.get_digest_delivery_system()
    content_sampler = bootstrap.get_sampler()

    # Configure Scheduler
    scheduler = schedulers.SimpleScheduler(
        lambda: services.delivery_service(
            uow,
            content_sampler,
            echopages.config.NUMBER_OF_UNITS_PER_DIGEST,
            digest_formatter,
            digest_delivery_system,
        ),
        time_of_day="07:00",
    )
    scheduler.start()
    uvicorn.run(endpoints.app, host="0.0.0.0", port=8000)
