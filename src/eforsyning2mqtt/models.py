from dataclasses import dataclass
from datetime import datetime


@dataclass
class CurrentMeasurement:
    supply_temperature: float
    return_temperature: float
    cooling: float

    energy_today: float
    energy_total: float
    energy_forecast: float

    water_today: float
    water_total: float


@dataclass
class BillingInfo:
    amount_paid: float
    amount_remaining: float
    amount_vat: float
    mwh_price: float
    m3_price: float


@dataclass
class DailyMeasurement:
    date_from: str
    date_to: str

    energy_used: float
    water_used: float

    supply_temperature: float
    return_temperature: float
    cooling: float


@dataclass
class Measurement:

    timestamp: datetime

    current: CurrentMeasurement

    billing: BillingInfo

    history: list[DailyMeasurement]

    raw: dict