import threading
from threading import Thread
import schedule
import time


class schedule_sync:
    def __init__(self):
        self.scheduler = schedule.Scheduler()
        threading.Thread(target=self.schedulerDaemon(), daemon=True).start()

    def schedulerDaemon(self):
        while True:
            try:
                self.scheduler.run_pending()
                time.wait(60)
            except KeyboardInterrupt:
                break
