import logging

from eforsyning2mqtt.config import load_config
from eforsyning2mqtt.logging_config import configure_logging
from eforsyning2mqtt.service import EForsyningService
from eforsyning2mqtt.version import VERSION


def main() -> None:

    configure_logging()

    logger = logging.getLogger("eforsyning2mqtt")

    logger.info("--------------------------------")
    logger.info("eforsyning2mqtt %s", VERSION)
    logger.info("--------------------------------")

    config = load_config()

    service = EForsyningService(config)

    try:

        service.run()

    except KeyboardInterrupt:

        logger.info("Stopping...")

    finally:

        service.stop()

        logger.info("Shutdown complete")


if __name__ == "__main__":
    main()