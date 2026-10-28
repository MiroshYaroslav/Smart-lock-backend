from datetime import datetime, timezone

def get_time() -> datetime:
    return datetime.now(timezone.utc)