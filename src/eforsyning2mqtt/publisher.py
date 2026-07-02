"""Publisher module for eforsyning2mqtt.

This module implements a single ``Publisher`` class which exposes the same
public API as the original implementation: ``Publisher(mqtt)`` and
``publish(measurement)``. It recursively publishes nested dictionaries to
MQTT topics, serializes lists as JSON and publishes helper topics
``<topic>/count`` and ``<topic>/last``. Home Assistant discovery is published
once per topic via ``DiscoveryPublisher``.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from eforsyning2mqtt.discovery import DiscoveryPublisher
from eforsyning2mqtt.measurement import Measurement
from eforsyning2mqtt.sensors import SENSORS


_LOGGER = logging.getLogger("eforsyning2mqtt")


class Publisher:
    """Publish measurement data and discovery payloads to MQTT.

    Public surface kept minimal and compatible with the previous API.
    """

    def __init__(self, mqtt: Any) -> None:
        self._mqtt = mqtt
        self._discovery = DiscoveryPublisher(mqtt=mqtt, base_topic=mqtt._cfg.topic)
        self._published_discovery: set[str] = set()

    def publish(self, measurement: Measurement) -> None:
        """Publish a Measurement to MQTT.

        The measurement object must provide an ``as_dict()`` method returning
        a nested mapping of keys to values. This method does not return a
        value; errors are logged.
        """
        try:
            data = measurement.as_dict()
        except Exception:
            _LOGGER.exception("Failed to obtain measurement dict from %r", measurement)
            return

        self._publish_map(data)

    def _publish_map(self, data: Dict[str, Any], prefix: str = "") -> None:
        """Recursively publish mapping entries to MQTT topics.

        - Nested dictionaries are traversed and published under ``prefix/key``.
        - Lists are serialized as JSON and ``<topic>/count`` and ``<topic>/last``
          are published.
        - Primitive values are published directly.
        - Discovery is attempted once per topic.
        """
        for key, value in data.items():
            topic = f"{prefix}/{key}" if prefix else key

            # Nested mapping -> recurse
            if isinstance(value, dict):
                self._publish_map(value, topic)
                continue

            # Lists -> JSON payload + helpers
            if isinstance(value, list):
                payload = self._serialize(value)
                try:
                    self._mqtt.publish(topic, payload)
                except Exception:
                    _LOGGER.exception("Failed to publish list payload for %s", topic)

                try:
                    self._mqtt.publish(f"{topic}/count", len(value))
                except Exception:
                    _LOGGER.exception("Failed to publish count for %s", topic)

                if value:
                    last_payload = self._serialize(value[-1])
                    try:
                        self._mqtt.publish(f"{topic}/last", last_payload)
                    except Exception:
                        _LOGGER.exception("Failed to publish last element for %s", topic)

                self._ensure_discovery(topic)
                continue

            # Primitive -> publish directly
            try:
                self._mqtt.publish(topic, value)
            except Exception:
                _LOGGER.exception("Failed to publish value for %s", topic)

            self._ensure_discovery(topic)

    def _serialize(self, obj: Any) -> str:
        """Serialize an object to JSON safely, falling back to str()."""
        try:
            return json.dumps(obj)
        except (TypeError, ValueError):
            return json.dumps(str(obj))

    def _ensure_discovery(self, topic: str) -> None:
        """Publish discovery for `topic` only once.

        Uses the global `SENSORS` mapping for metadata. Exceptions during
        discovery publishing are logged but do not raise.
        """
        if topic in self._published_discovery:
            return

        self._published_discovery.add(topic)

        sensor = SENSORS.get(topic, {"name": topic, "state_class": "measurement"})

        try:
            self._discovery.publish_sensor(
                object_id=topic.replace("/", "_"),
                name=sensor.get("name", topic),
                state_topic=f"{self._mqtt._cfg.topic}/{topic}",
                device_class=sensor.get("device_class"),
                state_class=sensor.get("state_class"),
                unit=sensor.get("unit"),
                icon=sensor.get("icon"),
            )
        except Exception:
            _LOGGER.exception("Failed to publish discovery for %s", topic)
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

            except Exception:

                self._logger.exception(
                    "Discovery failed for topic %s",
                    topic,
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