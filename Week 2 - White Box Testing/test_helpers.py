"""
test_helpers.py - White-box tests for helpers.py (Project Week 2).

Units under test
----------------
  compute_urgency             helpers.py lines 12-39   V(G) = 5
  completed_in_last_n_days    helpers.py lines 61-75   V(G) = 5
  is_valid_password           helpers.py lines 42-49   V(G) = 2  (optional extra)
  is_valid_username           helpers.py lines 52-58   (keeps the coverage report clean)

How the tests are organised
---------------------------
  * U1-U4 and C1-C5 are the white-box tests: together they reach every
    statement, every branch, and every outcome of the compound condition on
    helpers.py line 75.
  * U5-U7, C6-C8 and P2 are spec-based boundary tests. They are the ones that
    expose defects, because 100% coverage does not prove the code is correct.
  * Tests that currently fail because of a defect are marked
    xfail(strict=True). The suite stays green, the defect is documented, and
    the test fails loudly (XPASS) once someone fixes the bug.

Run
---
  pytest -v -rx
  pytest --cov=helpers --cov-branch --cov-report=term-missing
"""

from datetime import date, datetime, timedelta

import pytest

from helpers import (
    completed_in_last_n_days,
    compute_urgency,
    is_valid_password,
    is_valid_username,
)

# Fixed reference points so no test depends on the real clock
# (except C2, which deliberately leaves `now` unset).
TODAY = date(2026, 6, 15)
NOW = datetime(2026, 6, 15, 12, 0, 0)
FMT = "%Y-%m-%d %H:%M:%S"


def ago(**delta):
    """Timestamp string that is `delta` before NOW (negative values = future)."""
    return (NOW - timedelta(**delta)).strftime(FMT)


# ======================================================================
# compute_urgency
# Decisions: L26 today is None | L28 not due_date_str
#            L33 due <= today  | L37 delta_days <= 2
# ======================================================================

@pytest.mark.parametrize("empty_value", [None, ""])
def test_u1_no_due_date_returns_no_due_date(empty_value):
    """U1: falsy due date, `today` omitted.
    Covers: today-is-None True (L27 runs), not-due_date_str True (L29)."""
    assert compute_urgency(empty_value) == "No due date"


def test_u2_past_date_is_overdue():
    """U2: Covers: today-is-None False, not-due_date_str False, due <= today True."""
    assert compute_urgency("2026-06-14", today=TODAY) == "Overdue"


def test_u3_one_day_away_is_due_soon():
    """U3: Covers: due <= today False, delta_days <= 2 True."""
    assert compute_urgency("2026-06-16", today=TODAY) == "Due Soon"


def test_u4_three_days_away_is_upcoming():
    """U4: Covers: delta_days <= 2 False. Also the 2/3 boundary (upper side)."""
    assert compute_urgency("2026-06-18", today=TODAY) == "Upcoming"


@pytest.mark.xfail(
    strict=True,
    reason="DEFECT helpers.py L33: `due <= today` classifies today as Overdue; "
           "spec says 'Due Today', and no code path ever returns that label.",
)
def test_u5_due_today_returns_due_today():
    """U5: boundary due == today. Spec: 'Due Today'."""
    assert compute_urgency("2026-06-15", today=TODAY) == "Due Today"


def test_u6_two_days_away_is_due_soon():
    """U6: boundary delta == 2 (lower side of the 2/3 boundary)."""
    assert compute_urgency("2026-06-17", today=TODAY) == "Due Soon"


def test_u6b_month_boundary_is_handled():
    """U6b: date arithmetic across a month end (2026-06-30 -> 2026-07-02)."""
    assert compute_urgency("2026-07-02", today=date(2026, 6, 30)) == "Due Soon"


def test_u7_malformed_date_raises_value_error():
    """U7: error path. The spec is silent; current behaviour is an uncaught
    ValueError. app.py stores due_date unvalidated, so this can surface as a 500."""
    with pytest.raises(ValueError):
        compute_urgency("tomorrow", today=TODAY)


def test_u8_non_string_due_date_raises_type_error():
    """U8: error path. A non-string, truthy due date raises TypeError."""
    with pytest.raises(TypeError):
        compute_urgency(123, today=TODAY)


# ======================================================================
# completed_in_last_n_days   (n = 7 unless stated)
# Decisions: L69 not completed_at_str | L71 now is None
#            L75 (age.total_seconds() > 0) AND (age.days < n)
# ======================================================================

@pytest.mark.parametrize("empty_value", [None, ""])
def test_c1_not_completed_returns_false(empty_value):
    """C1: falsy input. Covers: not-completed_at_str True (L70)."""
    assert completed_in_last_n_days(empty_value, now=NOW) is False


