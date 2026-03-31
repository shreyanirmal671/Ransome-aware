# ─────────────────────────────────────────────
#  Module 1 — File Monitoring (Watchdog)
# ─────────────────────────────────────────────

import string
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from analyzer   import analyze_event, get_recent_summary
from alerting   import send_alert
from response   import is_paused
from report     import record_affected_file, set_total_events

MONITOR_DURATION = 10  # seconds — change as needed

_event_count = 0

def get_all_drives():
    """Auto-detect all available drives on Windows."""
    available_drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:/"
        if os.path.exists(drive):
            available_drives.append(drive)
    return available_drives


class WatcherHandler(FileSystemEventHandler):

    def _handle(self, event_type, path, dest=None):
        global _event_count
        if is_paused():
            return
        _event_count += 1
        record_affected_file(path)
        analyze_event(event_type, path, dest_path=dest)

    def on_created(self, event):
        self._handle("created", event.src_path)

    def on_deleted(self, event):
        self._handle("deleted", event.src_path)

    def on_modified(self, event):
        self._handle("modified", event.src_path)

    def on_moved(self, event):
        self._handle("renamed", event.src_path, dest=event.dest_path)


def start_monitoring(duration=MONITOR_DURATION):
    """Start file system monitoring across all detected drives."""
    global _event_count
    _event_count = 0

    drives = get_all_drives()
    print(f"[MONITOR] Detected drives: {drives}")

    event_handler = WatcherHandler()
    observer      = Observer()

    for drive in drives:
        try:
            observer.schedule(event_handler, path=drive, recursive=True)
            print(f"[MONITOR] Monitoring: {drive}")
        except Exception as e:
            print(f"[MONITOR] Could not monitor {drive}: {e}")

    print(f"\n[MONITOR] Started. Auto-stops in {duration}s. Press Ctrl+C to stop early.\n")
    observer.start()
    start = time.time()

    try:
        while True:
            elapsed   = time.time() - start
            remaining = duration - elapsed

            if remaining <= 0:
                print(f"\n[MONITOR] {duration}s completed. Stopping...")
                break

            if int(elapsed) % 5 == 0 and int(elapsed) > 0:
                summary = get_recent_summary()
                print(f"[MONITOR] ⏱  {int(remaining)}s left | "
                      f"Events: created={summary['created']} "
                      f"modified={summary['modified']} "
                      f"renamed={summary['renamed']} "
                      f"deleted={summary['deleted']}")

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[MONITOR] Manually stopped.")

    finally:
        observer.stop()
        observer.join()
        set_total_events(_event_count)
        print(f"[MONITOR] Stopped. Total events captured: {_event_count}")

    return observer


if __name__ == "__main__":
    start_monitoring()
