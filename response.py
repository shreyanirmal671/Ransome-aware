# ─────────────────────────────────────────────
#  Module 6 — Response & Containment Module
# ─────────────────────────────────────────────

import os
import subprocess
import stat
import threading
from logger_module import log_action, logger

# Global flag — set to True to pause analysis
monitoring_paused = threading.Event()

# Track which files/dirs we've restricted
restricted_paths = []

def pause_monitoring():
    """Signal the monitor to pause processing new events."""
    monitoring_paused.set()
    log_action("PAUSE_MONITORING", "Monitoring paused due to detection")
    print("[RESPONSE] ⏸  Monitoring paused.")

def resume_monitoring():
    """Resume monitoring after a pause."""
    monitoring_paused.clear()
    log_action("RESUME_MONITORING", "Monitoring resumed by user")
    print("[RESPONSE] ▶  Monitoring resumed.")

def is_paused():
    return monitoring_paused.is_set()

def restrict_write_access(path):
    """
    Remove write permissions from a file or directory.
    Works on Windows and Linux.
    """
    try:
        if os.path.exists(path):
            os.chmod(path, stat.S_IREAD | stat.S_IRGRP | stat.S_IROTH)
            restricted_paths.append(path)
            log_action("RESTRICT_WRITE", path)
            print(f"[RESPONSE] 🔒 Write access restricted: {path}")
        else:
            print(f"[RESPONSE] Path not found: {path}")
    except Exception as e:
        logger.error(f"Could not restrict {path}: {e}")

def restore_write_access(path):
    """Restore write permissions (undo restriction)."""
    try:
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
        if path in restricted_paths:
            restricted_paths.remove(path)
        log_action("RESTORE_WRITE", path)
        print(f"[RESPONSE] 🔓 Write access restored: {path}")
    except Exception as e:
        logger.error(f"Could not restore {path}: {e}")

def kill_process_by_pid(pid):
    """Forcefully terminate a process by PID."""
    try:
        if os.name == "nt":  # Windows
            subprocess.run(["taskkill", "/PID", str(pid), "/F"],
                           capture_output=True)
        else:                 # Linux/Mac
            os.kill(pid, 9)
        log_action("KILL_PROCESS", f"PID={pid}")
        print(f"[RESPONSE] 💀 Process {pid} terminated.")
    except Exception as e:
        logger.error(f"Could not kill PID {pid}: {e}")

def kill_process_by_name(name):
    """Terminate a process by name (Windows)."""
    try:
        subprocess.run(["taskkill", "/IM", name, "/F"],
                       capture_output=True)
        log_action("KILL_PROCESS_NAME", f"Name={name}")
        print(f"[RESPONSE] 💀 Process '{name}' terminated.")
    except Exception as e:
        logger.error(f"Could not kill process {name}: {e}")

def full_containment(observer=None):
    """
    Execute full containment:
    1. Pause monitoring
    2. Log the containment action
    """
    print("\n[RESPONSE] 🚨 INITIATING FULL CONTAINMENT...")
    pause_monitoring()
    if observer:
        try:
            observer.stop()
            log_action("STOP_OBSERVER", "File system observer stopped")
            print("[RESPONSE] Observer stopped.")
        except Exception as e:
            logger.error(f"Could not stop observer: {e}")
    log_action("FULL_CONTAINMENT", "All containment actions executed")
    print("[RESPONSE] ✅ Containment complete. Review logs for details.\n")

def get_restricted_paths():
    return restricted_paths.copy()
