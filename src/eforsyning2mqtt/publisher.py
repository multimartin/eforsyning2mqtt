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

                import json
                import logging
                from typing import Any, Dict

                from eforsyning2mqtt.discovery import DiscoveryPublisher
                from eforsyning2mqtt.measurement import Measurement
                from eforsyning2mqtt.sensors import SENSORS


                class Publisher:
                    """Publish measurement data to MQTT topics and optionally publish discovery.

                    The publisher serializes lists to JSON and provides summary topics like
                    ``<topic>/count`` and ``<topic>/last`` for lists.
                    """

                    def __init__(self, mqtt: Any) -> None:
                        self._mqtt = mqtt
                        self._logger = logging.getLogger("eforsyning2mqtt")
                        self._discovery = DiscoveryPublisher(mqtt=mqtt, base_topic=mqtt._cfg.topic)
                        self._discovered: set[str] = set()

                    def publish(self, measurement: Measurement) -> None:
                        """Publish an entire measurement object to MQTT."""
                        self._publish_dict(measurement.as_dict())

                    def _publish_dict(self, data: Dict[str, Any], prefix: str = "") -> None:
                        for key, value in data.items():
                            topic = f"{prefix}/{key}" if prefix else key

                            if isinstance(value, dict):
                                self._publish_dict(value, topic)
                                continue

                            if isinstance(value, list):
                                # publish list as JSON and provide count/last helpers
                                self._mqtt.publish(topic, json.dumps(value))
                                self._mqtt.publish(f"{topic}/count", len(value))

                                if value:
                                    self._mqtt.publish(f"{topic}/last", json.dumps(value[-1]))
                                continue

                            # publish primitive value
                            self._mqtt.publish(topic, value)

                            # attempt to publish discovery for this topic; log exceptions
                            try:
                                self._publish_discovery(topic)
                            except (KeyError, TypeError, ValueError, OSError) as exc:
                                self._logger.exception("Discovery failed for topic %s: %s", topic, exc)

                    def _publish_discovery(self, topic: str) -> None:
                        """Publish Home Assistant discovery information for a topic once.

                        The SENSORS mapping can provide metadata (name, device_class, state_class,
                        unit, icon). If no entry exists, a sensible default is used.
                        """
                        if topic in self._discovered:
                            return

                        self._discovered.add(topic)

                        sensor = SENSORS.get(topic, {"name": topic, "state_class": "measurement"})

                        self._discovery.publish_sensor(
                            object_id=topic.replace("/", "_"),
                            name=sensor["name"],
                            state_topic=f"{self._mqtt._cfg.topic}/{topic}",
                            device_class=sensor.get("device_class"),
                            state_class=sensor.get("state_class"),
                            unit=sensor.get("unit"),
                            icon=sensor.get("icon"),
                        )