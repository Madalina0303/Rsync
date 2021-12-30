import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class _CustomHandler(FileSystemEventHandler):
    def on_created(self, event):
        print("HOPA TOPA PENELOPA ", event.src_path)
    def on_deleted(self, event):
        print("Se sterge ", event.src_path)
    def on_modified(self, event):
        print("Se modifica ", event.src_path)
    def on_moved(self, event):
        print("se muta ", event_handler)
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    event_handler = _CustomHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

