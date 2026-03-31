# ─────────────────────────────────────────────
#  Module 2 — Behaviour Analysis Engine
# ─────────────────────────────────────────────

import time
import os
from collections import deque, defaultdict
from rules import RULES, is_excluded, is_suspicious_extension
from logger_module import log_alert, log_event

# Shared state — stores recent events in a sliding time window
recent_events = deque()          # (timestamp, event_type, path)
extension_changes = defaultdict(set)   # path -> set of extensions seen
alert_callbacks = []             # functions to call when alert fires

def register_alert_callback(fn):
    """Register a function to be called when an alert is triggered."""
    alert_callbacks.append(fn)

def _fire_alert(level, reason, details=""):
    log_alert(level, f"{reason} | {details}")
    for cb in alert_callbacks:
        cb(level, reason, details)

def _clean_old_events():
    """Remove events older than the time window."""
    cutoff = time.time() - RULES["time_window_seconds"]
    while recent_events and recent_events[0][0] < cutoff:
        recent_events.popleft()

def _count_events(event_type):
    return sum(1 for _, etype, _ in recent_events if etype == event_type)

def analyze_event(event_type, path, dest_path=None):
    """
    Called for every file system event.
    event_type: 'created' | 'modified' | 'deleted' | 'renamed'
    """
    if is_excluded(path):
        return

    now = time.time()
    recent_events.append((now, event_type, path))
    _clean_old_events()

    log_event(event_type.upper(), path, f"dest={dest_path}" if dest_path else "")

    # ── Rule 1: Suspicious extension detected ──────────────────────
    if is_suspicious_extension(path):
        _fire_alert("HIGH", "Suspicious ransomware extension detected", path)

    if dest_path and is_suspicious_extension(dest_path):
        _fire_alert("HIGH", "File renamed to suspicious ransomware extension", f"{path} -> {dest_path}")

    # ── Rule 2: Mass modifications in short window ─────────────────
    mod_count = _count_events("modified")
    if mod_count >= RULES["max_modifications_per_window"]:
        _fire_alert("HIGH",
                    f"Mass file modification detected",
                    f"{mod_count} files modified in {RULES['time_window_seconds']}s")

    # ── Rule 3: Mass renames in short window ──────────────────────
    rename_count = _count_events("renamed")
    if rename_count >= RULES["max_renames_per_window"]:
        _fire_alert("HIGH",
                    f"Mass file renaming detected",
                    f"{rename_count} renames in {RULES['time_window_seconds']}s")

    # ── Rule 4: Mass creations in short window ────────────────────
    create_count = _count_events("created")
    if create_count >= RULES["max_creations_per_window"]:
        _fire_alert("MEDIUM",
                    f"Mass file creation detected",
                    f"{create_count} files created in {RULES['time_window_seconds']}s")

    # ── Rule 5: Extension diversity change (encryption pattern) ───
    if dest_path:
        _, new_ext = os.path.splitext(dest_path)
        _, old_ext = os.path.splitext(path)
        base = os.path.dirname(path)
        if new_ext and new_ext != old_ext:
            extension_changes[base].add(new_ext)
            if len(extension_changes[base]) >= RULES["max_extension_changes"]:
                _fire_alert("HIGH",
                            "Multiple extension changes in same directory (encryption pattern)",
                            f"Directory: {base} | Extensions: {extension_changes[base]}")

    # ── Rule 6: Combined suspicious activity (MEDIUM early warning) ─
    total = len(recent_events)
    if total >= 10 and rename_count + mod_count >= total * 0.8:
        _fire_alert("MEDIUM",
                    "High ratio of modifications+renames (early ransomware pattern)",
                    f"{total} events in {RULES['time_window_seconds']}s")

def get_recent_summary():
    _clean_old_events()
    return {
        "total":    len(recent_events),
        "created":  _count_events("created"),
        "modified": _count_events("modified"),
        "deleted":  _count_events("deleted"),
        "renamed":  _count_events("renamed"),
    }
