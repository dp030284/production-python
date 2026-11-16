from fxrates.fx_client import fetch_historical_rate as fetch_historical_rate_from_service
from fxrates.fx_client import fetch_rate
from fxrates.retry import call_with_retry


def get_rate(pair: str) -> float:
    return call_with_retry(lambda: fetch_rate(pair))


def get_historical_rate(pair: str, date: str) -> float:
    return call_with_retry(lambda: fetch_historical_rate_from_service(pair, date))
