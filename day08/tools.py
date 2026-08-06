from datetime import date


def get_today_date():
    """
    Returns today's date as string in the format YYYY-MM-DD.
    """
    return str(date.today())

def add_numbers(a: float, b: float) -> float:
    """
    Adds two numbers and returns the result.
    """
    return a + b