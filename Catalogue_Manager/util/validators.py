from datetime import datetime, date

def validate_boolean(value):
    """
    Validates and converts a value to a boolean.

    Args:
        value: The input value to be validated. Typically expected to be 0, 1, "0", or "1".

    Returns:
        bool: True if the input is 1, False if 0.

    Raises:
        ValueError: If the input is empty, not an integer, or not 0 or 1.
    """
    if str(value).strip() == "":
        raise ValueError("Boolean input cannot be empty.")
    try:
        value = int(value)
    except ValueError:
        raise ValueError("Boolean value must be an integer (0 or 1).")
    if value not in (0, 1):
        raise ValueError("Boolean value must be either 0 (False) or 1 (True).")
    return bool(value)

def validate_date(date_str):
    """
    Validates a date string. Ensures format is YYYY-MM-DD and the date is not in the past.

    Args:
        date_str (str): Date string to validate.

    Returns:
        datetime.date: Parsed date object.

    Raises:
        ValueError: If empty, improperly formatted, or in the past.
    """
    if not date_str.strip():
        raise ValueError("Date input cannot be empty.")
    try:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    if parsed_date < date.today():
        raise ValueError("Date cannot be in the past.")
    return parsed_date

def validate_int(value):
    """
    Validates that the input is a non-empty, valid integer.

    Args:
        value: Input to validate.

    Returns:
        int: Validated integer.

    Raises:
        ValueError: If input is empty or not an integer.
    """
    if str(value).strip() == "":
        raise ValueError("Integer input cannot be empty.")
    try:
        return int(value)
    except ValueError:
        raise ValueError("Invalid integer value. Must be a number.")
