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

    def get_latest_data():
        pass
