import logging

import uvicorn

import echopages.config
from echopages.application import services
from echopages.infrastructure import samplers, schedulers, sql, web
from echopages.infrastructure.fakes import (
    FakeDigestDeliverySystem,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

if __name__ == "__main__":
    unit_of_work = sql.get_unit_of_work(echopages.config.DB_URI)
    delivery_system = FakeDigestDeliverySystem()
    content_sampler = samplers.SimpleContentSampler()

    # Configure Scheduler
    scheduler = schedulers.SimpleScheduler(
        lambda: services.delivery_service(
            unit_of_work,
            content_sampler,
            echopages.config.NUMBER_OF_UNITS_PER_DIGEST,
            delivery_system,
        ),
        time_of_day="07:00",
    )
    scheduler.start()
    uvicorn.run(web.app, host="0.0.0.0", port=8000)
