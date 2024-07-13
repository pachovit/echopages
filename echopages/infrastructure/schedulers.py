from datetime import datetime
from threading import Thread
from typing import Callable, Optional

from echopages.domain import model


class SimpleScheduler(model.Scheduler):
    def __init__(
        self, function: Callable[[], None], schedule: Optional[model.Schedule] = None
    ):
        super().__init__(function, schedule)
        self.function_called = False

    def start(self):
        thread = Thread(target=self._start)
        thread.daemon = True
        thread.start()

    def _start(self):
        while not self.function_called:
            now = datetime.now()
            # Check if the current time is within a minute range of the scheduled time
            if (
                now.hour == self.schedule.time_of_day.hour
                and now.minute == self.schedule.time_of_day.minute
            ):
                self.function()
                self.function_called = True
                break
