import os

DB_URI = os.environ.get("DB_URI", "data/echopages.db")
DELIVERY_SYSTEM = os.environ.get("DELIVERY_SYSTEM", "PostmarkDigestDeliverySystem")
DISK_DELIVERY_SYSTEM_DIRECTORY = os.environ.get(
    "DISK_DELIVERY_SYSTEM_DIRECTORY", "data/digests"
)
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "hello@echopages.com")
NUMBER_OF_UNITS_PER_DIGEST = int(os.environ.get("NUMBER_OF_UNITS_PER_DIGEST", 1))
DAILY_TIME_OF_DIGEST = os.environ.get("DAILY_TIME_OF_DIGEST", "07:00")
