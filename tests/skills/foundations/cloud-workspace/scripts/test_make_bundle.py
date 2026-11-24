"""Tests for skills/foundations/cloud-workspace/scripts/make_bundle.py"""

import json
import re

import pytest
import yaml
from helpers import CW_SCRIPTS, LANGS, TPL, docx_text, load_script
from openpyxl import load_workbook

mb = load_script("skills/foundations/cloud-workspace/scripts/make_bundle.py")

BUNDLE = TPL / "bundle.yaml"
GUIDE = CW_SCRIPTS.parent / "assets"
CTX = {
    "person_name": "Ana Souza",
    "leader_name": "Morgan Lee",
    "role": "Designer",
    "discipline": "Design",
    "level": "Learning",
    "next_level": "Contributing",
    "start_date": "2026-11-18",
    "created_date": "2026-11-18",
    "next_meeting_date": "2026-12-02",
    "cycle": "2027 H1",
    "ladder_source": "Generic ladder",
}

pytestmark = pytest.mark.unit


def make(tmp_path, lang="en", mode="lead", fmt="files", include=(), with_sheet=False):
    return mb.make(
        BUNDLE,
        TPL,
        lang,
        mode,
        fmt,
        CTX,
        tmp_path / "out",
        include,
        TPL / lang / "generic-ladder.yaml",
        GUIDE / f"paste-guide.{lang}.md",
        with_sheet,
    )


class TestSelection:
    bundle = yaml.safe_load(BUNDLE.read_text(encoding="utf-8"))

    def keys(self, mode, include=()):
        return [d["key"] for d in mb.selected(self.bundle, mode, set(include))]

    def test_self_mode_has_no_leader_only_docs(self):
        assert self.keys("self") == ["hub", "one_on_one", "growth_plan", "brag", "focus_plan", "ladder"]

    def test_lead_mode_optional_docs_only_when_asked(self):
        assert "evidence" not in self.keys("lead")
        assert {"evidence", "onboarding"} <= set(self.keys("lead", ["evidence", "onboarding"]))

    def test_growth_and_focus_plans_always_together(self):
        for mode in ("self", "lead"):
            ks = self.keys(mode)
            assert "growth_plan" in ks and "focus_plan" in ks


class TestFilesFormat:
    def test_creates_docx_and_xlsx_hub_first(self, tmp_path):
        created = make(tmp_path)
        assert created[0].name == "00 - 🚀 Career Hub.docx"
        assert [p.suffix for p in created].count(".xlsx") == 1
        assert len(created) == 7

    def test_hub_links_every_document(self, tmp_path):
        created = make(tmp_path, include=["evidence", "onboarding"])
        hub = created[0]
        import zipfile

        rels = zipfile.ZipFile(hub).read("word/_rels/document.xml.rels").decode()
        for p in created[1:]:
            assert p.name in rels, p.name

    def test_no_placeholder_left(self, tmp_path):
        for p in make(tmp_path):
            if p.suffix == ".docx":
                assert "{{" not in docx_text(p), p.name

    def test_sheet_gets_person_and_generic_label(self, tmp_path):
        xlsx = next(p for p in make(tmp_path) if p.suffix == ".xlsx")
        ws = load_workbook(xlsx).worksheets[1]
        assert ws["C5"].value == "Ana Souza" and ws["C11"].value == "Generic ladder"


class TestManualFormat:
    @pytest.mark.parametrize("lang", LANGS)
    def test_markdown_and_paste_guide(self, tmp_path, lang):
        created = make(tmp_path, lang=lang, fmt="manual")
        names = [p.name for p in created]
        assert names[0] == "HOW-TO-PASTE.md" and names[1].startswith("00 - ")
        assert all(n.endswith(".md") for n in names)
        guide = created[0].read_text(encoding="utf-8")
        for n in names[1:]:
            assert n in guide

    def test_links_are_valid_markdown_with_spaces(self, tmp_path):
        hub = make(tmp_path, fmt="manual")[1].read_text(encoding="utf-8")
        assert "](<01 - 🎶 1-1 Notes.md>)" in hub
        assert not re.search(r"\]\([^<)][^)]* [^)]*\)", hub), "bare spaces inside a link"

    def test_no_placeholder_left(self, tmp_path):
        for p in make(tmp_path, fmt="manual", include=["evidence", "onboarding"]):
            assert "{{" not in p.read_text(encoding="utf-8"), p.name

    def test_sheet_is_text_fallback_unless_asked(self, tmp_path):
        assert any(p.name.startswith("05 - ") and p.suffix == ".md" for p in make(tmp_path, fmt="manual"))
        assert any(p.suffix == ".xlsx" for p in make(tmp_path / "x", fmt="manual", with_sheet=True))


def test_cli_prints_created_files(tmp_path, capsys):
    ctx = tmp_path / "c.json"
    ctx.write_text(json.dumps(CTX), encoding="utf-8")
    mb.main(
        [
            "--bundle",
            str(BUNDLE),
            "--templates",
            str(TPL),
            "--lang",
            "en",
            "--mode",
            "self",
            "--format",
            "manual",
            "--context",
            str(ctx),
            "--out",
            str(tmp_path / "o"),
            "--paste-guide",
            str(GUIDE / "paste-guide.en.md"),
        ]
    )
    files = json.loads(capsys.readouterr().out.strip().splitlines()[-1])
    assert len(files) == 7 and files[0].endswith("HOW-TO-PASTE.md")
