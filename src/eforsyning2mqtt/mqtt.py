import logging
import socket
from typing import Any

import paho.mqtt.client as mqtt


class MQTTClient:
    """Simple wrapper around paho.mqtt.client to publish messages.

    Parameters
    ----------
    cfg:
        Configuration object exposing ``host``, ``port``, ``username``, ``password`` and ``topic``.
    """

    def __init__(self, cfg: Any) -> None:

        self._cfg = cfg

        self._logger = logging.getLogger("eforsyning2mqtt")

        self._closed = False

        self._client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"eforsyning2mqtt-{socket.gethostname()}",
        )

        if cfg.username:
            self._client.username_pw_set(cfg.username, cfg.password)

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect

        self._client.reconnect_delay_set(min_delay=1, max_delay=60)

        self._client.will_set(f"{cfg.topic}/status", "offline", qos=1, retain=True)

        self._client.connect(cfg.host, cfg.port, keepalive=60)

        self._client.loop_start()

 
    def publish(self, topic: str, payload: Any) -> None:

        full_topic = f"{self._cfg.topic}/{topic}"

        info = self._client.publish(
            full_topic,
            str(payload),
            qos=1,
            retain=True,
        )

        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            self._logger.warning(
                "Failed to publish %s (rc=%s)",
                full_topic,
                info.rc,
            )
 
    def close(self) -> None:

        if self._closed:
            return

        self._closed = True

        try:
            self.publish("status", "offline")
        except (OSError, RuntimeError) as exc:
            # Publishing status failed; log and continue shutdown
            self._logger.exception("Failed to publish offline status: %s", exc)

        self._client.loop_stop()

        self._client.disconnect()

    def _on_connect(self, client: mqtt.Client, userdata: Any, flags: Any, reason_code: int, properties: Any) -> None:

        self._logger.info("Connected to MQTT broker")

        self.publish("status", "online")

    def _on_disconnect(self, client: mqtt.Client, userdata: Any, flags: Any, reason_code: int, properties: Any) -> None:

        if not self._closed:
            self._logger.warning("Disconnected from MQTT broker (%s)", reason_code)