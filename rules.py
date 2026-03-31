# ─────────────────────────────────────────────
#  Module 3 — Threshold & Rule Configuration
# ─────────────────────────────────────────────

RULES = {
    # How many file modifications trigger an alert within the time window
    "max_modifications_per_window": 20,

    # How many file renames trigger an alert within the time window
    "max_renames_per_window": 10,

    # How many file creations trigger an alert within the time window
    "max_creations_per_window": 15,

    # Time window in seconds for counting events
    "time_window_seconds": 10,

    # Extensions commonly used by ransomware after encryption
    "suspicious_extensions": [
        ".locked", ".enc", ".crypt", ".crypto", ".encrypted",
        ".wnry", ".wncry", ".wcry", ".wncrypt",          # WannaCry
        ".lockbit", ".lckd",                              # LockBit
        ".ryuk",                                          # Ryuk
        ".maze",                                          # Maze
        ".sodinokibi", ".rEvil",                          # REvil/Sodinokibi
        ".conti",                                         # Conti
        ".darkside",                                      # DarkSide
        ".blackcat", ".alpv",                             # BlackCat/ALPV
        ".hive",                                          # Hive
        ".clop",                                          # Clop
        ".ransom", ".pay2decrypt", ".id-", ".000",
        ".R4A", ".R5A", ".breaking_bad", ".zzzzz"
    ],

    # Extensions that are commonly targeted by ransomware
    "targeted_extensions": [
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".pdf", ".jpg", ".jpeg", ".png", ".mp4", ".mp3",
        ".zip", ".rar", ".sql", ".db", ".mdb", ".txt",
        ".csv", ".html", ".php", ".py", ".java", ".cpp"
    ],

    # How many unique extensions changed = suspicious
    "max_extension_changes": 5,

    # Ratio of renamed files vs total files to flag as suspicious
    "rename_ratio_threshold": 0.5,

    # Directories to EXCLUDE from monitoring (system dirs)
    "excluded_paths": [
        "C:/Windows",
        "C:/Program Files",
        "C:/Program Files (x86)",
        "C:/$Recycle.Bin",
        "C:/ProgramData"
    ]
}

def is_excluded(path):
    """Check if a path should be excluded from monitoring."""
    for excluded in RULES["excluded_paths"]:
        if path.lower().startswith(excluded.lower()):
            return True
    return False

def is_suspicious_extension(path):
    """Check if file has a ransomware-like extension."""
    _, ext = os.path.splitext(path)
    return ext.lower() in RULES["suspicious_extensions"]

def is_targeted_extension(path):
    """Check if file is a common ransomware target."""
    _, ext = os.path.splitext(path)
    return ext.lower() in RULES["targeted_extensions"]

import os
