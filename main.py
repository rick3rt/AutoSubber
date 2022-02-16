from subprocess import call
from datetime import datetime
import time
import os
# from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.combining import AndTrigger

from subscriber import subscribe

SUCCESS = 0  # global variable to keep track of success
NUM_ATTEMPTS = 0
MAX_ATTEMPTS = 5


def job():
    global SUCCESS, NUM_ATTEMPTS
    print("In job, currtime: ", datetime.now())
    NUM_ATTEMPTS += 1
    if not SUCCESS and NUM_ATTEMPTS <= MAX_ATTEMPTS:
        SUCCESS = subscribe()
        print("Num attempts: {}".format(
            NUM_ATTEMPTS))
    else:
        print('waiting for closing')


if __name__ == '__main__':
    print("Started on {}, currtime: {}".format(
        datetime.today().strftime('%A'), datetime.now()))

    scheduler = BackgroundScheduler(timezone="Europe/Amsterdam")

    trigger = CronTrigger(year="*",
                          month="*",
                          day_of_week="sun",
                          hour="7",
                          minute="30-35",
                          second="00/30",
                          timezone="Europe/Amsterdam")
    print("First fire: ", trigger.get_next_fire_time(None, datetime.now()))

    scheduler.start()
    scheduler.add_job(job, trigger=trigger)
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(5)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
