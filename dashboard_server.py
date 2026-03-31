# ─────────────────────────────────────────────
#  Dashboard Server — Flask + SocketIO
#  Run this to start the web dashboard
#  Open browser at: http://localhost:5000
# ─────────────────────────────────────────────

import os
import json
import threading
import time
from datetime import datetime
from flask import Flask, render_template_string, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config["SECRET_KEY"] = "ransomwatch_secret"
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

# ── Shared state (written by monitor, read by dashboard) ──────────
dashboard_state = {
    "status":          "IDLE",       # IDLE | MONITORING | ALERT | CONTAINED
    "start_time":      None,
    "total_events":    0,
    "alerts":          [],           # list of alert dicts
    "detections":      [],           # list of classification dicts
    "recent_files":    [],           # last 50 affected files
    "event_counts":    {"created": 0, "modified": 0, "deleted": 0, "renamed": 0},
    "timeline":        [],           # (timestamp, count) for chart
}
_state_lock = threading.Lock()

# ── State update helpers (called from monitor/analyzer) ───────────

def update_status(status):
    with _state_lock:
        dashboard_state["status"] = status
    socketio.emit("status_update", {"status": status}, namespace="/")

def push_alert(level, reason, details=""):
    entry = {
        "time":    datetime.now().strftime("%H:%M:%S"),
        "level":   level,
        "reason":  reason,
        "details": details
    }
    with _state_lock:
        dashboard_state["alerts"].insert(0, entry)
        dashboard_state["alerts"] = dashboard_state["alerts"][:100]
    socketio.emit("new_alert", entry, namespace="/")

def push_detection(family, confidence, risk, description=""):
    entry = {
        "time":        datetime.now().strftime("%H:%M:%S"),
        "family":      family,
        "confidence":  confidence,
        "risk":        risk,
        "description": description
    }
    with _state_lock:
        dashboard_state["detections"].insert(0, entry)
    socketio.emit("new_detection", entry, namespace="/")

def push_file_event(event_type, path):
    with _state_lock:
        dashboard_state["total_events"] += 1
        dashboard_state["event_counts"][event_type] = \
            dashboard_state["event_counts"].get(event_type, 0) + 1
        dashboard_state["recent_files"].insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "type": event_type,
            "path": path
        })
        dashboard_state["recent_files"] = dashboard_state["recent_files"][:50]

        # Timeline point every 5 events
        if dashboard_state["total_events"] % 5 == 0:
            dashboard_state["timeline"].append({
                "time":  datetime.now().strftime("%H:%M:%S"),
                "count": dashboard_state["total_events"]
            })
            dashboard_state["timeline"] = dashboard_state["timeline"][-30:]

    socketio.emit("event_update", {
        "total":  dashboard_state["total_events"],
        "counts": dashboard_state["event_counts"],
        "file":   {"time": datetime.now().strftime("%H:%M:%S"),
                   "type": event_type, "path": path}
    }, namespace="/")

def set_start_time():
    with _state_lock:
        dashboard_state["start_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        dashboard_state["status"] = "MONITORING"

# ── Flask routes ──────────────────────────────────────────────────

@app.route("/")
def index():
    with open(os.path.join(os.path.dirname(__file__), "dashboard.html"), "r", encoding="utf-8") as f:
        return f.read()

@app.route("/api/state")
def api_state():
    with _state_lock:
        return jsonify(dashboard_state)

@app.route("/api/report")
def api_report():
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(reports_dir):
        return jsonify({"report": "No reports generated yet."})
    files = sorted(os.listdir(reports_dir), reverse=True)
    if not files:
        return jsonify({"report": "No reports generated yet."})
    latest = os.path.join(reports_dir, files[0])
    with open(latest, "r", encoding="utf-8") as f:
        return jsonify({"report": f.read(), "filename": files[0]})

@socketio.on("connect")
def on_connect():
    with _state_lock:
        emit("full_state", dashboard_state)

# ── Server launcher ───────────────────────────────────────────────

def run_dashboard(host="127.0.0.1", port=5000):
    print(f"\n[DASHBOARD] Starting at http://{host}:{port}")
    print("[DASHBOARD] Open your browser and go to http://localhost:5000\n")
    socketio.run(app, host=host, port=port, debug=False, use_reloader=False)

def start_dashboard_thread(host="127.0.0.1", port=5000):
    t = threading.Thread(target=run_dashboard, args=(host, port), daemon=True)
    t.start()
    time.sleep(1.5)
    return t

if __name__ == "__main__":
    run_dashboard()
