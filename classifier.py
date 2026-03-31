# ─────────────────────────────────────────────
#  Module 4 — Ransomware Family Classification
# ─────────────────────────────────────────────

from logger_module import logger

# Each family defined by behavioural signatures (NOT file signatures)
RANSOMWARE_FAMILIES = {
    "WannaCry": {
        "extensions":   [".wnry", ".wncry", ".wcry", ".wncrypt", ".wncryt"],
        "note_names":   ["@Please_Read_Me@.txt", "!Please Read Me!.txt"],
        "behaviour":    "mass_encrypt_rename",
        "description":  "Worm-like. Encrypts files then renames with .wncry. Spreads via EternalBlue.",
        "risk":         "CRITICAL"
    },
    "LockBit": {
        "extensions":   [".lockbit", ".lckd", ".abcd"],
        "note_names":   ["Restore-My-Files.txt", "LockBit_Ransomware.hta"],
        "behaviour":    "fast_mass_rename",
        "description":  "Extremely fast encryptor. Renames all files then drops ransom note.",
        "risk":         "CRITICAL"
    },
    "REvil/Sodinokibi": {
        "extensions":   [".sodinokibi", ".revil", ".randomext"],
        "note_names":   ["[ext]-readme.txt", "HOW-TO-DECRYPT.txt"],
        "behaviour":    "targeted_encrypt",
        "description":  "Targets business files. Uses random extension per victim.",
        "risk":         "HIGH"
    },
    "Ryuk": {
        "extensions":   [".ryuk", ".RYK"],
        "note_names":   ["RyukReadMe.txt", "UNIQUE_ID_DO_NOT_REMOVE.txt"],
        "behaviour":    "slow_targeted",
        "description":  "Manual deployment. Targets enterprise. Deletes shadow copies.",
        "risk":         "CRITICAL"
    },
    "Maze": {
        "extensions":   [".maze"],
        "note_names":   ["DECRYPT-FILES.txt", "maze-decrypt.txt"],
        "behaviour":    "exfil_then_encrypt",
        "description":  "Double extortion. Steals data before encrypting.",
        "risk":         "CRITICAL"
    },
    "Conti": {
        "extensions":   [".conti", ".CONTI"],
        "note_names":   ["CONTI_README.txt", "readme.txt"],
        "behaviour":    "fast_mass_encrypt",
        "description":  "Very fast multi-threaded encryption. Targets networks.",
        "risk":         "CRITICAL"
    },
    "DarkSide": {
        "extensions":   [".darkside"],
        "note_names":   ["README.[ext].TXT"],
        "behaviour":    "selective_encrypt",
        "description":  "Avoids CIS countries. Selective targeting of critical infrastructure.",
        "risk":         "HIGH"
    },
    "BlackCat/ALPV": {
        "extensions":   [".blackcat", ".alpv", ".sykffle"],
        "note_names":   ["RECOVER-[ext]-FILES.txt"],
        "behaviour":    "cross_platform_encrypt",
        "description":  "Written in Rust. Cross-platform (Windows/Linux/VMware).",
        "risk":         "HIGH"
    },
    "Hive": {
        "extensions":   [".hive", ".key.hive"],
        "note_names":   ["HOW_TO_DECRYPT.txt"],
        "behaviour":    "double_extortion",
        "description":  "Healthcare sector targeting. Double extortion model.",
        "risk":         "HIGH"
    },
    "Clop": {
        "extensions":   [".clop", ".Clop"],
        "note_names":   ["ClopReadMe.txt", "CLOP-README.TXT"],
        "behaviour":    "mass_encrypt_delete_backups",
        "description":  "Deletes backups and shadow copies. Large-scale campaigns.",
        "risk":         "HIGH"
    },
    "Generic Ransomware": {
        "extensions":   [".locked", ".enc", ".crypt", ".crypto", ".encrypted", ".ransom"],
        "note_names":   ["README.txt", "HOW_TO_DECRYPT.txt", "DECRYPT_INSTRUCTION.txt"],
        "behaviour":    "generic_encrypt",
        "description":  "Unknown or generic ransomware behaviour detected.",
        "risk":         "MEDIUM"
    }
}

def classify(detected_extensions, rename_count, mod_count, suspicious_notes=None):
    """
    Classify ransomware family based on observed behaviour.
    Returns list of (family_name, confidence, details) sorted by confidence.
    """
    results = []

    for family, profile in RANSOMWARE_FAMILIES.items():
        score = 0
        matched_ext = []

        # Match extensions
        for ext in detected_extensions:
            if ext.lower() in [e.lower() for e in profile["extensions"]]:
                score += 40
                matched_ext.append(ext)

        # Match ransom notes
        if suspicious_notes:
            for note in suspicious_notes:
                if any(n.lower() in note.lower() for n in profile["note_names"]):
                    score += 30

        # Behaviour matching
        behaviour = profile["behaviour"]
        if behaviour in ("mass_encrypt_rename", "fast_mass_rename") and rename_count > 10:
            score += 20
        if behaviour in ("fast_mass_encrypt", "mass_encrypt_delete_backups") and mod_count > 20:
            score += 20
        if behaviour == "generic_encrypt" and (rename_count > 5 or mod_count > 10):
            score += 10

        if score > 0:
            confidence = min(score, 100)
            results.append({
                "family":      family,
                "confidence":  confidence,
                "risk":        profile["risk"],
                "description": profile["description"],
                "matched_ext": matched_ext
            })

    results.sort(key=lambda x: x["confidence"], reverse=True)

    if results:
        top = results[0]
        logger.warning(
            f"CLASSIFICATION | Family={top['family']} | "
            f"Confidence={top['confidence']}% | Risk={top['risk']}"
        )

    return results

def get_family_info(family_name):
    return RANSOMWARE_FAMILIES.get(family_name, {})
