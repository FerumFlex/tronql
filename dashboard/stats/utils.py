import calendar
from datetime import datetime, timezone


def round_hour_datetime(value: datetime) -> datetime:
    return value.replace(second=0, microsecond=0, minute=0)


def get_current_biling_period(created: datetime) -> tuple[datetime, datetime]:
    now = datetime.now(timezone.utc)
    billing_cycle = now.replace(hour=0, minute=0, second=0, microsecond=0)

    if now.month == 1:
        prev_year = now.year - 1
        prev_month = 1
    else:
        prev_year = now.year
        prev_month = now.month - 1

    _, total_month_days = calendar.monthrange(prev_year, prev_month)
    billing_cycle = billing_cycle.replace(
        year=prev_year,
        month=prev_month,
        day=min(total_month_days, created.day),
    )
    return billing_cycle, now
