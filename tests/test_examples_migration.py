"""Migration tests for the example scripts (FR-012, SC-004).

The greeting and Person scripts must live under examples/ with unchanged
content and identical runtime behaviour.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = REPO_ROOT / "examples"

MIGRATED_SCRIPTS = ["Hello_Dad.py", "Hello_GitHub.py", "Hello_Mom.py", "Person.py"]


def test_examples_exist_after_migration():
    for script in MIGRATED_SCRIPTS:
        assert (EXAMPLES / script).is_file(), f"examples/{script} missing"


def test_old_paths_removed():
    for script in MIGRATED_SCRIPTS:
        assert not (REPO_ROOT / script).exists(), f"{script} still at repo root"


@pytest.mark.parametrize(
    ("script", "call", "expected"),
    [
        ("Hello_Dad.py", "import Hello_Dad; Hello_Dad.hello_dad()", "Hello, Dad!\n"),
        ("Hello_Mom.py", "import Hello_Mom; Hello_Mom.hello_mom()", "Hello, Mom!\n"),
        (
            "Hello_GitHub.py",
            "import Hello_GitHub; Hello_GitHub.hello_github()",
            "Hello GitHub!\n",
        ),
    ],
)
def test_greeting_behaviour_unchanged(script, call, expected):
    assert (EXAMPLES / script).is_file()
    result = subprocess.run(
        [sys.executable, "-c", call],
        cwd=str(EXAMPLES),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == expected
    assert result.stderr == ""


def test_scripts_run_directly_without_output():
    # Direct execution produces no output (scripts have no module-level
    # side effects) — identical to their behaviour at the original location.
    for script in MIGRATED_SCRIPTS:
        result = subprocess.run(
            [sys.executable, script],
            cwd=str(EXAMPLES),
            capture_output=True,
            text=True,
            check=True,
        )
        assert result.stdout == ""
        assert result.stderr == ""


def test_person_importable_and_unchanged():
    assert (EXAMPLES / "Person.py").is_file()
    result = subprocess.run(
        [sys.executable, "-c", "import Person; p = Person.Person(); print(p.get_name())"],
        cwd=str(EXAMPLES),
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout == "Nobody\n"
