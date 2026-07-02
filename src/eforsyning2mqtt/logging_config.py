import logging


def configure_logging(level: str = "INFO") -> None:

    numeric_level = getattr(
        logging,
        level.upper(),
        logging.INFO,
    )

    logging.basicConfig(
        level=numeric_level,
        format="%(asctime)s %(levelname)s %(message)s",
    )

    logging.getLogger(__name__).info(
        "Logging initialized (%s)",
        logging.getLevelName(numeric_level),
    )