def test_c2_now_omitted_uses_real_clock():
    """C2: `now` not supplied. Covers: now-is-None True (L72 runs).
    Uses the real clock, so the timestamp is built relative to it."""
    one_day_ago = (datetime.now() - timedelta(days=1)).strftime(FMT)
    assert completed_in_last_n_days(one_day_ago) is True


def test_c3_completed_yesterday_counts():
    """C3: L75 condition A True, condition B True."""
    assert completed_in_last_n_days(ago(days=1), now=NOW) is True


def test_c4_completed_eight_days_ago_does_not_count():
    """C4: L75 condition A True, condition B False (age.days < n fails)."""
    assert completed_in_last_n_days(ago(days=8), now=NOW) is False


def test_c5_future_timestamp_does_not_count():
    """C5: L75 condition A False (short-circuits; B is never evaluated)."""
    assert completed_in_last_n_days(ago(seconds=-1), now=NOW) is False


@pytest.mark.xfail(
    strict=True,
    reason="DEFECT helpers.py L75: `age.days < n` excludes exactly N days ago; "
           "spec says the window is inclusive of exactly N days.",
)
def test_c6_exactly_seven_days_ago_counts():
    """C6: boundary age == 7 days. Spec: inclusive, so True."""
    assert completed_in_last_n_days(ago(days=7), now=NOW) is True


def test_c7_just_inside_window_counts():
    """C7: boundary 6 d 23 h 59 m 59 s."""
    assert completed_in_last_n_days(ago(days=6, hours=23, minutes=59, seconds=59), now=NOW) is True


def test_c7b_just_outside_window_does_not_count():
    """C7b: boundary 7 d + 1 s is outside the window."""
    assert completed_in_last_n_days(ago(days=7, seconds=1), now=NOW) is False


@pytest.mark.xfail(
    strict=True,
    reason="PROBABLE DEFECT helpers.py L75: `total_seconds() > 0` excludes a task "
           "completed at exactly `now`. Spec is unclear, but 'within the last N days' "
           "should include a task completed this very second.",
)
def test_c8_completed_at_exactly_now_counts():
    """C8: boundary age == 0 s."""
    assert completed_in_last_n_days(ago(seconds=0), now=NOW) is True


def test_c9_custom_window_size_is_respected():
    """C9: the `n` parameter. 12 hours ago is inside a 1-day window, 2 days is not."""
    assert completed_in_last_n_days(ago(hours=12), n=1, now=NOW) is True
    assert completed_in_last_n_days(ago(days=2), n=1, now=NOW) is False


def test_c10_malformed_timestamp_raises_value_error():
    """C10: error path. Uncaught ValueError for a bad timestamp format."""
    with pytest.raises(ValueError):
        completed_in_last_n_days("not-a-date", now=NOW)


# ======================================================================
# is_valid_password   Spec: at least 8 characters
# ======================================================================

@pytest.mark.parametrize("value", [None, 12345678, ["abcdefghi"]])
def test_p1_non_string_password_is_invalid(value):
    """P1: isinstance branch True (non-strings are rejected)."""
    assert is_valid_password(value) is False


@pytest.mark.xfail(
    strict=True,
    reason="DEFECT helpers.py L49: `len(password) > 8` rejects 8-character "
           "passwords; spec says at least 8.",
)
def test_p2_eight_character_password_is_valid():
    """P2: boundary len == 8. Spec: valid."""
    assert is_valid_password("abcdefgh") is True


def test_p3_nine_character_password_is_valid():
    """P3: isinstance branch False, length above the boundary."""
    assert is_valid_password("abcdefghi") is True


@pytest.mark.parametrize("value", ["abcdefg", ""])
def test_p4_short_password_is_invalid(value):
    """P4: below the boundary (7 characters, and empty)."""
    assert is_valid_password(value) is False


# ======================================================================
# is_valid_username   Spec: 3-20 chars, letters/numbers/underscore only
# ======================================================================

@pytest.mark.parametrize(
    "username, expected",
    [
        (None, False),          # non-string: isinstance branch
        (123, False),           # non-string
        ("", False),            # empty
        ("ab", False),          # 2 chars: just below lower bound
        ("abc", True),          # 3 chars: lower bound
        ("a" * 20, True),       # 20 chars: upper bound
        ("a" * 21, False),      # 21 chars: just above upper bound
        ("abc123", True),       # letters + digits
        ("a_b", True),          # underscore allowed
        ("a b", False),         # space rejected
        ("a-b", False),         # hyphen rejected
        ("a@b", False),         # symbol rejected
    ],
)
def test_username_partitions_and_boundaries(username, expected):
    assert is_valid_username(username) is expected


def test_username_non_ascii_letter_currently_accepted():
    """Documents current behaviour: str.isalnum() is Unicode-aware, so 'usér' passes.
    The spec says 'letters', which is ambiguous; this is a discussion point, not a
    confirmed defect."""
    assert is_valid_username("us\u00e9r") is True
