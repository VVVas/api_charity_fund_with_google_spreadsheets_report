from datetime import datetime, timezone


def aware_utcnow():
    """datetime.utcnow deprecated."""
    return datetime.now(timezone.utc)
