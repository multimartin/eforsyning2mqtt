import json
import logging

from eforsyning2mqtt.discovery import DiscoveryPublisher
from eforsyning2mqtt.measurement import Measurement
from eforsyning2mqtt.sensors import SENSORS


class Publisher:

    def __init__(self, mqtt):

        self._mqtt = mqtt

        self._logger = logging.getLogger("eforsyning2mqtt")

        self._discovery = DiscoveryPublisher(
            mqtt=mqtt,
            base_topic=mqtt._cfg.topic,
        )

        self._discovered = set()

    def publish(self, measurement: Measurement):

        self._publish_dict(measurement.as_dict())

    def _publish_dict(self, data: dict, prefix: str = ""):

        for key, value in data.items():

            topic = f"{prefix}/{key}" if prefix else key

            if isinstance(value, dict):

                self._publish_dict(value, topic)

                continue

            if isinstance(value, list):

                self._mqtt.publish(
                    topic,
                    json.dumps(value),
                )

                self._mqtt.publish(
                    f"{topic}/count",
                    len(value),
                )

                if value:

                    self._mqtt.publish(
                        f"{topic}/last",
                        json.dumps(value[-1]),
                    )

                continue

            self._mqtt.publish(topic, value)

            try:
                self._publish_discovery(topic)
            except (KeyError, TypeError, ValueError, OSError) as exc:
                # Log expected discovery/publish related errors with stack trace
                self._logger.exception(
                    "Discovery failed for topic %s: %s",
                    topic,
                    exc,
                )

    def _publish_discovery(self, topic: str):

        if topic in self._discovered:
            return

        self._discovered.add(topic)

        sensor = SENSORS.get(
            topic,
            {
                "name": topic,
                "state_class": "measurement",
            },
        )

        self._discovery.publish_sensor(
            object_id=topic.replace("/", "_"),
            name=sensor["name"],
            state_topic=f"{self._mqtt._cfg.topic}/{topic}",
            device_class=sensor.get("device_class"),
            state_class=sensor.get("state_class"),
            unit=sensor.get("unit"),
            icon=sensor.get("icon"),
        )