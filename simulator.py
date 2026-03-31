# ─────────────────────────────────────────────
#  Module 10 — Safe Ransomware Simulation
#  ⚠  FOR TESTING ONLY — Uses dummy files
# ─────────────────────────────────────────────

import os
import time
import random
import string

SIM_DIR = "simulation_test_files"

def _create_sim_dir():
    os.makedirs(SIM_DIR, exist_ok=True)

def _random_content():
    return "DUMMY FILE - RANSOMWATCH SIMULATION TEST\n" + \
           ''.join(random.choices(string.ascii_letters, k=200))

def create_dummy_files(count=30):
    """Create dummy test files to be used in simulation."""
    _create_sim_dir()
    created = []
    extensions = [".txt", ".docx", ".pdf", ".jpg", ".xlsx"]
    for i in range(count):
        ext  = random.choice(extensions)
        name = f"test_file_{i:03d}{ext}"
        path = os.path.join(SIM_DIR, name)
        with open(path, "w") as f:
            f.write(_random_content())
        created.append(path)
    print(f"[SIM] ✅ Created {count} dummy files in '{SIM_DIR}/'")
    return created

def simulate_mass_rename(delay=0.05):
    """
    Simulate ransomware-style mass renaming:
    renames all dummy files to .locked extension
    """
    _create_sim_dir()
    files = [f for f in os.listdir(SIM_DIR)
             if not f.endswith(".locked")]

    if not files:
        print("[SIM] No files to rename. Run create_dummy_files() first.")
        return

    print(f"[SIM] 🔄 Simulating mass rename ({len(files)} files)...")
    for fname in files:
        old_path = os.path.join(SIM_DIR, fname)
        new_path = os.path.join(SIM_DIR, fname + ".locked")
        os.rename(old_path, new_path)
        print(f"[SIM]  Renamed: {fname} -> {fname}.locked")
        time.sleep(delay)
    print("[SIM] ✅ Mass rename simulation complete.")

def simulate_mass_modification(delay=0.05):
    """
    Simulate rapid file modifications (encryption-like writing)
    """
    _create_sim_dir()
    files = os.listdir(SIM_DIR)

    if not files:
        print("[SIM] No files found. Run create_dummy_files() first.")
        return

    print(f"[SIM] ✏  Simulating mass file modification ({len(files)} files)...")
    for fname in files:
        path = os.path.join(SIM_DIR, fname)
        with open(path, "w") as f:
            # Write garbled content to simulate encryption
            f.write(''.join(random.choices(string.printable, k=512)))
        print(f"[SIM]  Modified: {fname}")
        time.sleep(delay)
    print("[SIM] ✅ Mass modification simulation complete.")

def simulate_encryption_pattern(delay=0.03):
    """
    Full simulation: create files → modify → rename to .enc
    Mimics real ransomware behaviour pattern.
    """
    print("\n[SIM] 🚨 Starting full encryption pattern simulation...")
    print("[SIM] Step 1: Creating dummy files...")
    create_dummy_files(25)
    time.sleep(1)

    print("\n[SIM] Step 2: Simulating rapid modification (encryption phase)...")
    simulate_mass_modification(delay=delay)
    time.sleep(1)

    print("\n[SIM] Step 3: Simulating mass rename to .enc (post-encryption rename)...")
    files = [f for f in os.listdir(SIM_DIR) if not f.endswith(".enc")]
    for fname in files:
        old = os.path.join(SIM_DIR, fname)
        new = os.path.join(SIM_DIR, fname + ".enc")
        os.rename(old, new)
        print(f"[SIM]  {fname} -> {fname}.enc")
        time.sleep(delay)

    print("\n[SIM] ✅ Full simulation complete. Check alerts above.")

def cleanup_simulation():
    """Remove all simulation test files."""
    import shutil
    if os.path.exists(SIM_DIR):
        shutil.rmtree(SIM_DIR)
        print(f"[SIM] 🧹 Simulation directory '{SIM_DIR}' cleaned up.")
    else:
        print("[SIM] Nothing to clean up.")

if __name__ == "__main__":
    simulate_encryption_pattern()
