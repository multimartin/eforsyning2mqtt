import json
from typing import Optional


class DiscoveryPublisher:
    """Publish Home Assistant discovery messages over MQTT.

    Parameters
    ----------
    mqtt:
        MQTT client wrapper exposing a ``publish(topic, payload)`` method.
    base_topic:
        Base topic used by the integration (not currently used directly).
    """

    def __init__(self, mqtt, base_topic: str):
        self._mqtt = mqtt
        self._base_topic = base_topic

    def publish_sensor(
        self,
        object_id: str,
        name: str,
        state_topic: str,
        device_class: Optional[str] = None,
        state_class: Optional[str] = None,
        unit: Optional[str] = None,
        icon: Optional[str] = None,
    ) -> None:
        """Publish a single sensor discovery payload."""

        payload = {
            "name": name,
            "unique_id": f"eforsyning_{object_id}",
            "state_topic": state_topic,
            "device": {
                "identifiers": ["eforsyning"],
                "name": "eForsyning",
                "manufacturer": "eForsyning2MQTT",
                "model": "Gateway",
            },
        }

        if device_class:
            payload["device_class"] = device_class

        if state_class:
            payload["state_class"] = state_class

        if unit:
            payload["unit_of_measurement"] = unit

        if icon:
            payload["icon"] = icon

        topic = f"homeassistant/sensor/eforsyning/{object_id}/config"

        self._mqtt.publish(topic, json.dumps(payload))