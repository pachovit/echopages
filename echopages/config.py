import os

DB_URI = os.environ.get("DB_URI", "echopages.db")
DELIVERY_SYSTEM = os.environ.get("DELIVERY_SYSTEM", "DiskDigestDeliverySystem")
DISK_DELIVERY_SYSTEM_DIRECTORY = os.environ.get(
    "DISK_DELIVERY_SYSTEM_DIRECTORY", "./digests"
)
NUMBER_OF_UNITS_PER_DIGEST = 1
