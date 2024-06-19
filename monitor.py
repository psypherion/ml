import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ProjectHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            os.chdir(event.src_path)
            subprocess.run(['git', 'init'])
            print(f"Initialized a new git repository in {event.src_path}")
            os.chdir('..')

def monitor_projects(base_path):
    if not os.path.exists(base_path):
        raise FileNotFoundError(f"The path {base_path} does not exist.")
    event_handler = ProjectHandler()
    observer = Observer()
    observer.schedule(event_handler, base_path, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_projects('/path/to/existing_directory')  # Replace with the correct path
