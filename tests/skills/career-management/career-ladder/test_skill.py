"""Contract tests for skills/career-management/career-ladder/"""

import re

import pytest
from helpers import assert_skill_contract, skill_dir

pytestmark = pytest.mark.contract
SKILL = skill_dir("career-management", "career-ladder")
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")


def test_contract():
    assert_skill_contract(SKILL, user_invoked=False)


def test_questions_l1_to_l3():
    assert re.findall(r"\*\*(L\d)\*\*", TEXT) == ["L1", "L2", "L3"]


@pytest.mark.parametrize("lang", ["en", "pt-BR"])
def test_bundled_generic_ladder(lang):
    assert (SKILL / "assets" / f"generic-ladder.{lang}.yaml").exists()


def test_generic_ladder_markdown_is_generated():
    md = (SKILL / "GENERIC-LADDER.md").read_text(encoding="utf-8")
    assert "(en)" in md and "(pt-BR)" in md


def test_never_writes_company_ladders_into_the_repo():
    assert "Never" in TEXT and "repository" in TEXT
