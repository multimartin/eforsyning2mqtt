import logging

from eforsyning2mqtt.client import EForsyningClient
from eforsyning2mqtt.config import load_config
from eforsyning2mqtt.logging_config import configure_logging
from eforsyning2mqtt.version import VERSION


def main() -> None:
    configure_logging()

    logger = logging.getLogger("eforsyning2mqtt")

    logger.info("--------------------------------")
    logger.info("eforsyning2mqtt %s", VERSION)
    logger.info("--------------------------------")

    cfg = load_config()

    logger.info("Supplier ID : %s", cfg.eforsyning.supplier_id)
    logger.info("MQTT Host   : %s", cfg.mqtt.host)
    logger.info("Polling     : %d minutes", cfg.polling.interval_minutes)

    client = EForsyningClient(cfg)

    logger.info("Connecting to eForsyning...")

    if not client.authenticate():
        logger.error("Authentication failed")
        return

    logger.info("Authentication successful")

    measurement = client.update()

    logger.info("Measurement received")

    from pprint import pformat

    logger.info(pformat(measurement.raw))

if __name__ == "__main__":
    main()