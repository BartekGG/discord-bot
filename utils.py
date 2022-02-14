

def timedelta_format(time_delta):
    """Format default timedelta to \"x days, y hours, z minutes\" format."""
    seconds = int(time_delta.total_seconds())
    periods = [
        ("day", 60*60*24),
        ("hour", 60*60),
        ("minute", 60)
    ]

    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            has_s = "s" if period_value > 1 else ""
            strings.append(f"{period_value} {period_name}{has_s}")

    return ", ".join(strings)


if __name__ == "__main__":
    pass
