"""Contract tests for skills/foundations/doc-templates/"""

import re

import pytest
from helpers import ROOT, assert_skill_contract, skill_dir

pytestmark = pytest.mark.contract
SKILL = skill_dir("foundations", "doc-templates")
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")


def test_contract():
    assert_skill_contract(SKILL, user_invoked=False)


def test_every_placeholder_used_in_templates_is_documented():
    documented = set(re.findall(r"`\{\{([a-z_]+)\}\}`", TEXT))
    documented |= {
        f"doc_link_{k}" for k in re.findall(r"`(\w+)`", TEXT.split("Link to a sibling document:", 1)[1].split("|", 1)[0])
    }
    used = set()
    for md in (ROOT / "templates").glob("*/*/0*.md"):
        used |= set(re.findall(r"\{\{([a-z_]+)\}\}", md.read_text(encoding="utf-8")))
    assert used - {"doc_link_hub"} <= documented | {"doc_link_hub"}, used - documented


@pytest.mark.parametrize("emoji", ["ℹ️", "💡", "✍️", "🗓️", "⚠️"])
def test_callout_emojis_documented(emoji):
    assert emoji in TEXT
