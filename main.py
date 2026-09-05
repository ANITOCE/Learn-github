"""Math API entry point.

Creates the Flask application via the app factory and runs the development
server on http://127.0.0.1:5000 (FR-013).
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)