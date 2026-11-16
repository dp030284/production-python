import unittest
from unittest.mock import MagicMock, call, patch

from fxrates.exceptions import RateServiceTimeout, RateServiceUnavailable
from fxrates.rate_fetcher import get_historical_rate


class HistoricalRateTests(unittest.TestCase):
    @patch("fxrates.retry.time.sleep")
    @patch(
        "fxrates.rate_fetcher.fetch_historical_rate_from_service",
        side_effect=[
            RateServiceTimeout("temporary timeout"),
            RateServiceUnavailable("temporarily unavailable"),
            0.92,
        ],
    )
    def test_retries_transient_errors_for_requested_date(
        self, fetch_historical_rate: MagicMock, _sleep: MagicMock
    ) -> None:
        rate = get_historical_rate("USD/EUR", "2026-01-15")

        self.assertEqual(rate, 0.92)
        fetch_historical_rate.assert_has_calls(
            [call("USD/EUR", "2026-01-15")] * 3
        )


if __name__ == "__main__":
    unittest.main()
