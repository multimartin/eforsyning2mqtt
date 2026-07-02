import logging
import time
import requests

from .client import EForsyningClient
from .mqtt import MQTTClient
from .publisher import Publisher
from .pyeforsyning.eforsyning import LoginFailed, HTTPFailed


class EForsyningService:

    def __init__(self, config):

        self._cfg = config

        self._logger = logging.getLogger("eforsyning2mqtt")

        self._client = EForsyningClient(config)

        self._mqtt = MQTTClient(config.mqtt)

        self._publisher = Publisher(self._mqtt)

    def run(self):

        self._logger.info("Connecting to eForsyning")

        if not self._client.authenticate():
            raise RuntimeError("Authentication failed")

        self._logger.info("Authentication successful")

        interval = self._cfg.polling.interval_minutes * 60

        while True:

            try:
                self._logger.debug("Downloading latest measurements")

                measurement = self._client.get_latest()

                self._logger.debug("Publishing MQTT topics")

                self._publisher.publish(measurement)

                self._logger.info("Update completed")

            except (RuntimeError, LoginFailed, HTTPFailed, requests.exceptions.RequestException, OSError, ValueError) as exc:
                # Log expected errors and continue loop; do not silently swallow unexpected errors
                self._logger.exception("Update failed: %s", exc)

            self._logger.info(
                "Sleeping %d minutes...",
                self._cfg.polling.interval_minutes,
            )

            time.sleep(interval)

    def stop(self):

        self._mqtt.close()