"""Tests for scripts/check_parity.py"""

import shutil

import pytest
from helpers import ROOT, load_script

cp = load_script("scripts/check_parity.py")

pytestmark = pytest.mark.unit


def fake_repo(tmp_path):
    shutil.copytree(ROOT / "templates", tmp_path / "templates")
    return tmp_path


class TestShape:
    def test_counts(self):
        s = cp.shape("# A\n## B\n| a |\n|---|\n> 💡 x\n> y\n\n> ✍️ z\n{{p}} {{p}} {{q}}")
        assert s["headings"] == [1, 2]
        assert s["table rows"] == 2
        assert s["callouts"] == ["💡", "✍️"]
        assert s["placeholders"] == {"p": 2, "q": 1}


def test_real_templates_are_in_parity(monkeypatch, capsys):
    cp.main()
    assert "parity ok" in capsys.readouterr().out


@pytest.mark.parametrize(
    "mutation",
    [
        lambda t: t.replace("{{person_name}}", "Ana", 1),  # placeholder dropped
        lambda t: t.replace("\n## ", "\n### ", 1),  # heading level changed
        lambda t: t.replace("> 💡", "> 🙂", 1),  # callout emoji changed
    ],
)
def test_detects_drift(tmp_path, monkeypatch, mutation):
    repo = fake_repo(tmp_path)
    f = repo / "templates" / "career-management" / "pt-BR" / "02-growth-plan.md"
    f.write_text(mutation(f.read_text(encoding="utf-8")), encoding="utf-8")
    monkeypatch.setattr(cp, "ROOT", repo)
    with pytest.raises(SystemExit):
        cp.main()


def test_detects_missing_file_and_yaml_keys(tmp_path, monkeypatch):
    repo = fake_repo(tmp_path)
    (repo / "templates" / "career-management" / "pt-BR" / "08-onboarding-plan.md").unlink()
    s = repo / "templates" / "career-management" / "pt-BR" / "05-ladder-assessment.strings.yaml"
    s.write_text(s.read_text(encoding="utf-8") + '\nextra_key: "x"\n', encoding="utf-8")
    monkeypatch.setattr(cp, "ROOT", repo)
    with pytest.raises(SystemExit):
        cp.main()
