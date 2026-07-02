import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure module-level logging for the application.

    The default logger used by the project is ``eforsyning2mqtt``.
    """

    numeric_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(level=numeric_level, format="%(asctime)s %(levelname)s %(message)s")

    logging.getLogger("eforsyning2mqtt").info("Logging initialized: %s", logging.getLevelName(numeric_level))