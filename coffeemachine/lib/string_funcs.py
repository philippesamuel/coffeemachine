"""Functions for string formatting."""


def format_dollars(cents: int) -> str:
    """Format cents as dollars."""
    return f"${cents / 100:,.2f}"
