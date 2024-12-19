import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def __init__(self, log_file):
        self.log_file = log_file
    
    def on_modified(self, event):
        self.log_event("modified", event)

    def on_created(self, event):
        self.log_event("created", event)
    
    def on_deleted(self, event):
        self.log_event("deleted", event)

    def log_event(self, event_type, event):
        data = {
            "event_type": event_type,
            "file": event.src_path,
            "is_directory": event.is_directory,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')  # Corrected line
        }
        with open(self.log_file, "a") as log:
            log.write(json.dumps(data) + "\n")  # Use json.dumps to serialize data to JSON format
            

if __name__ == "__main__":
    path_to_watch = "/home/emirhan/bsm/test"
    log_file_path = "/home/emirhan/bsm/logs/changes.json"
    
    event_handler = ChangeHandler(log_file_path)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=True)

    print(f"Watching for changes in {path_to_watch}")
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
