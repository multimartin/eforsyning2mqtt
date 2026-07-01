from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Measurement:
    """
    Complete dataset received from eForsyning.
    """

    timestamp: datetime

    values: dict[str, Any] = field(default_factory=dict)

    def get(self, key: str, default=None):
        return self.values.get(key, default)

    def items(self):
        return self.values.items()

    def keys(self):
        return self.values.keys()

    def as_dict(self) -> dict[str, Any]:
        return self.values