import logging
from datetime import datetime

import uvicorn

import echopages.bootstrap as bootstrap
import echopages.config
from echopages.api import endpoints
from echopages.application import services
from echopages.infrastructure.delivery import schedulers

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure the logger to log info messages."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def start_scheduler(config: echopages.config.Config) -> None:
    """Start the scheduler that will send daily digest emails."""
    uow = bootstrap.get_unit_of_work()
    digest_formatter = bootstrap.get_digest_formatter()
    digest_delivery_system = bootstrap.get_digest_delivery_system()
    content_sampler = bootstrap.get_sampler()
    logger.info(
        f"Starting Scheduler at {datetime.now()}, " f"{config.daily_time_of_digest}"
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


def main() -> None:
    """Main function that configures the logging and starts the API server."""
    configure_logging()
    config = echopages.config.get_config()
    start_scheduler(config)
    uvicorn.run(endpoints.app, host=config.api_host, port=config.api_port)


if __name__ == "__main__":
    main()
