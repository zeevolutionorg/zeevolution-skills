"""Tests for scripts/build.py (release assets)."""

import zipfile

import pytest
from helpers import load_script

build = load_script("scripts/build.py")

pytestmark = pytest.mark.e2e


@pytest.fixture(scope="module")
def dist(tmp_path_factory):
    out = tmp_path_factory.mktemp("dist")
    mp = pytest.MonkeyPatch()
    mp.setattr("sys.argv", ["build.py", "--out", str(out)])
    build.main()
    mp.undo()
    return out


@pytest.mark.parametrize("lang", ["en", "pt-BR"])
def test_manual_kit_contents(dist, lang):
    names = zipfile.ZipFile(dist / f"career-management-kit-{lang}.zip").namelist()
    assert not any(c in n for n in names for c in '":<>|*?\r\n')
    # START-HERE is a PDF when LibreOffice is installed, and a .docx otherwise.
    documents = [n for n in names if n.endswith(".docx") and not n.endswith("START-HERE.docx")]
    assert len(documents) == 8  # every document except the spreadsheet
    assert sum(n.endswith(".xlsx") for n in names) == 1
    assert sum(n.endswith(".md") for n in names) == 9  # incl. the spreadsheet's text fallback
    assert sum(n.endswith("START-HERE.pdf") or n.endswith("START-HERE.docx") for n in names) == 1


def test_kit_keeps_placeholders_for_manual_use(dist):
    kit = dist / "career-management-kit-en" / "word"
    hub = next(kit.glob("00 - *.docx"))
    assert "{{person_name}}" in zipfile.ZipFile(hub).read("word/document.xml").decode()


def test_one_skill_file_per_skill(dist):
    skills = sorted(p.stem for p in (dist / "skills").glob("*.skill"))
    assert skills == sorted(
        [
            "career-hub-toolkit",
            "career-ladder",
            "cloud-workspace",
            "create-adr",
            "disciplines",
            "doc-templates",
            "service-handoff",
            "setup-zeevolution-skills",
            "strong-programmer",
        ]
    )


def test_skill_files_are_self_contained(dist):
    names = zipfile.ZipFile(dist / "skills" / "career-hub-toolkit.skill").namelist()
    for required in (
        "career-hub-toolkit/SKILL.md",
        "career-hub-toolkit/INTERVIEW.md",
        "career-hub-toolkit/scripts/make_bundle.py",
        "career-hub-toolkit/assets/templates/bundle.yaml",
        "career-hub-toolkit/assets/paste-guide.pt-BR.md",
    ):
        assert required in names, required


def test_all_skills_zip(dist):
    assert len(zipfile.ZipFile(dist / "zeevolution-skills-all-skills.zip").namelist()) == 9


def test_file_names_come_from_bundle():
    assert build.FILE_NAMES["en"]["00"] == "🚀 Career Hub"
    assert build.FILE_NAMES["pt-BR"]["02"] == "🌱 PDI"
