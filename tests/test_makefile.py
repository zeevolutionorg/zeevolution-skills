"""`make check` runs what CI runs (.github/workflows/ci.yml), so a green local run predicts a green PR."""

import re
import subprocess

import pytest
import yaml
from helpers import ROOT

pytestmark = pytest.mark.contract

CI = yaml.safe_load((ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8"))
MAKEFILE = (ROOT / "Makefile").read_text(encoding="utf-8")
# What `make check` would run, variables expanded; proves each stage is wired into check.
CHECK = subprocess.run(["make", "-n", "check"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
STEPS = [step for job in CI["jobs"].values() for step in job["steps"]]
RUNS = "\n".join(step.get("run", "") for step in STEPS)


@pytest.mark.parametrize("script", sorted(set(re.findall(r"scripts/\w+\.py", RUNS))))
def test_every_ci_script_runs_locally(script):
    assert script in CHECK


@pytest.mark.parametrize(
    "command",
    [
        "ruff check",
        "ruff format --check",
        "yamllint -c .yamllint.yml",
        '-m "unit or contract"',
        "-m e2e",
        "-m libreoffice",
        "scripts/build.py --out dist",
        "scripts/check_leaks.py . dist",
    ],
)
def test_ci_command_runs_locally(command):
    assert command in RUNS, f"CI no longer runs {command!r}: update this test"
    assert command in CHECK


def test_markdownlint_globs_match_ci():
    step = next(s for s in STEPS if s.get("name") == "markdownlint")
    ci_globs = step["with"]["globs"].split()
    make_globs = re.search(r"^MD_GLOBS\s*=\s*(.*)$", MAKEFILE, re.M).group(1).replace('"', "").split()
    assert make_globs == ci_globs


def test_actionlint_runs_locally_when_installed():
    assert any("actionlint" in step.get("uses", "") for step in STEPS)
    assert "then actionlint;" in CHECK


def test_secret_scan_uses_the_ci_gitleaks_version():
    version = re.search(r"gitleaks/releases/download/(v[\d.]+)/", RUNS).group(1)
    assert f"gitleaks/v8@{version} detect --source . --redact" in CHECK
