def clean_value(value: str):
    value = value.strip()
    if value == '-':
        return None
    try:
        return float(value.replace(",", ""))
    except ValueError:
        return value

