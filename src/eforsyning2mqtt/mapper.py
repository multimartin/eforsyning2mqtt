from datetime import datetime
from typing import Dict, Mapping

from eforsyning2mqtt.measurement import Measurement


class MeasurementMapper:
    """Utility to convert raw eForsyning API payloads into
    the internal :class:`Measurement` model.
    """

    @staticmethod
    def from_api(data: Mapping[str, object]) -> Measurement:
        """Create a :class:`Measurement` from raw API data.

        Parameters
        ----------
        data:
            Mapping containing the API JSON-decoded payload.

        Returns
        -------
        Measurement
            Populated measurement object.
        """

        return Measurement(
            timestamp=datetime.now(),
            values=dict(data),
        )