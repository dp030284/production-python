import pytest
from pydantic import ValidationError

from signupflow.models import SignupRecord


def signup_record(**overrides):
    return SignupRecord(
        email="customer@example.com",
        plan="free",
        signup_date="2026-11-14",
        **overrides,
    )


@pytest.mark.parametrize(
    ("referral_code", "referral_bonus_percent"),
    [
        ("FRIEND", 0),
        ("FRIEND", 15.5),
        ("FRIEND", 100),
        ("REF123", 0),
        ("REF123", 15.5),
        ("REF123", 100),
    ],
)
def test_referral_code_accepts_bonus_in_range(
    referral_code, referral_bonus_percent
):
    record = signup_record(
        referral_code=referral_code,
        referral_bonus_percent=referral_bonus_percent,
    )

    assert record.referral_code == referral_code
    assert record.referral_bonus_percent == referral_bonus_percent


def test_record_without_referral_fields_is_valid():
    record = signup_record()

    assert record.referral_code is None
    assert record.referral_bonus_percent is None


@pytest.mark.parametrize(
    "overrides",
    [
        {"referral_code": "FRIEND"},
        {"referral_code": "FRIEND", "referral_bonus_percent": None},
        {"referral_bonus_percent": 10},
        {"referral_bonus_percent": None},
        {"referral_code": "FRIEND", "referral_bonus_percent": -0.1},
        {"referral_code": "FRIEND", "referral_bonus_percent": 100.1},
        {"referral_code": "FRIEND", "referral_bonus_percent": "10"},
        {"referral_code": "FRIEND", "referral_bonus_percent": True},
        {"referral_code": None, "referral_bonus_percent": 0},
        {"referral_code": None, "referral_bonus_percent": 100},
    ],
)
def test_invalid_referral_bonus_combinations_are_rejected(overrides):
    with pytest.raises(ValidationError):
        signup_record(**overrides)
