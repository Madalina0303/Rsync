import threading
import schedule
import time


class schedule_sync:
    def __init__(self):
        """
        Constructorul clasei schedule_sync
        :returns: None

        """
        self.scheduler = schedule.Scheduler()

    def schedulerDaemon(self):
        """
        Daemon Thread - verificarea joburilor in astpatare pentru a fi planificate
        :returns: None

        """

        while True:
            self.scheduler.run_pending()
            time.sleep(1)

    def start(self, fct1):
        """
         Programeaza un eveniment pentru a fi realizat periodic
         :param function fct1: functie care sa fie apelata din 30 in 30 de secunde
         :returns: None

        """
        self.scheduler.every(30).seconds.do(fct1)
        print("Ok2")
        threading.Thread(target=self.schedulerDaemon(), daemon=True).start()
