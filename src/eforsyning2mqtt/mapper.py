from datetime import datetime

from eforsyning2mqtt.measurement import Measurement


class MeasurementMapper:
    """
    Converts raw eForsyning data into the internal Measurement model.
    """

    @staticmethod
    def from_api(data: dict) -> Measurement:

        return Measurement(
            timestamp=datetime.now(),
            values=data,
        )