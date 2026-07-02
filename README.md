# eforsyning2mqtt

A lightweight Docker application that retrieves meter data from **eForsyning.dk** and publishes it to an MQTT broker for use with home automation systems.

The application is designed to be simple, reliable and independent of any specific home automation platform.

---

## Features

* Docker based
* MQTT publishing
* Home Assistant MQTT Discovery
* OpenHAB compatible
* Configured using environment variables
* Lightweight and low resource usage
* No cloud service required
* Automatic polling

---

## Architecture

```
             eForsyning.dk
                    │
                 HTTPS
                    │
           eforsyning2mqtt
                    │
                  MQTT
                    │
    ┌───────────────┼────────────────┐
    │               │                │
Home Assistant   OpenHAB        Other MQTT clients
```

---

## Requirements

* Docker
* Docker Compose
* MQTT broker
* eForsyning account

---

## Installation

Clone the repository

```bash
git clone https://github.com/multimartin/eforsyning2mqtt.git
cd eforsyning2mqtt
```

Create your local configuration

```bash
cp .env.example .env
```

Edit `.env`

```text
EFORSYNING_USERNAME=your_username
EFORSYNING_PASSWORD=your_password
EFORSYNING_SUPPLIER_ID=123

MQTT_HOST=192.168.1.10
MQTT_PORT=1883
MQTT_USERNAME=
MQTT_PASSWORD=
MQTT_TOPIC=eforsyning

POLLING_INTERVAL=30
```

Start the container

```bash
docker compose up -d
```

---

## MQTT Topics

Example

```
eforsyning/
├── status
├── temp-forward
├── temp-return
├── energy-used
├── energy-end
├── water-used
├── water-end
└── billing/
```

All topics are published as retained MQTT messages.

---

## Home Assistant

The application publishes MQTT Discovery messages automatically.

No manual MQTT sensor configuration is required.

---

## OpenHAB

OpenHAB can subscribe directly to the published MQTT topics.

No special configuration is required.

---

## Configuration

Configuration is provided through environment variables.

See `.env.example` for all available settings.

---

## Acknowledgements

The communication with the eForsyning service is based on the excellent reverse engineering work and Home Assistant integration created by Kristian Poppel.

Original project:

https://github.com/kpoppel/homeassistant-eforsyning

This project adapts that work into an independent standalone MQTT gateway.

---

## Disclaimer

This is an independent open source project.

It is **not affiliated with, endorsed by or supported by eForsyning.dk or any utility company.**

---

## Contributing

Bug reports, feature requests and pull requests are welcome.

---

## License

This project is licensed under the MIT License.
