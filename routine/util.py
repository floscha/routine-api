import random
import string
from datetime import datetime, timezone


def _create_id() -> str:
    return "task:" + "".join(random.sample(string.ascii_letters + string.digits, 21))


def _get_now_as_str() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S%z")
