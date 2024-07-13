from threading import Thread
from typing import Callable, Optional

import schedule

from echopages.domain import model


class SimpleScheduler(model.Scheduler):
    def __init__(self, function: Callable[[], None], time_of_day: Optional[str] = None):
        super().__init__(function, time_of_day)
        self.continue_running = False

    def configure_schedule(self, time_of_day: str) -> None:
        self.time_of_day = time_of_day
        schedule.clear()
        schedule.every().day.at(time_of_day, "Europe/Berlin").do(self.function)

    def start(self):
        self.continue_running = True
        thread = Thread(target=self._start)
        thread.daemon = True
        thread.start()

    def _start(self):
        while self.continue_running:
            schedule.run_pending()

    def stop(self):
        self.continue_running = False
