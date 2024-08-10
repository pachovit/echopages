import time
from datetime import datetime, timedelta

from time_machine import travel
from zoneinfo import ZoneInfo

from echopages.backend.infrastructure.delivery import schedulers


class DummyClass:
    value = 0


def dummy_function() -> None:
    DummyClass.value = 1


def test_scheduler_works_on_time() -> None:
    DummyClass.value = 0
    zone = ZoneInfo("Europe/Berlin")
    original_time = datetime(2020, 1, 1, 6, 59, 59, tzinfo=zone)
    with travel(original_time, tick=False) as traveller:
        # Given: A scheduler
        scheduler = schedulers.SimpleScheduler(
            dummy_function, "07:00", sleep_interval=0.05
        )
        assert DummyClass.value == 0

        # When: Schedule time arrives
        scheduler.start()
        traveller.shift(timedelta(seconds=2))
        time.sleep(0.1)
        scheduler.stop()

        # Then: Digest is sent
        assert DummyClass.value == 1


def test_scheduler_is_reconfigured() -> None:
    DummyClass.value = 0

    zone = ZoneInfo("Europe/Berlin")
    original_time = datetime(2020, 1, 1, 6, 59, 59, tzinfo=zone)
    with travel(original_time, tick=False) as traveller:
        # Given: A running scheduler
        scheduler = schedulers.SimpleScheduler(
            dummy_function, "06:00", sleep_interval=0.05
        )
        scheduler.start()
        assert DummyClass.value == 0

        # When: Schedule time arrives
        scheduler.configure_schedule("07:00")
        traveller.shift(timedelta(seconds=2))
        time.sleep(0.1)
        scheduler.stop()

        # Then: Digest is sent
        assert DummyClass.value == 1
