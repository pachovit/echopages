import time
from datetime import datetime, timedelta

import freezegun

from echopages.domain import model
from echopages.infrastructure import schedulers


def test_scheduler_works_on_time():
    class DummyClass:
        value = 0

    def dummy_function():
        DummyClass.value = 1

    second_before_sending = datetime(2020, 1, 1, 6, 59, 59)
    schedule = model.Schedule(
        days_of_week=[0, 1, 2, 3, 4, 5, 6], time_of_day_str="07:00"
    )
    with freezegun.freeze_time(second_before_sending) as frozen_date:
        # Given: A scheduler and some digests

        scheduler = schedulers.SimpleScheduler(dummy_function, schedule)
        assert DummyClass.value == 0

        # When: Schedule time arrives
        scheduler.start()
        frozen_date.move_to(second_before_sending + timedelta(seconds=2))

        # Then: Digest is sent
        time.sleep(0.1)
        assert DummyClass.value == 1
