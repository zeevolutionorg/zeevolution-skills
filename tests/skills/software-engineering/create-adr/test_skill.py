"""Contract tests for skills/software-engineering/create-adr/"""

import re

import pytest
from helpers import assert_skill_contract, skill_dir

pytestmark = pytest.mark.contract
SKILL = skill_dir("software-engineering", "create-adr")
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")
TEMPLATE = (SKILL / "template.md").read_text(encoding="utf-8")


def test_contract():
    assert_skill_contract(SKILL, user_invoked=False)


@pytest.mark.parametrize("mode", ["compress", "from-pr", "free-prompt", "supersede"])
def test_all_four_input_modes(mode):
    assert f"`{mode}`" in TEXT


def test_always_asks_mode_and_folder_and_never_guesses():
    assert "Always ask, never guess" in TEXT and "destination folder" in TEXT


def test_asks_before_deleting():
    assert "No silent deletes" in TEXT


@pytest.mark.parametrize(
    "section", ["## Context", "## Decision", "## Alternatives considered", "## Consequences", "## Related artifacts"]
)
def test_template_sections(section):
    assert section in TEMPLATE


def test_template_has_at_least_two_alternatives():
    assert len(re.findall(r"^### Option [A-Z]", TEMPLATE, re.M)) >= 2


def test_size_budget_documented():
    assert "## Size budget" in TEXT and "4000 tokens" in TEXT
