import logging
from pathlib import Path


def setup_logging(log_file="logs/error.log"):
    """
    Configure application error logging.
    """

    log_path = Path(log_file)

    log_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    logging.basicConfig(
        filename=log_path,
        level=logging.ERROR,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )


def log_error(error):
    """
    Write an exception to the error log.
    """

    logging.error(
        "%s: %s",
        type(error).__name__,
        str(error)
    )