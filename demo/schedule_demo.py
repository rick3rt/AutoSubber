from autosubber.scheduler import Scheduler, Trigger
from demo import subscribe

if __name__ == "__main__":
    # setup trigger, day/time/seconds...
    trigger = Trigger(second="00/15")
    scheduler = Scheduler(trigger, subscribe)
    scheduler.run()

    print(
        "Scheduler stopped. Exiting program. Were we successful: ",
        scheduler.success,
    )
