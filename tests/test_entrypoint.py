"""Entrypoint replacement tests (FR-013, SC-005).

main.py must expose the API entry (create_app) and no longer reference or
run the greeting scripts. Runtime behaviour of `python main.py` is verified
manually in T018 (quickstart).
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_importing_main_produces_no_greeting_output():
    result = subprocess.run(
        [sys.executable, "-c", "import main"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == ""
    assert result.stderr == ""


def test_main_exposes_create_app():
    import main

    app = main.create_app()
    with app.test_client() as test_client:
        response = test_client.get("/add", query_string={"a": "1", "b": "2"})
    assert response.status_code == 200
    assert response.get_json() == {"result": 3.0}


def test_main_source_no_longer_references_greeting_scripts():
    source = (REPO_ROOT / "main.py").read_text(encoding="utf-8")
    for name in ("Hello_Dad", "Hello_Mom", "Hello_GitHub"):
        assert name not in source, f"main.py still references {name}"
