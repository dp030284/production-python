"""The data boundary for signup records.

A raw signup record arrives as an untyped dict - from a webhook, a CSV,
an API response, it doesn't matter. Before any of that data is trusted
anywhere else in this codebase, it passes through this one model. If a
record is malformed, it fails right here, with a specific error naming
the exact field that's wrong - not three functions later, in a place
that has nothing to do with where the bad data actually came from.
"""

from datetime import date
from typing import Annotated, Literal

from pydantic import BaseModel, Field, StrictFloat, StrictInt, model_validator


class SignupRecord(BaseModel):
    email: str
    plan: Literal["free", "pro", "enterprise"]
    signup_date: date
    trial_days: int = 14
    referral_code: str | None = None
    referral_bonus_percent: Annotated[
        StrictInt | StrictFloat, Field(ge=0, le=100)
    ] | None = None

    @model_validator(mode="after")
    def validate_referral_bonus(self) -> "SignupRecord":
        bonus_was_provided = "referral_bonus_percent" in self.model_fields_set
        if self.referral_code is not None:
            if not bonus_was_provided or self.referral_bonus_percent is None:
                raise ValueError(
                    "referral_bonus_percent is required when referral_code is set"
                )
        elif bonus_was_provided:
            raise ValueError(
                "referral_bonus_percent cannot be provided without referral_code"
            )
        return self
