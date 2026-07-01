import logging

import paho.mqtt.client as mqtt


class MQTTClient:

    def __init__(self, cfg):

        self._cfg = cfg

        self._logger = logging.getLogger("eforsyning2mqtt")

        self._closed = False

        self._client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        if cfg.username:
            self._client.username_pw_set(
                cfg.username,
                cfg.password,
            )

        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect

        self._client.will_set(
            f"{cfg.topic}/status",
            "offline",
            qos=1,
            retain=True,
        )

        self._client.connect(
            cfg.host,
            cfg.port,
            keepalive=60,
        )

        self._client.loop_start()

    def publish(self, topic: str, payload):

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

    def close(self):

        if self._closed:
            return

        self._closed = True

        try:
            self.publish("status", "offline")
        except Exception:
            pass

        self._client.loop_stop()

        self._client.disconnect()

    def _on_connect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties,
    ):

        self._logger.info("Connected to MQTT broker")

        self.publish("status", "online")

    def _on_disconnect(
        self,
        client,
        userdata,
        flags,
        reason_code,
        properties,
    ):

        if not self._closed:

            self._logger.warning(
                "Disconnected from MQTT broker (%s)",
                reason_code,
            )