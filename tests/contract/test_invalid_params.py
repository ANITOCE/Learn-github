"""Contract tests for invalid request parameters (FR-006, FR-009).

Missing or non-numeric parameters must yield 400 with a body that is exactly
{"error": "invalid parameters"} (no extra keys, no internal details).
"""

import pytest

PATHS = ["/add", "/subtract", "/multiply", "/divide"]


@pytest.mark.parametrize("path", PATHS)
@pytest.mark.parametrize(
    "query",
    [
        {"b": "2"},  # missing a
        {"a": "1"},  # missing b
        {"a": "abc", "b": "2"},  # non-numeric a
        {"a": "", "b": "2"},  # empty a
        {"a": "2", "b": "xyz"},  # non-numeric b
    ],
)
def test_invalid_parameters_return_400(client, path, query):
    response = client.get(path, query_string=query)
    assert response.status_code == 400
    assert response.get_json() == {"error": "invalid parameters"}


@pytest.mark.parametrize(
    ("path", "expected"),
    [
        ("/add", 7.0),
        ("/subtract", 3.0),
        ("/multiply", 10.0),
        ("/divide", 2.5),
    ],
)
def test_integer_format_parameters_accepted(client, path, expected):
    response = client.get(path, query_string={"a": "5", "b": "2"})
    assert response.status_code == 200
    assert response.get_json() == {"result": expected}
