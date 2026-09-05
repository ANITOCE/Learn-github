"""HTTP layer: mount the four arithmetic GET routes.

This module contains no arithmetic implementation (Constitution III);
it parses request parameters and delegates computation to app.operations.
"""

from flask import Flask, jsonify, request

from app.operations import add, divide, multiply, subtract

INVALID_PARAMETERS = "invalid parameters"
DIVISION_BY_ZERO = "division by zero"


def _parse_parameters() -> tuple[float, float] | None:
    """Return (a, b) as floats, or None when missing or non-numeric."""
    a_raw = request.args.get("a")
    b_raw = request.args.get("b")
    if a_raw is None or b_raw is None:
        return None
    try:
        return float(a_raw), float(b_raw)
    except ValueError:
        return None


def register_routes(app: Flask) -> None:
    """Mount GET /add, /subtract, /multiply and /divide on the app."""

    def _handler(operation, reject_zero_divisor=False):
        def endpoint():
            parameters = _parse_parameters()
            if parameters is None:
                return jsonify(error=INVALID_PARAMETERS), 400
            a, b = parameters
            if reject_zero_divisor and b == 0.0:
                return jsonify(error=DIVISION_BY_ZERO), 400
            return jsonify(result=operation(a, b))

        return endpoint

    app.add_url_rule("/add", endpoint="add", view_func=_handler(add))
    app.add_url_rule("/subtract", endpoint="subtract", view_func=_handler(subtract))
    app.add_url_rule("/multiply", endpoint="multiply", view_func=_handler(multiply))
    app.add_url_rule(
        "/divide", endpoint="divide", view_func=_handler(divide, reject_zero_divisor=True)
    )
