"""Tests for scripts/validate_skills.py"""

import json
import shutil

import pytest
from helpers import ROOT, load_script

vs = load_script("scripts/validate_skills.py")

pytestmark = pytest.mark.unit


def fake_repo(tmp_path):
    for d in ("skills", ".claude-plugin", ".cursor-plugin"):
        shutil.copytree(ROOT / d, tmp_path / d)
    return tmp_path


def test_real_repo_is_valid(capsys):
    vs.main()
    assert "skills valid" in capsys.readouterr().out


def test_name_must_match_folder(tmp_path, monkeypatch):
    repo = fake_repo(tmp_path)
    f = repo / "skills" / "foundations" / "disciplines" / "SKILL.md"
    f.write_text(f.read_text(encoding="utf-8").replace("name: disciplines", "name: discipline"), encoding="utf-8")
    monkeypatch.setattr(vs, "ROOT", repo)
    with pytest.raises(SystemExit):
        vs.main()


def test_unlisted_skill_fails(tmp_path, monkeypatch):
    repo = fake_repo(tmp_path)
    new = repo / "skills" / "foundations" / "brand-new"
    new.mkdir()
    (new / "SKILL.md").write_text(
        "---\nname: brand-new\ndescription: A new skill that does a thing, used when testing.\n---\n", encoding="utf-8"
    )
    monkeypatch.setattr(vs, "ROOT", repo)
    with pytest.raises(SystemExit):
        vs.main()


def test_duplicate_names_across_categories_fail(tmp_path, monkeypatch):
    repo = fake_repo(tmp_path)
    shutil.copytree(repo / "skills" / "foundations" / "disciplines", repo / "skills" / "career-management" / "disciplines")
    manifest = repo / ".claude-plugin" / "plugin.json"
    data = json.loads(manifest.read_text())
    data["skills"].append("./skills/career-management/disciplines")
    manifest.write_text(json.dumps(data))
    monkeypatch.setattr(vs, "ROOT", repo)
    with pytest.raises(SystemExit):
        vs.main()


def test_manifest_versions_must_match(tmp_path, monkeypatch):
    repo = fake_repo(tmp_path)
    cursor = repo / ".cursor-plugin" / "plugin.json"
    data = json.loads(cursor.read_text())
    data["version"] = "9.9.9"
    cursor.write_text(json.dumps(data))
    monkeypatch.setattr(vs, "ROOT", repo)
    with pytest.raises(SystemExit):
        vs.main()


def test_missing_frontmatter_fails(tmp_path, monkeypatch):
    repo = fake_repo(tmp_path)
    (repo / "skills" / "foundations" / "disciplines" / "SKILL.md").write_text("# no frontmatter\n", encoding="utf-8")
    monkeypatch.setattr(vs, "ROOT", repo)
    with pytest.raises(SystemExit):
        vs.main()
