import logging
import time

from .client import EForsyningClient
from .mqtt import MQTTClient
from .publisher import Publisher


class EForsyningService:

    def __init__(self, config):

        self._cfg = config

        self._logger = logging.getLogger("eforsyning2mqtt")

        self._client = EForsyningClient(config)

        self._mqtt = MQTTClient(config.mqtt)

        self._publisher = Publisher(self._mqtt)

    def run(self):

        self._logger.info("Connecting to eForsyning...")

        if not self._client.authenticate():
            raise RuntimeError("Authentication failed")

        self._logger.info("Authentication successful")

        interval = self._cfg.polling.interval_minutes * 60

        while True:

            try:

                self._logger.info("Downloading latest measurements...")

                data = self._client.get_latest()

                self._logger.info("Publishing MQTT topics...")

                self._publisher.publish(data)

                self._logger.info("Publishing completed")

            except Exception:

                self._logger.exception(
                    "Update failed"
                )

            self._logger.info(
                "Sleeping %d minutes",
                self._cfg.polling.interval_minutes,
            )

            time.sleep(interval)