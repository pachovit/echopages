import logging
from datetime import datetime

import uvicorn

import echopages.backend.bootstrap as bootstrap
import echopages.backend.config
from echopages.setup_app import create_app

logger = logging.getLogger(__name__)


def configure_logging() -> None:
    """Configure the logger to log info messages."""
    log_level = logging.getLevelName(echopages.backend.config.get_config().log_level)
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def start_scheduler() -> None:
    """Start the scheduler that will send daily digest emails."""
    config = echopages.backend.config.get_config()
    logger.info(
        f"Starting Scheduler at {datetime.now()}, " f"{config.daily_time_of_digest}"
    )
    scheduler = bootstrap.get_scheduler()
    scheduler.start()


def main() -> None:
    """Main function that configures the logging and starts the API server."""
    configure_logging()
    config = echopages.backend.config.get_config()
    start_scheduler()
    uvicorn.run(app, host=config.api_host, port=config.api_port)


app = create_app()

if __name__ == "__main__":
    main()
