from datetime import datetime

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    db_uri: str = "data/echopages.db"
    delivery_system: str = "PostmarkDigestDeliverySystem"
    disk_delivery_system_directory: str = "data/digests"
    recipient_email: str = "recipient@echopages.com"
    number_of_units_per_digest: int = 1
    daily_time_of_digest: str = "07:00"

    @field_validator("daily_time_of_digest")
    def validate_time(cls, v: str) -> str:
        if v is not None:
            try:
                datetime.strptime(v, "%H:%M")
            except ValueError:
                raise ValueError("daily_time_of_digest must be in the format HH:MM")
        return v


config = None


def get_config() -> Config:
    global config
    if config is None:
        config = Config()
    return config
