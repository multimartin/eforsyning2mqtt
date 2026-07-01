import logging


def configure_logging() -> None:

    root = logging.getLogger()

    print("===== ROOT LOGGER =====")
    print(f"Handlers before: {len(root.handlers)}")

    for i, handler in enumerate(root.handlers):
        print(f"Handler {i}: {handler!r}")

    if not root.handlers:
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
        )

    print(f"Handlers after: {len(root.handlers)}")

    for i, handler in enumerate(root.handlers):
        print(f"Handler {i}: {handler!r}")

    print("=======================")