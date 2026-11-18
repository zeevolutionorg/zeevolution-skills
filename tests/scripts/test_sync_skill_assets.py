"""Tests for scripts/sync_skill_assets.py"""

import shutil

import pytest
from helpers import ROOT, load_script

sa = load_script("scripts/sync_skill_assets.py")

pytestmark = pytest.mark.unit


def point_to(module, repo, monkeypatch):
    monkeypatch.setattr(module, "ROOT", repo)
    monkeypatch.setattr(module, "TPL", repo / "templates" / "career-management")
    monkeypatch.setattr(module, "SHARED_SCRIPTS", repo / "skills" / "foundations" / "cloud-workspace" / "scripts")
    monkeypatch.setattr(module, "SHARED_ASSETS", repo / "skills" / "foundations" / "cloud-workspace" / "assets")
    monkeypatch.setattr(module, "TOOLKIT", repo / "skills" / "career-management" / "career-hub-toolkit")
    monkeypatch.setattr(module, "LADDER_SKILL", repo / "skills" / "career-management" / "career-ladder")


@pytest.fixture
def repo(tmp_path, monkeypatch):
    for d in ("templates", "skills"):
        shutil.copytree(ROOT / d, tmp_path / d)
    point_to(sa, tmp_path, monkeypatch)
    return tmp_path


def test_real_repo_is_in_sync(monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["sync", "--check"])
    sa.main()
    assert "in sync" in capsys.readouterr().out


def test_check_fails_when_a_copy_drifts(repo, monkeypatch):
    copy = repo / "skills" / "career-management" / "career-hub-toolkit" / "scripts" / "render_doc.py"
    copy.write_text(copy.read_text(encoding="utf-8") + "\n# edited by hand\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["sync", "--check"])
    with pytest.raises(SystemExit):
        sa.main()


def test_sync_repairs_drift(repo, monkeypatch, capsys):
    copy = repo / "skills" / "career-management" / "career-hub-toolkit" / "assets" / "templates" / "en" / "00-career-hub.md"
    copy.write_text("stale", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["sync"])
    sa.main()
    monkeypatch.setattr("sys.argv", ["sync", "--check"])
    sa.main()
    assert "in sync" in capsys.readouterr().out


def test_generic_ladder_markdown_has_both_languages():
    md = sa.generic_ladder_md()
    assert "(en)" in md and "(pt-BR)" in md and "| **Learning** |" in md
