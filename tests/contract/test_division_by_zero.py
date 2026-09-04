"""Contract tests for division by zero (FR-007).

All zero representations (0, 0.0, -0, scientific notation) must yield
400 + {"error": "division by zero"}; add/subtract/multiply are unaffected.
"""

import pytest


@pytest.mark.parametrize("b", ["0", "0.0", "-0", "0e5"])
def test_divide_by_zero_returns_400(client, b):
    response = client.get("/divide", query_string={"a": "1", "b": b})
    assert response.status_code == 400
    assert response.get_json() == {"error": "division by zero"}


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/add", 1.0),
        ("/subtract", 1.0),
        ("/multiply", 0.0),
    ],
)
def test_other_operations_unaffected_by_zero(client, path, expected):
    response = client.get(path, query_string={"a": "1", "b": "0"})
    assert response.status_code == 200
    assert response.get_json() == {"result": expected}
