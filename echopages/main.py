import logging
from datetime import datetime

import uvicorn

import echopages.bootstrap as bootstrap
import echopages.config
from echopages.api import endpoints
from echopages.application import services
from echopages.infrastructure.delivery import schedulers

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uow = bootstrap.get_unit_of_work()
    digest_formatter = bootstrap.get_digest_formatter()
    digest_delivery_system = bootstrap.get_digest_delivery_system()
    content_sampler = bootstrap.get_sampler()
    config = echopages.config.get_config()
    # Configure Scheduler
    logger.info(
        f"Starting Scheduler at {datetime.now()}, {config.daily_time_of_digest}"
    )
    scheduler = schedulers.SimpleScheduler(
        lambda: services.delivery_service(
            uow,
            content_sampler,
            config.number_of_units_per_digest,
            digest_formatter,
            digest_delivery_system,
        ),
        time_of_day=config.daily_time_of_digest,
    )
    scheduler.start()
    uvicorn.run(endpoints.app, host="0.0.0.0", port=8000)
