from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
import logging
import time
import os
from os import listdir
from os.path import  isfile, join


class _CustomHandler(FileSystemEventHandler):

    def on_created(self, event):
        print("HOPA TOPA PENELOPA ", event.src_path)

    def on_deleted(self, event):
        print("Se sterge ", event.src_path)

    def on_modified(self, event):
        print("Se modifica ", event.src_path)

    def on_moved(self, event):
        print("se muta ", event.src_path)


class LocalFolder:
    def __init__(self, path):
        self.path = path
        self.local_file_info = {}

    def startMonitoring(self):
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        event_handler = _CustomHandler()
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()

    def get_info(self):
        for f in listdir(self.path):
            full_path = join(self.path, f)
            if isfile(full_path):
                size = os.path.getsize(full_path) # size in bytes/octeti
                modTimesinceEpoc = os.path.getmtime(full_path)
                modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimesinceEpoc))
                print("Last Modified Time : ", modificationTime)
                self.local_file_info[f] = (size, modificationTime)
        return self.local_file_info
