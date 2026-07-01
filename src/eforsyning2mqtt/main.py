import logging

from eforsyning2mqtt.client import EForsyningClient
from eforsyning2mqtt.config import load_config
from eforsyning2mqtt.logging_config import configure_logging
from eforsyning2mqtt.mqtt import MQTTClient
from eforsyning2mqtt.version import VERSION


def publish_measurements(mqtt: MQTTClient, data: dict):

    mqtt.publish("raw", data)

    mqtt.publish("temp-forward", data.get("temp-forward"))

    mqtt.publish("temp-return", data.get("temp-return"))

    mqtt.publish("temp-cooling", data.get("temp-cooling"))

    mqtt.publish("energy-used", data.get("energy-used"))

    mqtt.publish("energy-end", data.get("energy-end"))

    mqtt.publish("energy-total-used", data.get("energy-total-used"))

    mqtt.publish("energy-use-prognosis", data.get("energy-use-prognosis"))

    mqtt.publish("water-used", data.get("water-used"))

    mqtt.publish("water-end", data.get("water-end"))

    mqtt.publish("billing", data.get("billing"))

    mqtt.publish("history", data.get("data"))

    mqtt.publish("year", data.get("year"))


def main():

    configure_logging()

    logger = logging.getLogger("eforsyning2mqtt")

    logger.info("--------------------------------")
    logger.info("eforsyning2mqtt %s", VERSION)
    logger.info("--------------------------------")

    cfg = load_config()

    logger.info("Connecting to eForsyning...")

    ef = EForsyningClient(cfg)

    if not ef.authenticate():
        logger.error("Authentication failed")
        return

    logger.info("Authentication OK")

    logger.info("Downloading measurements...")

    data = ef.get_latest()

    logger.info("Connecting to MQTT...")

    mqtt = MQTTClient(cfg.mqtt)

    mqtt.publish_dict(data)

    mqtt.disconnect()

    logger.info("Published successfully")


if __name__ == "__main__":
    main()