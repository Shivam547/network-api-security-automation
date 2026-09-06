import time
from collections import defaultdict
from threading import Lock


MAX_REQUESTS = 5
WINDOW_SECONDS = 10


class RateLimiter:

    def __init__(
        self,
        max_requests=MAX_REQUESTS,
        window_seconds=WINDOW_SECONDS
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds

        self.requests = defaultdict(list)

        # Protect shared state when multiple threads
        # access the rate limiter.
        self.lock = Lock()

    def is_allowed(self, client_id):

        now = time.time()

        with self.lock:

            timestamps = self.requests[client_id]

            # Remove timestamps outside the window
            timestamps[:] = [
                timestamp
                for timestamp in timestamps
                if now - timestamp < self.window_seconds
            ]

            if len(timestamps) >= self.max_requests:
                retry_after = int(
                    self.window_seconds -
                    (now - timestamps[0])
                )

                return False, max(1, retry_after)

            timestamps.append(now)

            return True, 0