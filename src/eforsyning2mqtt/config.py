import os

from .exceptions import ConfigurationError
from .models import Config, EForsyningConfig, MQTTConfig, PollingConfig


def _env(name: str, default: str | None = None) -> str:

    value = os.getenv(name, default)

    if value is None:
        raise ConfigurationError(
            f"Environment variable '{name}' is not defined."
        )

    return value


def load_config() -> Config:

    return Config(

        eforsyning=EForsyningConfig(
            username=_env("EFORSYNING_USERNAME"),
            password=_env("EFORSYNING_PASSWORD"),
            supplier_id=_env("EFORSYNING_SUPPLIER_ID"),
        ),

        mqtt=MQTTConfig(
            host=_env("MQTT_HOST"),
            port=int(_env("MQTT_PORT", "1883")),
            username=_env("MQTT_USERNAME", ""),
            password=_env("MQTT_PASSWORD", ""),
            topic=_env("MQTT_TOPIC", "eforsyning"),
        ),

        polling=PollingConfig(
            interval_minutes=int(
                _env("POLLING_INTERVAL", "60")
            )
        ),
    )