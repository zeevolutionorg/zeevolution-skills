"""Contract tests for skills/foundations/disciplines/"""

import pytest
from helpers import assert_skill_contract, skill_dir

pytestmark = pytest.mark.contract
SKILL = skill_dir("foundations", "disciplines")
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")


def test_contract():
    assert_skill_contract(SKILL, user_invoked=False)


@pytest.mark.parametrize("discipline", ["Engineering", "Data Science", "Design", "Product Management"])
def test_every_discipline_has_column_and_examples(discipline):
    header = next(ln for ln in TEXT.splitlines() if ln.startswith("| |"))
    assert discipline in header
    assert f"**{discipline}**" in TEXT


def test_other_discipline_follow_up_question():
    assert "Other" in TEXT and "?" in TEXT.split("## Other disciplines", 1)[1]
