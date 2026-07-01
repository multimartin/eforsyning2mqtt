import json
import logging

from .mqtt import MQTTClient


class Publisher:
    """
    Generic recursive MQTT publisher.

    Publishes only changed values.
    """

    def __init__(self, mqtt: MQTTClient):

        self._mqtt = mqtt

        self._logger = logging.getLogger("eforsyning2mqtt")

        self._last_values = {}

    def publish(self, data: dict):

        self._publish("", data)

    def _publish(self, path: str, value):

        if isinstance(value, dict):

            for key, item in value.items():

                next_path = f"{path}/{key}" if path else key

                self._publish(next_path, item)

            return

        if isinstance(value, list):

            for index, item in enumerate(value):

                next_path = f"{path}/{index}"

                self._publish(next_path, item)

            return

        if value is None:
            value = ""

        elif isinstance(value, bool):
            value = "true" if value else "false"

        elif isinstance(value, (dict, list)):
            value = json.dumps(value)

        else:
            value = str(value)

        previous = self._last_values.get(path)

        if previous == value:
            return

        self._last_values[path] = value

        self._mqtt.publish(path, value)

        self._logger.debug(
            "Published %s = %s",
            path,
            value,
        )