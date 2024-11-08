from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.combining import AndTrigger

from datetime import datetime
import time


class Trigger:
    """
    A class to represent a scheduling trigger.
    See https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html for
    the complete format

    Attributes:
    -----------
    year : str, optional
        The year when the trigger should activate (default is "*").
    month : str, optional
        The month when the trigger should activate (default is "*").
    day_of_week : str, optional
        The day of the week when the trigger should activate (default is "*").
    hour : str, optional
        The hour when the trigger should activate (default is "*").
    minute : str, optional
        The minute when the trigger should activate (default is "*").
    second : str, optional
        The second when the trigger should activate (default is "00/30").
    Methods:
    --------
    toCron(timezone):
        Converts the trigger to a CronTrigger object with the specified timezone.
    """

    def __init__(
        self, year="*", month="*", day_of_week="*", hour="*", minute="*", second="00/30"
    ):
        self.year = year
        self.month = month
        self.day_of_week = day_of_week
        self.hour = hour
        self.minute = minute
        self.second = second

    def toCron(self, timezone):
        return CronTrigger(
            year=self.year,
            month=self.month,
            day_of_week=self.day_of_week,
            hour=self.hour,
            minute=self.minute,
            second=self.second,
            timezone=timezone,
        )


def execute_task(scheduler_instance, task_function):
    if (
        not scheduler_instance.success
        and scheduler_instance.attempts < scheduler_instance.max_attempts
    ):
        scheduler_instance.attempts += 1
        print("Executing task - attempt: ", scheduler_instance.attempts)
        scheduler_instance.success = task_function()
    else:
        print("Execution complete, stop scheduler!")


class Scheduler:
    def __init__(
        self, trigger, task_function, timezone="Europe/Amsterdam", max_attempts=10
    ):
        self.task_function = task_function
        self.trigger = trigger.toCron(timezone)

        self.scheduler = BackgroundScheduler(timezone=timezone)
        self.scheduler.start()

        job_fun = lambda: execute_task(self, task_function)
        self.scheduler.add_job(job_fun, trigger=self.trigger)

        self.success = False
        self.max_attempts = max_attempts
        self.attempts = 0

    def run(self):
        print("Scheduler started")
        print(
            "First execution: ", self.trigger.get_next_fire_time(None, datetime.now())
        )
        try:
            while not self.success:
                time.sleep(5)
        except (KeyboardInterrupt, SystemExit):
            self.scheduler.shutdown()

        print(
            "Scheduler stopped. Exiting program. Were we successful: ",
            self.success,
        )


if __name__ == "__main__":

    def subscribe():
        print("Subscribing...")
        return False

    print("Creating trigger...")
    trigger = Trigger()
    print("Creating scheduler...")
    scheduler = Scheduler(trigger, subscribe)
    print("Starting scheduler...")
    scheduler.run()

    print("...")
