

from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from constants import DATE_FORMAT


def validate_date(value):
    value = str(value).strip()
    try:
        datetime.strptime(value, DATE_FORMAT)
    except ValueError as error:
        raise ValueError("Enter the date as DD/MM/YYYY,") from error
    return value


def validate_text(value, field_name):
    cleaned_value = str(value).strip()
    if not cleaned_value:
        raise ValueError(f"{field_name} is required.")
    return cleaned_value


def to_money(value):
    try:
        amount = Decimal(str(value)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    except (InvalidOperation, ValueError, TypeError) as error:
        raise ValueError("Enter a valid price") from error

    if not amount.is_finite() or amount < 0:
        raise ValueError("Price must be zero or greater.")

    return amount
