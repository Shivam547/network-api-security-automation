from datetime import datetime, timedelta, timezone

LOCK_DURATION_SECONDS = 30


def get_current_time():
    return datetime.now(timezone.utc).replace(tzinfo=None)


def get_lock_expiry():
    return (
        get_current_time()
        + timedelta(seconds=LOCK_DURATION_SECONDS)
    )