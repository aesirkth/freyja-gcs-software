def format_value(value, unit, digits=1):
    if value is None:
        return f"-- {unit}"
    if isinstance(value, float):
        return f"{value:.{digits}f} {unit}"
    return f"{value} {unit}"
