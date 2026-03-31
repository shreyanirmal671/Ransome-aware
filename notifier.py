# ─────────────────────────────────────────────
#  Notifier — Desktop Pop-up Alerts
#  Sends Windows toast notifications on detection
# ─────────────────────────────────────────────

import threading

def _try_notify(title, message, level="HIGH"):
    """Try multiple notification methods in order of preference."""
    notified = False

    # Method 1: plyer (cross-platform)
    try:
        from plyer import notification
        icons = {"LOW": "", "MEDIUM": "", "HIGH": "", "CRITICAL": ""}
        notification.notify(
            title=f"RansomWatch {icons.get(level, '')} {level} ALERT",
            message=message,
            app_name="RansomWatch",
            timeout=8
        )
        notified = True
        return
    except Exception:
        pass

    # Method 2: win10toast (Windows only)
    try:
        from win10toast import ToastNotifier
        toaster = ToastNotifier()
        toaster.show_toast(
            f"RansomWatch {level} ALERT",
            message,
            duration=8,
            threaded=True
        )
        notified = True
        return
    except Exception:
        pass

    # Method 3: Windows balloon via ctypes (always available on Windows)
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(
            0,
            f"{message}",
            f"RansomWatch — {level} ALERT",
            0x00000010  # MB_ICONERROR
        )
        notified = True
        return
    except Exception:
        pass

    if not notified:
        print(f"[NOTIFY] {level}: {message}")


def send_popup(title, message, level="HIGH"):
    """Send desktop popup in a background thread (non-blocking)."""
    t = threading.Thread(
        target=_try_notify,
        args=(title, message, level),
        daemon=True
    )
    t.start()


def send_detection_popup(family, confidence, risk):
    send_popup(
        title=f"Ransomware Detected: {family}",
        message=f"Family: {family}\nConfidence: {confidence}%\nRisk: {risk}\nOpen dashboard: http://localhost:5000",
        level=risk
    )


def send_alert_popup(level, reason, details=""):
    msg = reason
    if details:
        msg += f"\n{details[:120]}"
    msg += "\nView: http://localhost:5000"
    send_popup(title=f"RansomWatch Alert [{level}]", message=msg, level=level)
