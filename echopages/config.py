import json
import logging
import os
from datetime import datetime
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class Config(BaseSettings):
    log_level: str = "INFO"
    config_file_path: str = "data/config.json"

    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database URI
    db_uri: str = "data/echopages.db"

    # Delivery system to use
    delivery_system: str = "PostmarkDigestDeliverySystem"

    # Directory for digests if using the FileDigestDeliverySystem
    file_delivery_system_directory: str = "data/digests"

    # Recipient email address
    recipient_email: str = "recipient@echopages.com"

    # Number of content units per digest
    number_of_units_per_digest: int = 1

    # Time of daily digest in the format HH:MM
    daily_time_of_digest: str = "07:00"

    @field_validator("daily_time_of_digest")
    def validate_time(cls, v: str) -> str:
        """Validate the daily time of digest format."""
        if v is not None:
            try:
                datetime.strptime(v, "%H:%M")
            except ValueError:
                raise ValueError("daily_time_of_digest must be in the format HH:MM")
        return v


config = None


def get_config() -> Config:
    """Returns a singleton configuration object."""

    global config

    # If config already defined in memory, nothing else is needed
    if config is not None:
        return config

    # Load initial configuration from the environment and defaults
    config = Config()

    # If config file exists, take config from the file
    if Path(config.config_file_path).exists():
        with open(config.config_file_path, "r") as file:
            config_data = json.load(file)
            config = Config(**config_data)
    else:
        logger.warning(
            (
                f"Unexisting config file {config.config_file_path}. "
                "Configuration will be read from the environment"
                "and written to the file"
            )
        )
        write_config(config)
    return config


def write_config(cfg: Config) -> None:
    os.makedirs(os.path.dirname(cfg.config_file_path), exist_ok=True)
    with open(cfg.config_file_path, "w") as file:
        json.dump(cfg.model_dump(), file, indent=2)
