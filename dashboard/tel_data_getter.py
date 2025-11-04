import sqlite3
import logging
import csv

logger = logging.getLogger(__name__)

DB_PATH = "data.db"

def get_tel_data_file() -> bool:
    try:
        with sqlite3.connect(DB_PATH) as con:
            res = con.execute("""
                SELECT * FROM telemetry_data
            """)
            if not res:
                logger.exception(f"Given file '{DB_PATH}' is empty.")
                return False
            
            with open('telemetry_data.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for row in res:
                    spamwriter.writerow(row)

        return True
    except Exception:
        logger.exception("Error while getting telemetry data from disk storage.")
        return False

if __name__ == "__main__":
    get_tel_data_file()
