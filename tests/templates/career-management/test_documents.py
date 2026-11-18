"""Contract tests for templates/career-management/<lang>/NN-*.md

Every document must stay self-explanatory and consistent: these tests encode the rules in
skills/foundations/doc-templates/SKILL.md and the decisions behind the career hub.
"""

import re

import pytest
from helpers import LANGS, TPL

pytestmark = pytest.mark.contract

ALLOWED_PLACEHOLDERS = {
    "person_name",
    "leader_name",
    "role",
    "discipline",
    "level",
    "next_level",
    "start_date",
    "created_date",
    "next_meeting_date",
    "cycle",
    "ladder_source",
} | {
    f"doc_link_{k}"
    for k in ("hub", "one_on_one", "growth_plan", "focus_plan", "brag", "ladder", "review", "evidence", "onboarding")
}
CALLOUT_EMOJIS = ("🗓️", "ℹ️", "💡", "✍️", "⚠️")
DISCIPLINE_LABELS = {
    "en": ("Engineering", "Data Science", "Design", "Product"),
    "pt-BR": ("Engenharia", "Ciência de Dados", "Design", "Produto"),
}
DOCS = sorted(p.name for p in (TPL / "en").glob("0*.md"))
CASES = [(lang, name) for lang in LANGS for name in DOCS]


def read(lang, name):
    return (TPL / lang / name).read_text(encoding="utf-8")


def callouts(text):
    out, prev = [], False
    for line in text.splitlines():
        q = line.startswith(">")
        if q and not prev:
            out.append(line[1:].lstrip())
        prev = q
    return out


@pytest.mark.parametrize("lang,name", CASES)
class TestEveryDocument:
    def test_title_line(self, lang, name):
        first = read(lang, name).splitlines()[0]
        assert first.startswith("# ") and "{{person_name}}" in first

    def test_back_link_to_hub_except_hub(self, lang, name):
        text = read(lang, name)
        if name.startswith("00-"):
            assert "{{doc_link_hub}}" not in text
        else:
            assert re.search(r"^\[← .+\]\(\{\{doc_link_hub\}\}\)$", text, re.M), "missing back-link to the hub"

    def test_exactly_one_what_this_is(self, lang, name):
        assert sum(c.startswith("ℹ️") for c in callouts(read(lang, name))) == 1

    def test_callouts_use_known_emojis(self, lang, name):
        for c in callouts(read(lang, name)):
            assert c.startswith(CALLOUT_EMOJIS), c[:30]

    def test_every_how_to_section_has_example_somewhere(self, lang, name):
        cs = callouts(read(lang, name))
        if any(c.startswith("💡") for c in cs) and not name.startswith("05-"):
            assert any(c.startswith("✍️") or "✍️" in c for c in cs) or "✍️" in read(lang, name)

    def test_only_known_placeholders(self, lang, name):
        used = set(re.findall(r"\{\{([a-zA-Z0-9_]+)\}\}", read(lang, name)))
        assert used <= ALLOWED_PLACEHOLDERS, used - ALLOWED_PLACEHOLDERS

    def test_no_unbalanced_braces(self, lang, name):
        text = read(lang, name)
        assert text.count("{{") == text.count("}}")

    def test_tables_are_rectangular(self, lang, name):
        rows = [ln for ln in read(lang, name).splitlines() if ln.lstrip().startswith("|")]
        blocks, cur = [], []
        for ln in read(lang, name).splitlines():
            if ln.lstrip().startswith("|"):
                cur.append(ln.count("|"))
            elif cur:
                blocks.append(cur)
                cur = []
        if cur:
            blocks.append(cur)
        for b in blocks:
            assert len(set(b)) == 1, f"table with uneven columns: {b}"
        assert rows is not None


@pytest.mark.parametrize("lang", LANGS)
class TestCareerHubDecisions:
    def test_hub_opens_with_biweekly_rhythm(self, lang):
        first_callout = callouts(read(lang, "00-career-hub.md"))[0]
        assert first_callout.startswith("🗓️") and "{{next_meeting_date}}" in read(lang, "00-career-hub.md")

    def test_hub_links_every_document(self, lang):
        text = read(lang, "00-career-hub.md")
        for key in ("one_on_one", "growth_plan", "focus_plan", "brag", "ladder", "review", "evidence", "onboarding"):
            assert f"{{{{doc_link_{key}}}}}" in text, key

    def test_growth_and_focus_plans_declare_they_are_alternatives(self, lang):
        growth, focus = read(lang, "02-growth-plan.md"), read(lang, "04-focus-plan.md")
        assert callouts(growth)[0].startswith("⚠️") and "{{doc_link_focus_plan}}" in growth
        assert callouts(focus)[0].startswith("⚠️") and "{{doc_link_growth_plan}}" in focus

    def test_one_on_one_has_the_four_parts_and_the_questions(self, lang):
        text = read(lang, "01-one-on-one-notes.md")
        assert len(re.findall(r"^## .*(Part|Parte) [1-4]", text, re.M)) == 4
        assert len(re.findall(r"^### [1-5]\. ", text, re.M)) == 5  # Working Agreement
        assert len(re.findall(r"^\*\*[1-7]\. ", text, re.M)) == 7  # Career Check

    def test_examples_cover_all_disciplines(self, lang):
        corpus = "".join(read(lang, n) for n in DOCS)
        for label in DISCIPLINE_LABELS[lang]:
            assert label in corpus, label

    def test_sbi_status_values_present(self, lang):
        text = read(lang, "01-one-on-one-notes.md")
        assert "SBI" in text
