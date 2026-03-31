# ─────────────────────────────────────────────
#  Module 5 — Alerting Module
# ─────────────────────────────────────────────

import time
from logger_module import logger

# Track alerts to avoid spamming same alert repeatedly
_recent_alerts = {}
ALERT_COOLDOWN_SECONDS = 10

# Colour codes for terminal output
COLORS = {
    "RED":    "\033[91m",
    "YELLOW": "\033[93m",
    "CYAN":   "\033[96m",
    "WHITE":  "\033[97m",
    "BOLD":   "\033[1m",
    "RESET":  "\033[0m",
}

RISK_COLORS = {
    "LOW":      COLORS["CYAN"],
    "MEDIUM":   COLORS["YELLOW"],
    "HIGH":     COLORS["RED"],
    "CRITICAL": COLORS["RED"] + COLORS["BOLD"],
}

def _should_suppress(key):
    now = time.time()
    if key in _recent_alerts:
        if now - _recent_alerts[key] < ALERT_COOLDOWN_SECONDS:
            return True
    _recent_alerts[key] = now
    return False

def send_alert(level, reason, details=""):
    """
    Display a formatted alert in the CLI terminal.
    level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL'
    """
    key = f"{level}:{reason}"
    if _should_suppress(key):
        return

    color  = RISK_COLORS.get(level, COLORS["WHITE"])
    reset  = COLORS["RESET"]
    bold   = COLORS["BOLD"]
    border = "═" * 60

    print(f"\n{color}{bold}{border}")
    print(f"  ⚠  RANSOMWATCH ALERT")
    print(f"  Risk Level : {level}")
    print(f"  Reason     : {reason}")
    if details:
        print(f"  Details    : {details}")
    print(f"  Time       : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{border}{reset}\n")

    logger.warning(f"ALERT | Level={level} | Reason={reason} | Details={details}")

def send_detection_banner(family, confidence, risk):
    """Show a big banner when a ransomware family is identified."""
    color  = RISK_COLORS.get(risk, COLORS["WHITE"])
    reset  = COLORS["RESET"]
    bold   = COLORS["BOLD"]
    border = "█" * 60

    print(f"\n{color}{bold}{border}")
    print(f"  🚨  RANSOMWARE FAMILY DETECTED!")
    print(f"  Family     : {family}")
    print(f"  Confidence : {confidence}%")
    print(f"  Risk       : {risk}")
    print(f"  Time       : {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{border}{reset}\n")

    logger.critical(
        f"DETECTION | Family={family} | Confidence={confidence}% | Risk={risk}"
    )

def send_info(message):
    print(f"{COLORS['CYAN']}[INFO]{COLORS['RESET']} {message}")

def send_warning(message):
    print(f"{COLORS['YELLOW']}[WARN]{COLORS['RESET']} {message}")
