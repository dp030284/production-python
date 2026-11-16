class IngestionError(Exception):
    """Base class for anything that can go wrong ingesting a record."""


class UpstreamTimeout(IngestionError):
    """The API didn't respond in time. Retryable."""


class UpstreamRateLimited(IngestionError):
    """The API returned 429. Retryable, after waiting."""


class RecordValidationError(IngestionError):
    """A record failed validation. Not retryable - the data is wrong."""