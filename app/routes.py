"""HTTP layer: mount the four arithmetic GET routes.

This module contains no arithmetic implementation (Constitution III);
it parses request parameters and delegates computation to app.operations.
"""

from flask import Flask, jsonify, request

from app.operations import add, divide, multiply, subtract


def register_routes(app: Flask) -> None:
    """Mount GET /add, /subtract, /multiply and /divide on the app."""

    def _handler(operation):
        def endpoint():
            a = float(request.args["a"])
            b = float(request.args["b"])
            return jsonify(result=operation(a, b))

        return endpoint

    app.add_url_rule("/add", endpoint="add", view_func=_handler(add))
    app.add_url_rule("/subtract", endpoint="subtract", view_func=_handler(subtract))
    app.add_url_rule("/multiply", endpoint="multiply", view_func=_handler(multiply))
    app.add_url_rule("/divide", endpoint="divide", view_func=_handler(divide))
