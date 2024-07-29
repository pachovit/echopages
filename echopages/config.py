from datetime import datetime

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Database URI
    db_uri: str = "data/echopages.db"

    # Delivery system to use
    delivery_system: str = "PostmarkDigestDeliverySystem"

    # Directory for digests if using the DiskDigestDeliverySystem
    disk_delivery_system_directory: str = "data/digests"

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
    if config is None:
        config = Config()
    return config
