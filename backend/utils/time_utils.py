from datetime import datetime


def current_timestamp() -> str:
    """
    Returns timestamp suitable for filenames.
    """

    return datetime.now().strftime("%Y%m%d_%H%M%S")


def readable_time() -> str:
    """
    Human-readable timestamp.
    """

    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
