import logging


def setup_logging():
    logging.basicConfig(
        format="[%(levelname)s|%(module)s:%(lineno)d] %(asctime)s %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("ollama").setLevel(logging.WARNING)
