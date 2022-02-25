from decimal import Decimal


def ensure_decimal(value):
    if isinstance(value, float):
        return Decimal(str(value))

    if isinstance(value, str):
        return Decimal(value)

    return value
