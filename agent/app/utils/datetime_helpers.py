"""
Date and time utility functions.
"""
from datetime import datetime, timedelta
from typing import List, Optional
import pytz
import pendulum


def get_utc_now() -> datetime:
    """Get current UTC datetime."""
    return datetime.utcnow()


def get_local_now(timezone: str = "UTC") -> datetime:
    """
    Get current datetime in specified timezone.

    Args:
        timezone: Timezone string (e.g., 'America/New_York')

    Returns:
        Current datetime in specified timezone
    """
    tz = pytz.timezone(timezone)
    return datetime.now(tz)


def convert_to_utc(dt: datetime, from_timezone: str) -> datetime:
    """
    Convert a datetime from a specific timezone to UTC.

    Args:
        dt: Datetime object
        from_timezone: Source timezone string

    Returns:
        UTC datetime
    """
    if dt.tzinfo is None:
        # Assume it's in the from_timezone
        tz = pytz.timezone(from_timezone)
        dt = tz.localize(dt)

    return dt.astimezone(pytz.UTC)


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    Format datetime as string.

    Args:
        dt: Datetime object
        format_str: Format string

    Returns:
        Formatted datetime string
    """
    return dt.strftime(format_str)


def parse_datetime(dt_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    """
    Parse datetime string.

    Args:
        dt_str: Datetime string
        format_str: Format string

    Returns:
        Datetime object
    """
    return datetime.strptime(dt_str, format_str)


def get_date_range(
    period: str, end_date: Optional[datetime] = None
) -> tuple[datetime, datetime]:
    """
    Get start and end dates for a time period.

    Args:
        period: Time period ('last_7_days', 'last_30_days', 'last_90_days', 'this_month', 'last_month')
        end_date: End date (defaults to now)

    Returns:
        Tuple of (start_date, end_date)
    """
    if end_date is None:
        end_date = get_utc_now()

    if period == "last_7_days":
        start_date = end_date - timedelta(days=7)
    elif period == "last_30_days":
        start_date = end_date - timedelta(days=30)
    elif period == "last_90_days":
        start_date = end_date - timedelta(days=90)
    elif period == "this_month":
        start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    elif period == "last_month":
        first_this_month = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = first_this_month - timedelta(seconds=1)
        start_date = end_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    else:
        # Default to last 30 days
        start_date = end_date - timedelta(days=30)

    return start_date, end_date


def get_optimal_posting_times(
    timezone: str = "UTC", platform: str = "instagram"
) -> List[dict]:
    """
    Get optimal posting times for a platform.

    Args:
        timezone: User's timezone
        platform: Social media platform

    Returns:
        List of optimal time slots
    """
    # Define optimal times per platform (based on industry research)
    optimal_times = {
        "instagram": [
            {"day": "monday", "hour": 11},
            {"day": "tuesday", "hour": 10},
            {"day": "wednesday", "hour": 11},
            {"day": "thursday", "hour": 10},
            {"day": "friday", "hour": 10},
            {"day": "saturday", "hour": 11},
            {"day": "sunday", "hour": 10},
        ],
        "twitter": [
            {"day": "monday", "hour": 9},
            {"day": "tuesday", "hour": 9},
            {"day": "wednesday", "hour": 9},
            {"day": "thursday", "hour": 9},
            {"day": "friday", "hour": 9},
            {"day": "saturday", "hour": 10},
            {"day": "sunday", "hour": 10},
        ],
        "facebook": [
            {"day": "monday", "hour": 13},
            {"day": "tuesday", "hour": 13},
            {"day": "wednesday", "hour": 13},
            {"day": "thursday", "hour": 13},
            {"day": "friday", "hour": 13},
            {"day": "saturday", "hour": 12},
            {"day": "sunday", "hour": 12},
        ],
        "linkedin": [
            {"day": "monday", "hour": 10},
            {"day": "tuesday", "hour": 10},
            {"day": "wednesday", "hour": 10},
            {"day": "thursday", "hour": 10},
            {"day": "friday", "hour": 10},
            {"day": "saturday", "hour": 0},  # Weekend not recommended
            {"day": "sunday", "hour": 0},
        ],
        "tiktok": [
            {"day": "monday", "hour": 18},
            {"day": "tuesday", "hour": 18},
            {"day": "wednesday", "hour": 18},
            {"day": "thursday", "hour": 18},
            {"day": "friday", "hour": 18},
            {"day": "saturday", "hour": 19},
            {"day": "sunday", "hour": 19},
        ],
        "youtube": [
            {"day": "monday", "hour": 14},
            {"day": "tuesday", "hour": 14},
            {"day": "wednesday", "hour": 14},
            {"day": "thursday", "hour": 14},
            {"day": "friday", "hour": 14},
            {"day": "saturday", "hour": 12},
            {"day": "sunday", "hour": 12},
        ],
    }

    return optimal_times.get(platform.lower(), optimal_times["instagram"])


def calculate_next_post_time(
    last_post_time: Optional[datetime],
    platform: str,
    timezone: str = "UTC",
    min_gap_hours: int = 4,
) -> datetime:
    """
    Calculate the next optimal time to post.

    Args:
        last_post_time: When the last post was made
        platform: Social media platform
        timezone: User's timezone
        min_gap_hours: Minimum hours between posts

    Returns:
        Next optimal posting time
    """
    if last_post_time is None:
        # First post - use next optimal time
        now = get_local_now(timezone)
    else:
        # Ensure minimum gap
        now = last_post_time + timedelta(hours=min_gap_hours)

    optimal_times = get_optimal_posting_times(timezone, platform)

    # Find next optimal time
    current_day = now.strftime("%A").lower()
    current_hour = now.hour

    # Get today's optimal hour
    today_optimal = next(
        (t for t in optimal_times if t["day"] == current_day), optimal_times[0]
    )

    if current_hour < today_optimal["hour"]:
        # Can post today
        next_time = now.replace(
            hour=today_optimal["hour"], minute=0, second=0, microsecond=0
        )
    else:
        # Post tomorrow
        next_day = now + timedelta(days=1)
        next_day_name = next_day.strftime("%A").lower()
        next_optimal = next(
            (t for t in optimal_times if t["day"] == next_day_name), optimal_times[0]
        )
        next_time = next_day.replace(
            hour=next_optimal["hour"], minute=0, second=0, microsecond=0
        )

    return next_time


def humanize_datetime(dt: datetime) -> str:
    """
    Convert datetime to human-readable format (e.g., '2 hours ago').

    Args:
        dt: Datetime object

    Returns:
        Human-readable string
    """
    return pendulum.instance(dt).diff_for_humans()


def is_within_business_hours(
    dt: datetime, timezone: str = "UTC", start_hour: int = 9, end_hour: int = 17
) -> bool:
    """
    Check if datetime is within business hours.

    Args:
        dt: Datetime to check
        timezone: Timezone string
        start_hour: Business day start hour
        end_hour: Business day end hour

    Returns:
        True if within business hours
    """
    tz = pytz.timezone(timezone)
    local_dt = dt.astimezone(tz)

    # Check if weekday (Monday=0, Sunday=6)
    if local_dt.weekday() >= 5:
        return False

    # Check if within hours
    return start_hour <= local_dt.hour < end_hour
