import logging
from threading import Thread
from time import sleep
from typing import Any, Callable, Optional

import schedule

from echopages.backend.domain import model

logger = logging.getLogger(__name__)


class SimpleScheduler(model.Scheduler):
    """A simple scheduler based on the `schedule` library."""

    def __init__(
        self,
        function: Callable[[], Any],
        time_of_day: Optional[str] = None,
        time_zone: str = "Europe/Berlin",
        sleep_interval: float = 1.0,
    ) -> None:
        if time_of_day is None:
            time_of_day = "00:00"
        self.function = function
        self.time_zone = time_zone
        self.sleep_interval = sleep_interval
        self.continue_running = False
        self.configure_schedule(time_of_day)

    def configure_schedule(self, time_of_day: str) -> None:
        logger.info(f"Configuring schedule for {time_of_day}")
        self.time_of_day = time_of_day

        was_running = self.continue_running
        if was_running:
            self.stop()

        schedule.clear()
        schedule.every().day.at(time_of_day, self.time_zone).do(self.function)

        if was_running:
            self.start()

    def start(self) -> None:
        self.continue_running = True
        thread = Thread(target=self._run)
        thread.daemon = True
        thread.start()

    def _run(self) -> None:
        """Run the scheduled function at the configured time interval."""
        while self.continue_running:
            schedule.run_pending()
            sleep(self.sleep_interval)

    def stop(self) -> None:
        self.continue_running = False
