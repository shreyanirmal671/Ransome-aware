# 🛡️ RansomWatch — Real-Time Ransomware Detection System

RansomWatch is a **real-time ransomware detection and response system** that monitors file system activity, detects suspicious behavior patterns, classifies ransomware families, and automatically triggers alerts and containment actions.

---

## 🚀 Features

* 🔍 **Real-Time File Monitoring**

  * Tracks file creation, modification, deletion, and renaming events across drives 

* 🧠 **Behavior-Based Detection Engine**

  * Detects ransomware patterns using rule-based analysis (mass rename, modification, etc.) 

* 🚨 **Smart Alerting System**

  * CLI alerts with cooldown to prevent spam 
  * Desktop notifications (cross-platform fallback support) 

* 🧬 **Ransomware Family Classification**

  * Identifies families like WannaCry, LockBit, Ryuk, Conti, etc. 

* 📊 **Live Web Dashboard**

  * Real-time visualization of alerts, detections, and file activity 
  * Interactive UI powered by Socket.IO + Chart.js 

* 📋 **Incident Report Generation**

  * Detailed logs of events, alerts, detections, and actions 

* 🧯 **Automated Response & Containment**

  * Pause monitoring, restrict file access, kill processes 

* 🧪 **Safe Simulation Mode**

  * Simulate ransomware behavior for testing (no real malware) 

---

## 🏗️ Project Structure

```
RansomWatch/
│
├── monitor.py            # File system monitoring (Watchdog)
├── analyzer.py           # Behavior analysis engine
├── rules.py              # Detection rules & thresholds
├── classifier.py         # Ransomware family classification
├── alerting.py           # CLI alert system
├── notifier.py           # Desktop notifications
├── response.py           # Containment & response actions
├── report.py             # Incident report generator
├── logger_module.py      # Logging system
│
├── dashboard_server.py   # Flask + SocketIO backend
├── dashboard.html        # Web dashboard UI
│
├── simulator.py          # Safe ransomware simulation
├── cli_menu.py           # Main entry point (run this)
│
├── logs/                 # Generated logs
└── reports/              # Generated reports
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ransomwatch.git
cd ransomwatch
```

### 2. Install dependencies

```bash
pip install watchdog flask flask-socketio plyer
```

(Optional for Windows notifications)

```bash
pip install win10toast
```

---

## ▶️ Usage

### Run the system

```bash
python cli_menu.py
```

This will:

* Start the dashboard server
* Open the web dashboard at:
  👉 http://localhost:5000 

---

## 📌 CLI Options

```
[1] Start Monitoring (30 seconds)
[2] Start Monitoring (custom duration)
[3] Run Safe Simulation
[4] View Logs
[5] Generate Report
[6] View Summary
[7] Open Dashboard
[0] Exit
```

---

## 🔎 Detection Logic

RansomWatch detects ransomware using behavioral patterns such as:

* ⚠️ Suspicious file extensions (e.g., `.locked`, `.enc`)
* ⚠️ Mass file modifications in short time
* ⚠️ Mass file renaming
* ⚠️ Multiple extension changes in same directory
* ⚠️ High ratio of rename/modify events

Configured in:

```
rules.py
```



---

## 🧬 Supported Ransomware Families

* WannaCry
* LockBit
* REvil / Sodinokibi
* Ryuk
* Maze
* Conti
* DarkSide
* Hive
* Clop
* Generic Ransomware



---

## 📊 Dashboard Features

* 📈 Live event activity chart
* ⚠️ Real-time alert feed
* 🔴 Ransomware detection panel
* 📁 File activity stream
* 📋 Incident report viewer



---

## 🧯 Automated Response Actions

* Pause monitoring
* Restrict file write access
* Kill suspicious processes
* Trigger full containment



---

## 🧪 Simulation Mode

Test detection safely without real malware:

* Mass rename simulation
* Mass modification simulation
* Full encryption pattern simulation



---

## 📝 Logging

* All events and alerts are logged automatically
* Logs stored in:

```
/logs/ransomwatch_*.log
```



---

## ⚠️ Disclaimer

This tool is for **educational and defensive security purposes only**.
Do NOT use it in unauthorized environments.

---

## 👨‍💻 Author

Your Name
GitHub: https://github.com/your-username

---

## ⭐ Future Improvements

* Machine learning-based detection
* Cloud-based alerting
* Multi-device monitoring
* SIEM integration

---

## 📄 License

MIT License

---

**🛡️ Stay Safe. Detect Early. Respond Faster.**
