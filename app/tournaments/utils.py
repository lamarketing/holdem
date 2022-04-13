from datetime import datetime, timedelta, timezone


def is_time_to_registration_tournament(time_start: datetime.now) -> bool:
    """Для защиты от регистраций на турнир не вовремя."""
    return (time_start - timedelta(minutes=11)) <= datetime.now(timezone.utc) < time_start


def is_time_to_active_tournament(time_start: datetime.now) -> bool:
    """Для защиты от регистраций на турнир не вовремя."""
    return time_start - timedelta(milliseconds=100) <= datetime.now(timezone.utc)
