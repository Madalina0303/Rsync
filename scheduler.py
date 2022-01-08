import threading
from threading import Thread
import schedule
import time


class schedule_sync:
    def __init__(self):
        # print("NIVLUCFG;")
        self.scheduler = schedule.Scheduler()

    def schedulerDaemon(self):
        # print("SUNT BINEEEEEEEEEEEEEEE")
        while True:
            self.scheduler.run_pending()
            # print("CONTEZ PENTRU MINE")
            time.sleep(1)
            # except KeyboardInterrupt:
            #     break

    def ESB(self):
        print("Ma jur ca voi fi bine")

    def start(self, fct1):
        # print("Ok", type(fct1))
        self.scheduler.every(30).seconds.do(fct1)
        # print("Ok1")
        # self.scheduler.every(5).seconds.do(fct2)

        print("Ok2")
        threading.Thread(target=self.schedulerDaemon(), daemon=True).start()
        # while(True):
        #     self.scheduler.run_pending()
        #     time.sleep(1)
