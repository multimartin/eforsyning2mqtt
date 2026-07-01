import json

import paho.mqtt.client as mqtt


class MQTTClient:

    def __init__(self, config):

        self._topic = config.topic.rstrip("/")

        self._client = mqtt.Client()

        if config.username:

            self._client.username_pw_set(
                config.username,
                config.password,
            )

        self._client.connect(
            config.host,
            config.port,
            60,
        )

    def publish(self, topic, payload):

        if isinstance(payload, (dict, list)):
            payload = json.dumps(payload)

        if payload is None:
            payload = ""

        self._client.publish(
            f"{self._topic}/{topic}",
            payload,
            retain=True,
        )

    def publish_dict(self, data):

        self._publish_recursive("", data)

    def _publish_recursive(self, path, value):

        if isinstance(value, dict):

            for key, val in value.items():

                next_path = f"{path}/{key}" if path else key

                self._publish_recursive(next_path, val)

            return

        if isinstance(value, list):

            for index, val in enumerate(value):

                next_path = f"{path}/{index}"

                self._publish_recursive(next_path, val)

            return

        self.publish(path, value)

    def disconnect(self):

        self._client.disconnect()