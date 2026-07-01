import logging
import time

from eforsyning2mqtt.client import EForsyningClient
from eforsyning2mqtt.config import load_config
from eforsyning2mqtt.logging_config import configure_logging
from eforsyning2mqtt.mqtt import MQTTClient
from eforsyning2mqtt.publisher import Publisher
from eforsyning2mqtt.version import VERSION


def main() -> None:

    configure_logging()

    logger = logging.getLogger("eforsyning2mqtt")

    logger.info("--------------------------------")
    logger.info("eforsyning2mqtt %s", VERSION)
    logger.info("--------------------------------")

    cfg = load_config()

    client = EForsyningClient(cfg)

    mqtt = MQTTClient(cfg.mqtt)

    publisher = Publisher(mqtt)

    try:

        logger.info("Connecting to eForsyning...")

        if not client.authenticate():
            logger.error("Authentication failed")
            return

        logger.info("Authentication OK")

        interval = cfg.polling.interval_minutes * 60

        while True:

            try:

                logger.info("Downloading measurements...")

                data = client.get_latest()

                logger.info("Publishing MQTT topics...")

                publisher.publish(data)

                logger.info("Publishing completed")

            except Exception:

                logger.exception("Update failed")

            logger.info(
                "Sleeping %d minutes...",
                cfg.polling.interval_minutes,
            )

            time.sleep(interval)

    except KeyboardInterrupt:

        logger.info("Stopping...")

    finally:

        mqtt.close()

        logger.info("Shutdown complete")


if __name__ == "__main__":
    main()