import logging

from eforsyning2mqtt.config import load_config
from eforsyning2mqtt.logging_config import configure_logging
from eforsyning2mqtt.version import VERSION


def main():

    configure_logging()

    root = logging.getLogger()

    logger = logging.getLogger("eforsyning2mqtt")

    logger.info("Root handlers: %d", len(root.handlers))

    for h in root.handlers:


    logger.info("Handler: %s", h)

    logger = logging.getLogger("eforsyning2mqtt")

    cfg = load_config()

    logger.info("Username=%s (%s)", cfg.eforsyning.username, type(cfg.eforsyning.username).__name__,)
    logger.info("SupplierID=%s", cfg.eforsyning.supplier_id)

    from eforsyning2mqtt.client import EForsyningClient

    logger.info("--------------------------------")
    logger.info("eforsyning2mqtt %s", VERSION)
    logger.info("--------------------------------")

    logger.info("Supplier ID : %s", cfg.eforsyning.supplier_id)

    logger.info("MQTT host: %s", cfg.mqtt.host)

    logger.info(
        "Polling : %d minutes",
        cfg.polling.interval_minutes,
    )

    client = EForsyningClient(cfg)

    logger.info("Authenticating...")

    ok = client.authenticate()

    logger.info("Authenticated = %s", ok)

    logger.info("Getting user...")

    user = client.get_user()

    logger.info("User:")
    logger.info(user)

    logger.info("Getting installations...")

    installations = client.get_installations()

    logger.info(installations)

    logger.info("Getting latest year...")

    year = client.get_latest_year()

    logger.info("Latest year = %s", year)

if __name__ == "__main__":
    main()
