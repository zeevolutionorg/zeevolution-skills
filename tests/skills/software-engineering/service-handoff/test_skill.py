"""Contract tests for skills/software-engineering/service-handoff/"""

import re

import pytest
from helpers import assert_skill_contract, skill_dir

pytestmark = pytest.mark.contract
SKILL = skill_dir("software-engineering", "service-handoff")
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")
TEMPLATE = (SKILL / "template.md").read_text(encoding="utf-8")


def test_contract():
    assert_skill_contract(SKILL, user_invoked=True)


def test_interview_is_mandatory_and_numbered():
    assert "Do not skip step 1" in TEXT
    ids = [int(n) for n in re.findall(r"^\| (\d+) \| \*\*", TEXT, re.M)]
    assert ids[:14] == list(range(1, 15))


def test_redacts_secrets():
    assert "Redact secrets and PII" in TEXT


def test_offers_other_destinations():
    assert "cloud-workspace" in TEXT and "chat" in TEXT


@pytest.mark.parametrize(
    "section", ["## TL;DR", "## Incoming owner checklist", "## Observability snapshot", "## Ownership transfer PR checklist"]
)
def test_template_sections(section):
    assert section in TEMPLATE


def test_cheatsheet_exists_and_is_linked():
    assert (SKILL / "stack-cheatsheet.md").exists() and "stack-cheatsheet.md" in TEXT
