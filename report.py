# ─────────────────────────────────────────────
#  Module 8 — Audit & Incident Report Generator
# ─────────────────────────────────────────────

import os
import time
from datetime import datetime
from logger_module import get_log_filename, logger

REPORTS_DIR = "reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

# In-memory incident record (populated by other modules)
incident_record = {
    "start_time":       None,
    "detection_time":   None,
    "end_time":         None,
    "affected_files":   [],
    "alerts":           [],
    "classifications":  [],
    "actions_taken":    [],
    "total_events":     0,
}

def record_start():
    incident_record["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def record_detection(family, confidence, risk):
    incident_record["detection_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    incident_record["classifications"].append({
        "family":     family,
        "confidence": confidence,
        "risk":       risk,
        "time":       datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def record_alert(level, reason, details=""):
    incident_record["alerts"].append({
        "level":   level,
        "reason":  reason,
        "details": details,
        "time":    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def record_affected_file(path):
    if path not in incident_record["affected_files"]:
        incident_record["affected_files"].append(path)

def record_action(action, detail=""):
    incident_record["actions_taken"].append({
        "action": action,
        "detail": detail,
        "time":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

def set_total_events(count):
    incident_record["total_events"] = count

def generate_report():
    """Generate a human-readable incident report and save to file."""
    incident_record["end_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(REPORTS_DIR, f"incident_report_{timestamp}.txt")

    border   = "=" * 65
    divider  = "-" * 65

    lines = [
        border,
        "       RANSOMWATCH — INCIDENT REPORT",
        border,
        f"  Report Generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"  Log File         : {get_log_filename()}",
        border,
        "",
        "SECTION 1 — TIMELINE",
        divider,
        f"  Monitoring Started : {incident_record['start_time'] or 'N/A'}",
        f"  Detection Time     : {incident_record['detection_time'] or 'No detection'}",
        f"  Monitoring Ended   : {incident_record['end_time']}",
        f"  Total File Events  : {incident_record['total_events']}",
        "",
        "SECTION 2 — WHAT HAPPENED",
        divider,
    ]

    if incident_record["alerts"]:
        for i, alert in enumerate(incident_record["alerts"], 1):
            lines.append(f"  [{i}] [{alert['time']}] [{alert['level']}] {alert['reason']}")
            if alert["details"]:
                lines.append(f"      Details: {alert['details']}")
    else:
        lines.append("  No alerts triggered during this session.")

    lines += [
        "",
        "SECTION 3 — RANSOMWARE FAMILY CLASSIFICATION",
        divider,
    ]

    if incident_record["classifications"]:
        for c in incident_record["classifications"]:
            lines.append(f"  Family     : {c['family']}")
            lines.append(f"  Confidence : {c['confidence']}%")
            lines.append(f"  Risk Level : {c['risk']}")
            lines.append(f"  Detected   : {c['time']}")
            lines.append("")
    else:
        lines.append("  No ransomware family classified.")

    lines += [
        "",
        "SECTION 4 — AFFECTED FILES",
        divider,
    ]

    if incident_record["affected_files"]:
        for f in incident_record["affected_files"][:50]:   # cap at 50
            lines.append(f"  {f}")
        if len(incident_record["affected_files"]) > 50:
            lines.append(f"  ... and {len(incident_record['affected_files']) - 50} more (see log)")
    else:
        lines.append("  No specific files recorded.")

    lines += [
        "",
        "SECTION 5 — ACTIONS TAKEN BY SYSTEM",
        divider,
    ]

    if incident_record["actions_taken"]:
        for a in incident_record["actions_taken"]:
            lines.append(f"  [{a['time']}] {a['action']}")
            if a["detail"]:
                lines.append(f"      Detail: {a['detail']}")
    else:
        lines.append("  No automated actions were taken.")

    lines += [
        "",
        "SECTION 6 — RECOMMENDATIONS",
        divider,
        "  1. Isolate the affected machine from the network immediately.",
        "  2. Do NOT pay ransom — consult cybersecurity professionals.",
        "  3. Restore files from clean offline backups.",
        "  4. Report to: https://www.nomoreransom.org",
        "  5. Preserve this report and log file as evidence.",
        "",
        border,
        "  END OF REPORT — RansomWatch v1.0",
        border,
    ]

    report_text = "\n".join(lines)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)

    logger.info(f"Incident report saved: {report_file}")
    print(f"\n[REPORT] ✅ Incident report saved: {report_file}\n")
    print(report_text)

    return report_file

def get_incident_record():
    return incident_record.copy()
