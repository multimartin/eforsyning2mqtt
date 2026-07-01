from pathlib import Path
import yaml

from .exceptions import ConfigurationError
from .models import *


CONFIG_FILE = Path("/config/config.yaml")


def load_config() -> Config:

    if not CONFIG_FILE.exists():
        raise ConfigurationError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    with CONFIG_FILE.open() as f:
        cfg = yaml.safe_load(f)

    return Config(

        eforsyning=EForsyningConfig(
            username=str(cfg["eforsyning"]["username"]),
            password=str(cfg["eforsyning"]["password"]),
            supplier_id=str(cfg["eforsyning"]["supplier_id"]),
        ),

        mqtt=MQTTConfig(
            host=str(cfg["mqtt"]["host"]),
            port=int(cfg["mqtt"]["port"]),
            username=str(cfg["mqtt"]["username"]),
            password=str(cfg["mqtt"]["password"]),
            topic=str(cfg["mqtt"]["topic"]),
        ),

        polling=PollingConfig(
            interval_minutes=int(
                cfg["polling"]["interval_minutes"]
            )
        ),
    )
