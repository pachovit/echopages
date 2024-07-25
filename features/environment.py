import os
import shutil

from behave.runner import Context
from dotenv import load_dotenv

import echopages.config


def before_all(context: Context) -> None:
    load_dotenv(dotenv_path="test.env", override=True)
    echopages.config.DB_URI = os.getenv("DB_URI", "")
    echopages.config.DELIVERY_SYSTEM = os.getenv("DELIVERY_SYSTEM", "")
    echopages.config.DISK_DELIVERY_SYSTEM_DIRECTORY = os.getenv(
        "DISK_DELIVERY_SYSTEM_DIRECTORY", ""
    )


def after_all(context: Context) -> None:
    if os.path.exists(echopages.config.DISK_DELIVERY_SYSTEM_DIRECTORY):
        shutil.rmtree(echopages.config.DISK_DELIVERY_SYSTEM_DIRECTORY)
    if os.path.exists(echopages.config.DB_URI):
        shutil.rmtree(echopages.config.DB_URI)
