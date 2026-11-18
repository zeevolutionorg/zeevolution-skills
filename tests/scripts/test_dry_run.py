"""Tests for scripts/dry_run.py — the end-to-end run of /career-hub-toolkit (Files + Manual adapters)."""

import pytest
from helpers import load_script

dr = load_script("scripts/dry_run.py")

pytestmark = pytest.mark.e2e


def test_full_dry_run_passes(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["dry_run.py", "--out", str(tmp_path)])
    dr.main()
    out = capsys.readouterr().out
    assert out.count(" ok") >= 32 and "FAIL" not in out
    assert (tmp_path / "manual" / "en" / "lead" / "Ana_Souza" / "HOW-TO-PASTE.md").exists()
    assert len(list((tmp_path / "files" / "pt-BR" / "self" / "Carla_Mendes").iterdir())) == 6


def test_dry_run_detects_a_broken_template(tmp_path, monkeypatch):
    """If a template references a placeholder nobody fills, the dry run must fail."""
    import shutil

    tpl = tmp_path / "tpl"
    shutil.copytree(dr.TPL, tpl)
    f = tpl / "en" / "03-brag-document.md"
    f.write_text(f.read_text(encoding="utf-8") + "\n{{unknown_field}}\n", encoding="utf-8")
    monkeypatch.setattr(dr, "TPL", tpl)

    def keep_missing(text, ctx, keep):  # simulate a renderer that keeps unknowns
        return dr.make_bundle.render_doc.PLACEHOLDER.sub(lambda m: str(ctx.get(m.group(1), m.group(0)) or m.group(0)), text)

    monkeypatch.setattr(dr.make_bundle.render_doc, "fill", keep_missing)
    problems = dr.run_one(dr.PERSONAS[0], "self", "en", "manual", tmp_path / "o")
    assert any("leftover" in p for p in problems)
