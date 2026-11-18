"""Shared fixtures. Helpers live in tests/helpers.py.

The tests/ tree mirrors the repository: the test for `scripts/build.py` lives at
`tests/scripts/test_build.py`, the test for `skills/foundations/cloud-workspace/scripts/render_doc.py`
at `tests/skills/foundations/cloud-workspace/scripts/test_render_doc.py`, and so on.
tests/test_repo_layout.py enforces it.
"""

import json
import shutil

import pytest
from helpers import ROOT


@pytest.fixture(scope="session")
def root():
    return ROOT


@pytest.fixture
def ctx_file(tmp_path):
    """A complete, fictional context for one person."""
    ctx = {
        "person_name": "Ana Souza",
        "leader_name": "Morgan Lee",
        "role": "Data Scientist",
        "discipline": "Data Science",
        "level": "Contributing",
        "next_level": "Owning",
        "start_date": "2026-11-18",
        "created_date": "2026-11-18",
        "next_meeting_date": "2026-12-02",
        "cycle": "2027 H1",
        "ladder_source": "Generic ladder",
        "doc_link_hub": "https://example.com/hub",
    }
    p = tmp_path / "context.json"
    p.write_text(json.dumps(ctx), encoding="utf-8")
    return p


@pytest.fixture(scope="session")
def soffice():
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        pytest.skip("LibreOffice not installed")
    return exe


LEVELS = {"unit", "contract", "e2e", "libreoffice"}


def pytest_collection_modifyitems(config, items):
    """Every test must declare its level, so CI stages can select them (-m unit, -m e2e, ...)."""
    unmarked = [i.nodeid for i in items if not LEVELS & {m.name for m in i.iter_markers()}]
    if unmarked:
        raise pytest.UsageError("tests without a level marker (unit/contract/e2e/libreoffice):\n  " + "\n  ".join(unmarked))
