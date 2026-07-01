from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class Measurement:
    """Normalized measurement returned from eForsyning."""

    timestamp: datetime

    supply_temperature: float | None = None
    return_temperature: float | None = None

    flow_temperature: float | None = None

    effect_kw: float | None = None

    energy_mwh: float | None = None

    volume_m3: float | None = None

    flow_lh: float | None = None

    pressure_bar: float | None = None

    raw: dict[str, Any] = field(default_factory=dict)