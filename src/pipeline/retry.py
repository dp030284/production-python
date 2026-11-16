import random
import time
from typing import Callable, TypeVar

from fxrates.exceptions import RateServiceTimeout, RateServiceUnavailable

T = TypeVar("T")

# Only these two are worth retrying. Anything else - like
# InvalidCurrencyPairError - is a permanent failure, and isn't listed
# here on purpose, so it propagates immediately instead of being caught.
RETRYABLE_EXCEPTIONS = (UpstreamTimeout, UpstreamRateLimited)


def call_with_retry(
    func: Callable[[], T],
    *,
    max_attempts: int = 5,
    base_delay: float = 0.05,
    max_delay: float = 2.0,
) -> T:
    attempt = 0
    while True:
        attempt += 1
        try:
            return func()
        except RETRYABLE_EXCEPTIONS as e:
            if attempt >= max_attempts:
                raise
            backoff = min(max_delay, base_delay * (2 ** (attempt - 1)))
            delay = random.uniform(0, backoff)
            print(f"    attempt {attempt} failed ({e}); retrying in {delay:.3f}s")
            time.sleep(delay)