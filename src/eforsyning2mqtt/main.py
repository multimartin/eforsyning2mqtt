import json

from eforsyning2mqtt.discovery import DiscoveryPublisher


class Publisher:

    def __init__(self, mqtt):

        self._mqtt = mqtt

        self._discovery = DiscoveryPublisher(
            mqtt=mqtt,
            base_topic=mqtt._cfg.topic,
        )

        self._discovered = set()

    def publish(self, data: dict):

        self._publish_dict(data)

    def _publish_dict(self, data: dict, prefix: str = ""):

        for key, value in data.items():

            topic = f"{prefix}/{key}" if prefix else key

            if isinstance(value, dict):

                self._publish_dict(value, topic)

            elif isinstance(value, list):

                self._mqtt.publish(
                    topic,
                    json.dumps(value),
                )

            else:

                self._mqtt.publish(topic, value)

                self._publish_discovery(topic, value)

    def _publish_discovery(self, topic: str, value):

        #
        # Publish Home Assistant discovery only once
        #

        if topic in self._discovered:
            return

        self._discovered.add(topic)

        unit = None
        device_class = None
        state_class = "measurement"

        lower = topic.lower()

        if "temp" in lower:
            unit = "°C"
            device_class = "temperature"

        elif "kwh" in lower:
            unit = "kWh"
            device_class = "energy"

        elif "m3" in lower:
            unit = "m³"

        elif "price" in lower:
            unit = "DKK"

        self._discovery.publish_sensor(
            object_id=topic.replace("/", "_"),
            name=topic.replace("/", " ").title(),
            state_topic=f"{self._mqtt._cfg.topic}/{topic}",
            device_class=device_class,
            state_class=state_class,
            unit=unit,
        )