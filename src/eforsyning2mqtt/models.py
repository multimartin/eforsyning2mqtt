from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class EForsyningConfig:
    username: str
    password: str
    supplier_id: str


@dataclass(slots=True)
class MQTTConfig:
    host: str
    port: int
    username: str
    password: str
    topic: str


@dataclass(slots=True)
class PollingConfig:
    interval_minutes: int


@dataclass(slots=True)
class Config:
    eforsyning: EForsyningConfig
    mqtt: MQTTConfig
    polling: PollingConfig
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(slots=True)
class CurrentMeasurement:
    supply_temperature: float = 0.0
    return_temperature: float = 0.0
    cooling: float = 0.0

    energy_today: float = 0.0
    energy_total: float = 0.0
    energy_forecast: float = 0.0

    water_today: float = 0.0
    water_total: float = 0.0


@dataclass(slots=True)
class BillingInfo:
    amount_paid: float = 0.0
    amount_remaining: float = 0.0
    amount_vat: float = 0.0
    mwh_price: float = 0.0
    m3_price: float = 0.0


@dataclass(slots=True)
class DailyMeasurement:
    date_from: str = ""
    date_to: str = ""

    energy_used: float = 0.0
    energy_total: float = 0.0

    water_used: float = 0.0
    water_total: float = 0.0

    supply_temperature: float = 0.0
    return_temperature: float = 0.0
    cooling: float = 0.0


@dataclass(slots=True)
class Measurement:
    timestamp: datetime

    current: CurrentMeasurement

    billing: BillingInfo

    history: list[DailyMeasurement] = field(default_factory=list)

    raw: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------


@dataclass(slots=True)
class EForsyningConfig:
    username: str
    password: str
    supplier_id: str


@dataclass(slots=True)
class MQTTConfig:
    host: str
    port: int
    username: str
    password: str
    topic: str


@dataclass(slots=True)
class PollingConfig:
    interval_minutes: int


@dataclass(slots=True)
class Config:
    eforsyning: EForsyningConfig
    mqtt: MQTTConfig
    polling: PollingConfig