from pathlib import Path
from models.input_tel_data import TelemetryInput
import logging
import sqlite3

logger = logging.getLogger(__name__)

DB_PATH = "data.db"

def save_to_disk(data: TelemetryInput) -> bool:
    try:
        with sqlite3.connect(DB_PATH) as con:
            con.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    flight_state TEXT,
                    loki_state TEXT,
                    loki_substate TEXT,
                    ax REAL,
                    ay REAL,
                    az REAL
                )
            """)

            con.execute(
                "INSERT INTO telemetry_data "
                "(flight_state, loki_state, loki_substate, ax, ay, az) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    getattr(data, "flight_state", None),
                    getattr(data, "loki_state", None),
                    getattr(data, "loki_substate", None),
                    data.ax, data.ay, data.az,
                ),
            ),

        return True

    except Exception:
        logger.exception("Error while saving telemetry data to persistent disk storage.")
        return False
    