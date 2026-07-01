from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Measurement:
    timestamp: datetime
    raw: dict[str, Any] = field(default_factory=dict)