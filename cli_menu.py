2# ─────────────────────────────────────────────
#  Module 9 — User Control Module (CLI Menu)
#  This is the MAIN entry point — run this
# ─────────────────────────────────────────────

import os
import time
import webbrowser

from dashboard_server import (start_dashboard_thread, push_alert,
                               push_detection, push_file_event,
                               update_status, set_start_time)
from notifier   import send_alert_popup, send_detection_popup
from alerting   import send_alert, send_detection_banner, send_info, send_warning
from analyzer   import register_alert_callback, get_recent_summary
from classifier import classify
from report     import (record_start, record_alert, record_detection,
                        record_action, generate_report, get_incident_record)
from response   import pause_monitoring, resume_monitoring, full_containment
from logger_module import get_log_filename, logger

_seen_extensions = set()
_detection_done  = False

def _on_alert(level, reason, details=""):
    global _detection_done
    send_alert(level, reason, details)
    record_alert(level, reason, details)
    push_alert(level, reason, details)
    if level in ("HIGH", "CRITICAL"):
        send_alert_popup(level, reason, details)
    for ext in [".enc",".locked",".crypt",".wncry",".lockbit",
                ".ryuk",".maze",".conti",".darkside",".hive",".clop"]:
        if ext in details or ext in reason:
            _seen_extensions.add(ext)
    if level in ("HIGH", "CRITICAL") and not _detection_done:
        summary = get_recent_summary()
        results = classify(
            detected_extensions=list(_seen_extensions),
            rename_count=summary["renamed"],
            mod_count=summary["modified"]
        )
        if results:
            top = results[0]
            send_detection_banner(top["family"], top["confidence"], top["risk"])
            record_detection(top["family"], top["confidence"], top["risk"])
            push_detection(top["family"], top["confidence"], top["risk"], top.get("description",""))
            send_detection_popup(top["family"], top["confidence"], top["risk"])
            update_status("ALERT")
            _detection_done = True
            if top["risk"] == "CRITICAL":
                send_warning("CRITICAL risk - initiating containment!")
                full_containment()
                record_action("FULL_CONTAINMENT", f"Triggered by {top['family']}")
                update_status("CONTAINED")

register_alert_callback(_on_alert)

import monitor as _mon_module
_orig = _mon_module.WatcherHandler._handle
def _patched(self, event_type, path, dest=None):
    push_file_event(event_type, path)
    _orig(self, event_type, path, dest)
_mon_module.WatcherHandler._handle = _patched

COLORS = {
    "GREEN": "\033[92m", "CYAN": "\033[96m",
    "YELLOW": "\033[93m", "RED": "\033[91m",
    "BOLD": "\033[1m", "RESET": "\033[0m",
}

def _banner():
    b = COLORS["CYAN"] + COLORS["BOLD"]
    r = COLORS["RESET"]
    print(f"""\n{b}
  ==========================================
       RANSOMWATCH v1.0
       Real-Time Ransomware Detection System
  ==========================================
  Dashboard : http://localhost:5000
{r}""")

def _menu():
    g = COLORS["GREEN"] + COLORS["BOLD"]
    r = COLORS["RESET"]
    print(f"""{g}
  [1]  Start Monitoring  (30 seconds)
  [2]  Start Monitoring  (custom duration)
  [3]  Run Safe Simulation (test mode)
  [4]  View Latest Log File
  [5]  Generate Incident Report
  [6]  View Incident Summary
  [7]  Open Dashboard in Browser
  [0]  Exit
{r}""")

def _view_log():
    log_file = get_log_filename()
    if not os.path.exists(log_file):
        print("[LOG] No log file found yet.")
        return
    print(f"\n[LOG] {log_file}\n" + "-"*60)
    with open(log_file, "r") as f:
        for line in f.readlines()[-40:]:
            print(line, end="")
    print("\n" + "-"*60)

def _view_summary():
    record = get_incident_record()
    print("\n-- Incident Summary " + "-"*40)
    print(f"  Started   : {record['start_time'] or 'Not started'}")
    print(f"  Detection : {record['detection_time'] or 'No detection'}")
    print(f"  Events    : {record['total_events']}")
    print(f"  Alerts    : {len(record['alerts'])}")
    if record["classifications"]:
        top = record["classifications"][0]
        print(f"  Top Match : {top['family']} ({top['confidence']}% / {top['risk']})")
    print("-"*60 + "\n")

def main():
    os.system("")
    print("[*] Starting dashboard server...")
    start_dashboard_thread()
    _banner()
    record_start()
    webbrowser.open("http://localhost:5000")
    print("[*] Dashboard opened at http://localhost:5000\n")

    while True:
        _menu()
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            send_info("Starting monitoring for 30 seconds...")
            update_status("MONITORING")
            set_start_time()
            from monitor import start_monitoring
            start_monitoring(duration=30)
            update_status("IDLE")

        elif choice == "2":
            try:
                secs = int(input("  Enter duration in seconds: ").strip())
                update_status("MONITORING")
                set_start_time()
                from monitor import start_monitoring
                start_monitoring(duration=secs)
                update_status("IDLE")
            except ValueError:
                send_warning("Invalid input.")

        elif choice == "3":
            print(f"\n{COLORS['YELLOW']}[SIM] Safe simulation - no real malware{COLORS['RESET']}")
            print("  [a] Full encryption pattern")
            print("  [b] Mass rename only")
            print("  [c] Mass modification only")
            print("  [d] Cleanup simulation files")
            sim = input("  Enter choice: ").strip().lower()
            from simulator import (simulate_encryption_pattern, simulate_mass_rename,
                                   simulate_mass_modification, cleanup_simulation,
                                   create_dummy_files)
            if sim == "a":
                import threading
                from monitor import start_monitoring
                update_status("MONITORING")
                set_start_time()
                t = threading.Thread(target=start_monitoring, args=(60,), daemon=True)
                t.start()
                time.sleep(2)
                simulate_encryption_pattern()
                t.join()
                update_status("IDLE")
            elif sim == "b":
                create_dummy_files(); simulate_mass_rename()
            elif sim == "c":
                create_dummy_files(); simulate_mass_modification()
            elif sim == "d":
                cleanup_simulation()
            else:
                send_warning("Invalid choice.")

        elif choice == "4":
            _view_log()
        elif choice == "5":
            generate_report()
            push_alert("LOW", "Incident report generated", "Check dashboard report panel")
        elif choice == "6":
            _view_summary()
        elif choice == "7":
            webbrowser.open("http://localhost:5000")
            print("[*] Opened http://localhost:5000")
        elif choice == "0":
            print("\n[*] Exiting. Goodbye!\n")
            break
        else:
            send_warning("Invalid choice.")

if __name__ == "__main__":
    main()
