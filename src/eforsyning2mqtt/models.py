from dataclasses import dataclass


@dataclass(slots=True)
class MQTTConfig:
    host: str
    port: int
    username: str
    password: str
    topic: str

@dataclass(slots=True)
class EForsyningConfig:
    username: str
    password: str
    supplier_id: str

@dataclass(slots=True)
class PollingConfig:
    interval_minutes: int


@dataclass(slots=True)
class Config:

    mqtt: MQTTConfig

    eforsyning: EForsyningConfig

    polling: PollingConfig
