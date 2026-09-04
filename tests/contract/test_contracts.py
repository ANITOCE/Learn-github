"""Contract tests for the four arithmetic endpoints (success paths).

FR-001~FR-005, FR-008, FR-009, FR-011: 200 with a body that is exactly
{"result": <expected>} (single key, no extra fields); results equal direct
IEEE 754 double arithmetic.
"""

import pytest


def _call(client, path: str, a: str, b: str):
    return client.get(path, query_string={"a": a, "b": b})


@pytest.mark.parametrize(
    ("path", "a", "b", "expected"),
    [
        ("/add", "2", "3", 5.0),
        ("/add", "-1", "1e3", 999.0),
        ("/subtract", "7", "4", 3.0),
        ("/subtract", "1.5", "0.5", 1.0),
        ("/multiply", "6", "7", 42.0),
        ("/multiply", "-3", "4", -12.0),
        ("/divide", "10", "2", 5.0),
        ("/divide", "1.5", "0.5", 3.0),
    ],
)
def test_endpoint_success(client, path, a, b, expected):
    response = _call(client, path, a, b)
    assert response.status_code == 200
    assert response.get_json() == {"result": expected}
