import logging
import os
from datetime import datetime

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = os.path.join(LOG_DIR, f"ransomwatch_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("RansomWatch")

def log_event(event_type, file_path, extra=""):
    msg = f"EVENT={event_type} | FILE={file_path}"
    if extra:
        msg += f" | {extra}"
    logger.info(msg)

def log_alert(level, message):
    logger.warning(f"ALERT [{level}] | {message}")

def log_action(action, detail=""):
    msg = f"ACTION={action}"
    if detail:
        msg += f" | {detail}"
    logger.critical(msg)

def get_log_filename():
    return log_filename
