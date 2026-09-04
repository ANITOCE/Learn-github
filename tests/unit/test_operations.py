"""Unit tests for the pure arithmetic functions in app.operations.

FR-011: results must be exactly equal to direct IEEE 754 double arithmetic
(no tolerance). All cases below are exactly representable in binary floating
point, except where explicitly documenting standard float semantics.
"""

import pytest

from app.operations import add, divide, multiply, subtract


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (2.0, 3.0, 5.0),
        (1.5, 2.5, 4.0),
        (-2.5, 1.5, -1.0),
        (1e3, 2e2, 1200.0),
        # Standard IEEE 754 double semantics, no arbitrary precision.
        (0.1, 0.2, 0.30000000000000004),
    ],
)
def test_add(a: float, b: float, expected: float) -> None:
    assert add(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (7.0, 4.0, 3.0),
        (1.5, 0.5, 1.0),
        (-1.0, 1e3, -1001.0),
        (0.0, 0.0, 0.0),
    ],
)
def test_subtract(a: float, b: float, expected: float) -> None:
    assert subtract(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (6.0, 7.0, 42.0),
        (1.5, 2.0, 3.0),
        (-3.0, 4.0, -12.0),
        (1e3, 1e-2, 10.0),
    ],
)
def test_multiply(a: float, b: float, expected: float) -> None:
    assert multiply(a, b) == expected


@pytest.mark.parametrize(
    ("a", "b", "expected"),
    [
        (10.0, 2.0, 5.0),
        (1.5, 0.5, 3.0),
        (-6.0, 2.0, -3.0),
        (7.0, 2.0, 3.5),
    ],
)
def test_divide(a: float, b: float, expected: float) -> None:
    assert divide(a, b) == expected
