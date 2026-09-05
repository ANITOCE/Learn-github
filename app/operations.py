"""Pure arithmetic operations for the math API.

These functions are stateless and independent of Flask so they can be
unit-tested directly. Results follow standard IEEE 754 double semantics.
"""


def add(a: float, b: float) -> float:
    """Return the sum of two numbers."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Return the difference of two numbers."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Return the product of two numbers."""
    return a * b


def divide(a: float, b: float) -> float:
    """Return the quotient of two numbers.

    Division by zero is validated at the HTTP layer before this function is
    called (FR-007), so a zero divisor never reaches this function.
    """
    return a / b
