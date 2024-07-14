from threading import Thread
from time import sleep
from typing import Callable, Optional

import schedule

from echopages.domain import model


class SimpleScheduler(model.Scheduler):
    def __init__(
        self,
        function: Callable[[], None],
        time_of_day: Optional[str] = None,
        time_zone: str = "Europe/Berlin",
        sleep_interval: float = 1.0,
    ) -> None:
        if time_of_day is None:
            time_of_day = "00:00"
        self.function = function
        self.time_zone = time_zone
        self.sleep_interval = sleep_interval
        self.configure_schedule(time_of_day)

    def configure_schedule(self, time_of_day: str) -> None:
        self.time_of_day = time_of_day
        schedule.clear()
        schedule.every().day.at(time_of_day, self.time_zone).do(self.function)

    def start(self) -> None:
        self.continue_running = True
        thread = Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def _run(self) -> None:
        while self.continue_running:
            schedule.run_pending()
            sleep(self.sleep_interval)

    def stop(self) -> None:
        self.continue_running = False
