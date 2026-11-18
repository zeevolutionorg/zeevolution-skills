"""Contract tests for evals/<case>/ — every behavioral eval case is well formed."""

import re

import pytest
import yaml
from helpers import ROOT

pytestmark = pytest.mark.contract

CASES = sorted(p for p in (ROOT / "evals").iterdir() if p.is_dir() and p.name != "results")
GRADER_TYPES = {"regex", "tool_used", "tool_order", "file_exists", "llm", "baseline"}


def fm(path):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", path.read_text(encoding="utf-8"), re.S)
    assert m, f"{path} needs frontmatter"
    return yaml.safe_load(m.group(1)) or {}, m.group(2).strip()


@pytest.mark.parametrize("case", CASES, ids=lambda p: p.name)
def test_prompt(case):
    meta, body = fm(case / "prompt.md")
    assert meta["name"] == case.name
    assert body, "empty prompt"
    assert meta.get("runs", 3) <= 3 and meta.get("timeout_seconds", 300) <= 900


@pytest.mark.parametrize("case", CASES, ids=lambda p: p.name)
def test_graders(case):
    graders = list((case / "graders").glob("*.md"))
    assert graders, "at least one grader"
    for g in graders:
        meta, body = fm(g)
        assert meta.get("type") in GRADER_TYPES, g.name
        if meta["type"] == "llm":
            assert len(body) > 40, f"{g.name}: llm grader needs explicit criteria"


def test_smoke_subset_exists():
    tags = [fm(c / "prompt.md")[0].get("tags", []) for c in CASES]
    assert sum("smoke" in t for t in tags) >= 2
