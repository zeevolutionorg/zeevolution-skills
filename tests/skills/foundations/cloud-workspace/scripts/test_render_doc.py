"""Tests for skills/foundations/cloud-workspace/scripts/render_doc.py"""

import zipfile

import pytest
from helpers import LANGS, TPL, docx_text, load_script

rd = load_script("skills/foundations/cloud-workspace/scripts/render_doc.py")

pytestmark = pytest.mark.unit


class TestFill:
    def test_replaces_known_placeholders(self):
        assert rd.fill("Hi {{person_name}}", {"person_name": "Ana"}, False) == "Hi Ana"

    def test_unknown_placeholder_becomes_empty_by_default(self):
        assert rd.fill("[{{nope}}]", {}, False) == "[]"

    def test_keep_missing_keeps_unknown_placeholders(self):
        assert rd.fill("[{{nope}}]", {}, True) == "[{{nope}}]"

    def test_empty_value_counts_as_missing(self):
        assert rd.fill("{{a}}", {"a": ""}, True) == "{{a}}"


class TestParseBlocks:
    def blocks(self, text):
        return list(rd.parse_blocks(text.splitlines()))

    def test_headings_paragraphs_rules(self):
        kinds = [k for k, _ in self.blocks("# T\n\nsome text\n\n---\n## S")]
        assert kinds == ["h", "p", "hr", "h"]

    def test_table_with_header(self):
        ((_, (has_header, rows)),) = self.blocks("| a | b |\n|---|---|\n| 1 | 2 |")
        assert has_header and rows == [["a", "b"], ["1", "2"]]

    def test_key_value_table_without_header(self):
        ((_, (has_header, rows)),) = self.blocks("| | |\n|---|---|\n| **k** | v |")
        assert not has_header and rows == [["**k**", "v"]]

    def test_list_levels_and_continuation_lines(self):
        ((_, items),) = self.blocks("- one\n  more\n  - two\n1. three")
        assert items[0] == [0, False, "one\nmore"]
        assert items[1][0] == 1
        assert items[2][1] is True

    def test_callouts_split_into_one_box_each(self):
        quotes = [v for k, v in self.blocks("> 💡 how\n>\n> ✍️ example") if k == "quote"]
        assert len(quotes) == 2 and quotes[1][0].startswith("✍️")

    def test_multiline_callout_stays_together(self):
        quotes = [v for k, v in self.blocks("> 🗓️ rhythm\n> 1. a\n> 2. b") if k == "quote"]
        assert len(quotes) == 1 and len(quotes[0]) == 3


class TestInline:
    def test_tokens(self):
        toks = list(rd.inline_tokens("a **b** *c* `d` [e](f)"))
        assert ("b", "b") in toks and ("i", "c") in toks and ("c", "d") in toks and ("a", ("e", "f")) in toks

    def test_angle_bracket_links_are_unwrapped(self):
        ((_, (label, url)),) = [t for t in rd.inline_tokens("[x](<01 - a b.md>)") if t[0] == "a"]
        assert url == "01 - a b.md"

    def test_checkbox(self):
        assert rd.checkbox("[ ] todo") == "☐ todo"
        assert rd.checkbox("[x] done") == "☑ done"


class TestOutputs:
    @pytest.mark.parametrize("lang", LANGS)
    @pytest.mark.parametrize("name", sorted(p.name for p in (TPL / "en").glob("0*.md")))
    def test_every_template_renders_to_docx(self, tmp_path, ctx_file, lang, name):
        out = tmp_path / "out.docx"
        rd.main(["--in", str(TPL / lang / name), "--out", str(out), "--context", str(ctx_file)])
        text = docx_text(out)
        assert "{{" not in text.replace("{{doc_link", "")  # only sibling links may be unset here
        assert "Ana Souza" in text

    def test_docx_metadata_is_neutral(self, tmp_path, ctx_file):
        out = tmp_path / "o.docx"
        rd.main(["--in", str(TPL / "en" / "00-career-hub.md"), "--out", str(out), "--context", str(ctx_file)])
        core = zipfile.ZipFile(out).read("docProps/core.xml").decode()
        assert "<dc:creator>zeevolution-skills</dc:creator>" in core

    def test_external_links_become_hyperlinks(self, tmp_path, ctx_file):
        out = tmp_path / "o.docx"
        rd.main(["--in", str(TPL / "en" / "01-one-on-one-notes.md"), "--out", str(out), "--context", str(ctx_file)])
        rels = zipfile.ZipFile(out).read("word/_rels/document.xml.rels").decode()
        assert "https://example.com/hub" in rels

    def test_html_and_md_outputs(self, tmp_path, ctx_file):
        src = TPL / "en" / "02-growth-plan.md"
        rd.main(["--in", str(src), "--out", str(tmp_path / "o.html"), "--context", str(ctx_file)])
        rd.main(["--in", str(src), "--out", str(tmp_path / "o.md"), "--context", str(ctx_file)])
        html = (tmp_path / "o.html").read_text(encoding="utf-8")
        assert "<h1>" in html and "Ana Souza" in html and "border-left" in html
        assert (tmp_path / "o.md").read_text(encoding="utf-8").startswith("# 🌱 Growth Plan — Ana Souza")
