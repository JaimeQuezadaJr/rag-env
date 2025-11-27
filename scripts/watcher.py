# scripts/watcher.py

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from ingest import run_ingest   # works because ingest is in same folder

# Calculate project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Full absolute path to pdf_inputs folder
WATCH_PATH = os.path.join(ROOT_DIR, "pdf_inputs")

class PDFWatcher(FileSystemEventHandler):
    def on_any_event(self, event):
        # Only process PDF files and relevant events (created, deleted, modified, moved)
        if not event.is_directory and event.src_path.lower().endswith('.pdf'):
            print(f"\n📢 Change detected: {event.event_type} — {event.src_path}")
            run_ingest()

def start_watcher():
    print(f"👀 Watching: {WATCH_PATH}")
    event_handler = PDFWatcher()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_PATH, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Watcher stopped.")
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_watcher()
