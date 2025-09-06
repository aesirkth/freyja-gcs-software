from models.input_data import TelemetryInput

class DataQueue:
    def __init__(self):
        self.logger = logger = logging.getLogger(__name__)
        self.tel_data_queue = []

    def insert_data(data: TelemetryData):
        try:
            self.tel_data_queue.insert(0, data)
        except Exception as e:
            self.logger.e(f"Error while inserting telemetry data into queue {e}")

    def get_latest_data() -> TelemetryInput:
        try:
            latest_data = self.tel_data_queue[0]

            if isinstance(data, TelemetryInput):
                return latest_data
            else:
                raise
        except Exception as e:
            self.logger.e(f"Error while getting latest telemetry data from queue {e}")

