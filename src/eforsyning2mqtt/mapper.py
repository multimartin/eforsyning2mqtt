from datetime import datetime

from .measurement import Measurement


class MeasurementMapper:

    @staticmethod
    def from_api(data: dict) -> Measurement:

        return Measurement(
            timestamp=datetime.now(),
            raw=data,
        )