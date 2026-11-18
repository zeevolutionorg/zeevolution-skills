"""Contract tests for skills/foundations/cloud-workspace/ (SKILL.md, adapters, assets)."""

import re

import pytest
from helpers import assert_skill_contract, skill_dir

pytestmark = pytest.mark.contract
SKILL = skill_dir("foundations", "cloud-workspace")
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")


def test_contract():
    assert_skill_contract(SKILL, user_invoked=False)


@pytest.mark.parametrize("adapter", ["GOOGLE.md", "MICROSOFT.md", "FILES.md", "MANUAL.md", "SHEETS.md"])
def test_adapter_documents_exist_and_are_linked(adapter):
    assert (SKILL / adapter).exists()
    assert f"({adapter})" in TEXT


def test_fallback_order_ends_with_manual():
    section = TEXT.split("### Fallback order", 1)[1].split("##", 1)[0]
    steps = re.findall(r"^\d\. \*\*([^*]+)\*\*", section, re.M)
    assert steps[0].startswith("Connector") and steps[1].startswith("Files") and steps[2].startswith("Manual")


@pytest.mark.parametrize("adapter", ["GOOGLE.md", "MICROSOFT.md", "FILES.md"])
def test_every_adapter_points_to_the_manual_fallback(adapter):
    assert "MANUAL.md" in (SKILL / adapter).read_text(encoding="utf-8")


def test_manual_adapter_covers_chat_only_delivery():
    text = (SKILL / "MANUAL.md").read_text(encoding="utf-8")
    assert "Chat only" in text and "```markdown" in text


@pytest.mark.parametrize("script", ["render_doc.py", "build_sheet.py", "make_bundle.py"])
def test_scripts_exist_and_are_documented(script):
    assert (SKILL / "scripts" / script).exists()
    assert f"scripts/{script}" in TEXT


class TestPasteGuides:
    def read(self, lang):
        return (SKILL / "assets" / f"paste-guide.{lang}.md").read_text(encoding="utf-8")

    @pytest.mark.parametrize("lang", ["en", "pt-BR"])
    def test_placeholders(self, lang):
        assert set(re.findall(r"\{\{([a-z_]+)\}\}", self.read(lang))) == {"folder_name", "doc_list"}

    def test_same_structure_in_both_languages(self):
        heads = [re.findall(r"^#+ ", self.read(lang), re.M) for lang in ("en", "pt-BR")]
        assert heads[0] == heads[1]

    @pytest.mark.parametrize("lang", ["en", "pt-BR"])
    def test_covers_google_word_and_others(self, lang):
        text = self.read(lang)
        assert "Google Docs" in text and "Word" in text and "Notion" in text
