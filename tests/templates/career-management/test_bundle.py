"""Contract tests for templates/career-management/bundle.yaml"""

import pytest
import yaml
from helpers import LANGS, TPL

pytestmark = pytest.mark.contract

BUNDLE = yaml.safe_load((TPL / "bundle.yaml").read_text(encoding="utf-8"))
DOCS = BUNDLE["documents"]


def test_ids_are_sequential_and_unique():
    assert [d["id"] for d in DOCS] == [f"{i:02d}" for i in range(len(DOCS))]
    assert len({d["key"] for d in DOCS}) == len(DOCS)


def test_exactly_one_hub_and_it_comes_first():
    hubs = [d for d in DOCS if d.get("hub")]
    assert len(hubs) == 1 and DOCS[0] is hubs[0]


@pytest.mark.parametrize("lang", LANGS)
def test_every_referenced_file_exists(lang):
    for d in DOCS:
        files = [d["template"]] if d["kind"] == "doc" else [d["text_fallback"]]
        for f in files:
            assert (TPL / lang / f).exists(), f
        if d["kind"] == "sheet":
            assert (TPL / d["spec"]).exists() and (TPL / lang / d["strings"]).exists()
        assert d["title"][lang].strip()


def test_every_template_is_in_the_bundle():
    in_bundle = {d.get("template") or d.get("text_fallback") for d in DOCS}
    on_disk = {p.name for p in (TPL / "en").glob("0*.md")}
    assert on_disk == in_bundle


def test_modes():
    for d in DOCS:
        assert set(d["modes"]) <= {"self", "lead"} and d["modes"]
    assert {d["key"] for d in DOCS if d.get("optional")} == {"evidence", "onboarding"}


@pytest.mark.parametrize("lang", LANGS)
def test_folder_title_has_person(lang):
    assert "{{person_name}}" in BUNDLE["folder_title"][lang]
