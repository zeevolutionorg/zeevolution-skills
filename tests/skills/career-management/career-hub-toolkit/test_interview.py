"""Contract tests for skills/career-management/career-hub-toolkit/INTERVIEW.md — the exact questions."""

import re

import pytest
from helpers import skill_dir

pytestmark = pytest.mark.contract
TEXT = (skill_dir("career-management", "career-hub-toolkit") / "INTERVIEW.md").read_text(encoding="utf-8")
ROWS = {m.group(1): m.group(0) for m in re.finditer(r"^\| ([STLF]\d+) \|.*$", TEXT, re.M)}
EXPECTED = [f"S{i}" for i in range(1, 7)] + [f"T{i}" for i in range(1, 11)] + ["L1", "L2", "L3", "F1", "F2"]


def test_every_question_id_present_once():
    assert sorted(ROWS) == sorted(EXPECTED)


@pytest.mark.parametrize("qid", EXPECTED)
def test_each_question_has_english_and_portuguese_wording(qid):
    cells = [c.strip() for c in ROWS[qid].strip("|").split("|")]
    quoted = [c for c in cells if c.startswith('"')]
    assert len(quoted) >= 2, f"{qid}: needs an English and a Portuguese question"
    assert quoted[0] != quoted[1]


def test_confirmation_in_both_languages():
    assert '"Create these documents?"' in TEXT and '"Posso criar estes documentos?"' in TEXT


def test_platform_question_offers_markdown():
    assert "Markdown I copy and paste myself" in ROWS["S3"]


def test_question_count_table_present():
    assert "## Question count" in TEXT
