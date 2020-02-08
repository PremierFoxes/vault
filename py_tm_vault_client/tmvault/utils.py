import logging
from datetime import datetime
from dateutil import parser


def get_logger(name):
    logger = logging.getLogger(name)
    return logger


def timestamp_now() -> str:
    return datetime_to_str(datetime.utcnow())


def datetime_to_str(dt: datetime) -> str:
    return dt.isoformat() + "Z" if dt is not None else ""


def datetime_from_timestamp_iso_string(iso_string: str) -> datetime:
    return (parser.parse(iso_string)
            if iso_string
            else None)
