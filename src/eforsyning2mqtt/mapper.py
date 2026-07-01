from datetime import datetime

from .measurement import Measurement


class MeasurementMapper:
    """Converts raw eForsyning data to our internal model."""

    @staticmethod
    def from_api(data: dict) -> Measurement:
        return Measurement(
            timestamp=datetime.now(),
            raw=data,
        )