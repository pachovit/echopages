from datetime import datetime
from threading import Thread
from typing import Callable


class Scheduler:
    def __init__(self, function: Callable[[], None], schedule: str):
        self.scheduled_time = datetime.strptime(schedule, "%H:%M")
        self.function = function
        self.function_called = False

    def get_schedule(self) -> str:
        return self.scheduled_time

    def configure_schedule(self, schedule: str):
        self.scheduled_time = datetime.strptime(schedule, "%H:%M")

    def start(self):
        thread = Thread(target=self._start)
        thread.daemon = True
        thread.start()

    def _start(self):
        while not self.function_called:
            now = datetime.now()
            # Check if the current time is within a minute range of the scheduled time
            if (
                now.hour == self.scheduled_time.hour
                and now.minute == self.scheduled_time.minute
            ):
                self.function()
                self.function_called = True
                break
