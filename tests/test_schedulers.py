import time
from datetime import datetime, timedelta

import freezegun

from echopages.infrastructure import schedulers


def test_scheduler_works_on_time():
    class DummyClass:
        value = 0

    def dummy_function():
        DummyClass.value = 1

    second_before_sending = datetime(2020, 1, 1, 6, 59, 59)
    with freezegun.freeze_time(second_before_sending) as frozen_date:
        # Given: A scheduler and some digests
        scheduler = schedulers.Scheduler(dummy_function, "07:00")
        assert DummyClass.value == 0

        # When: Schedule time arrives
        scheduler.start()
        frozen_date.move_to(second_before_sending + timedelta(seconds=2))

        # Then: Digest is sent
        time.sleep(0.1)
        assert DummyClass.value == 1


def test_user_can_configure_schedule():
    # TODO: This is being coupled to hour and minute in date time format,
    # which means assuming daily schedule.

    # Given: Some schedule
    scheduler = schedulers.Scheduler(lambda: None, "00:00")
    assert scheduler.get_schedule().hour == 0
    assert scheduler.get_schedule().minute == 0

    # When: User configures schedule
    scheduler.configure_schedule("07:00")

    # Then: Schedule is changed
    assert scheduler.get_schedule().hour == 7
    assert scheduler.get_schedule().minute == 0
