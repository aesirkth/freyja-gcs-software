from typing import Any
import logging
import csv

logger = logging.getLogger(__name__)

def save_sql_as_csv(sql_data: Any, out_file_name: str):
    try:
        with open(out_file_name, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for row in sql_data:
                spamwriter.writerow(row)
    except Exception as e:
        logger.exception(f"Error while saving SQL data as CSV file. {e}")
