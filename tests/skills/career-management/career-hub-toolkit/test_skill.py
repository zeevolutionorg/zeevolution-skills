"""Contract tests for skills/career-management/career-hub-toolkit/ (SKILL.md + bundled assets)."""

import pytest
from helpers import LANGS, assert_skill_contract, skill_dir

pytestmark = pytest.mark.contract
SKILL = skill_dir("career-management", "career-hub-toolkit")
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")


def test_contract():
    assert_skill_contract(SKILL, user_invoked=True)


def test_both_modes_in_usage():
    assert "/career-hub-toolkit me" in TEXT and "lead mode" in TEXT


def test_fallback_order_and_manual_mode():
    assert "Connector / MCP" in TEXT and "**Files**" in TEXT and "**Manual**" in TEXT
    assert "### Manual mode" in TEXT and "paste-guide" in TEXT


def test_hub_is_central_and_created_last():
    assert "central piece" in TEXT and "Fill the Hub last" in TEXT


def test_never_chooses_between_growth_and_focus():
    assert "Never choose for them" in TEXT


def test_confirmation_before_creating():
    assert "Nothing is created before" in TEXT


@pytest.mark.parametrize(
    "path",
    [
        "assets/templates/bundle.yaml",
        "assets/templates/05-ladder-assessment.sheet.yaml",
        "scripts/render_doc.py",
        "scripts/build_sheet.py",
        "scripts/make_bundle.py",
    ],
)
def test_bundled_files(path):
    assert (SKILL / path).exists(), path


@pytest.mark.parametrize("lang", LANGS)
def test_bundled_language_assets(lang):
    assert len(list((SKILL / "assets" / "templates" / lang).glob("0*.md"))) == 9
    assert (SKILL / "assets" / f"paste-guide.{lang}.md").exists()
    assert (SKILL / "assets" / f"generic-ladder.{lang}.yaml").exists()
