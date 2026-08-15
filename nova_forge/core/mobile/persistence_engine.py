import os
import time
from datetime import datetime

import psutil
import psycopg2
import requests

# --- CONFIGURATION (Environment Variables) ---
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "prs_001"),
    "user": os.getenv("DB_USER", "phoenix_admin"),
    "password": os.getenv("DB_PASS"),
}
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK_URL")

# --- CORE MODULES ---


def send_tactical_alert(message, priority="NORMAL"):
    """Filters and sends alerts to Discord based on Signal-to-Noise rules."""
    if priority not in ["HIGH", "CRITICAL"]:
        print(f"[{priority}] {message}")  # Silent local log
        return

    color = 16711680 if priority == "CRITICAL" else 3066993
    payload = {
        "embeds": [
            {
                "title": f"🛡️ Sentinel Report: {priority}",
                "description": message,
                "color": color,
                "footer": {"text": "Synarche Workspace • Autonomous Loop"},
            }
        ]
    }
    try:
        requests.post(DISCORD_WEBHOOK, json=payload)
    except Exception as e:
        print(f"Failed to alert Discord: {e}")


def emit_heartbeat():
    """Captures hardware vitals and updates the system_vitals table."""
    try:
        vitals = {
            "cpu": psutil.cpu_percent(interval=1),
            "ram": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage("/").percent,
            "time": datetime.now(),
        }

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        query = """
            INSERT INTO system_vitals (system_id, cpu_percent, ram_percent, disk_percent, last_pulse)
            VALUES (1, %s, %s, %s, %s)
            ON CONFLICT (system_id) DO UPDATE SET
                cpu_percent = EXCLUDED.cpu_percent,
                ram_percent = EXCLUDED.ram_percent,
                disk_percent = EXCLUDED.disk_percent,
                last_pulse = EXCLUDED.last_pulse;
        """
        cur.execute(
            query, (vitals["cpu"], vitals["ram"], vitals["disk"], vitals["time"])
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        send_tactical_alert(f"Heartbeat Failure: {e}", priority="CRITICAL")
        return False


def check_lockdown_status():
    """Checks if a lockdown has been triggered remotely or locally."""
    if os.path.exists("lockdown.trigger"):
        send_tactical_alert(
            "EMERGENCY LOCKDOWN DETECTED. Terminating processes.", priority="CRITICAL"
        )
        # Log to physical file before death
        with open("lockdown_event.log", "a") as f:
            f.write(f"Lockdown at {datetime.now()}\n")
        exit(1)


def process_sophia_ingestion():
    """Placeholder for Sophia's Lore Ingestion logic (Gmail API integration)."""
    # Logic for scanning Gmail and writing to sophia_lore_ingestion table goes here
    print("Sophia: Scanning lore buffers...")


# --- MAIN PERSISTENCE LOOP ---


def run_engine():
    """The 24/7 autonomous cycle."""
    print("🚀 Synarche Persistence Engine Initialized.")
    send_tactical_alert("System Online and Autonomous.", priority="HIGH")

    while True:
        # 1. Security Check
        check_lockdown_status()

        # 2. Vital Signs
        pulse_success = emit_heartbeat()

        # 3. Agent Tasks (If healthy)
        if pulse_success:
            process_sophia_ingestion()
            # Add Axion optimization calls here

        # 4. Wait for next pulse (Standard 5-minute interval)
        time.sleep(300)


if __name__ == "__main__":
    run_engine()
