"""Contract tests for templates/career-management/05-ladder-assessment.sheet.yaml, its strings and the generic ladder."""

import re

import pytest
import yaml
from helpers import LANGS, TPL

pytestmark = pytest.mark.contract

_RAW = (TPL / "05-ladder-assessment.sheet.yaml").read_text(encoding="utf-8")
SPEC_TEXT = "\n".join(ln for ln in _RAW.splitlines() if not ln.lstrip().startswith("#"))  # ignore the docs header
SPEC = yaml.safe_load(_RAW)
PORTABLE = {"INDEX", "MATCH", "IF", "IFERROR", "COUNTIF", "AVERAGE", "ABS", "OR", "LEFT", "LEN"}


def strings(lang):
    return yaml.safe_load((TPL / lang / "05-ladder-assessment.strings.yaml").read_text(encoding="utf-8"))


def ladder(lang):
    return yaml.safe_load((TPL / lang / "generic-ladder.yaml").read_text(encoding="utf-8"))


@pytest.mark.parametrize("lang", LANGS)
def test_every_string_token_exists(lang):
    keys = set(re.findall(r"\[\[(?:q:)?([a-zA-Z0-9_]+)\]\]", SPEC_TEXT))
    missing = keys - set(strings(lang))
    assert not missing, missing


def test_only_portable_formula_functions():
    used = set(re.findall(r"\b([A-Z][A-Z0-9]+)\(", SPEC_TEXT))
    assert used <= PORTABLE, used - PORTABLE


def test_sheet_references_point_to_existing_keys():
    keys = {s["key"] for s in SPEC["sheets"]}
    assert set(re.findall(r"\{sheet:([a-z_]+)\}", SPEC_TEXT)) <= keys


def test_input_styles_are_unlocked_and_computed_locked():
    styles = SPEC["styles"]
    for name in ("input", "input_date", "input_link"):
        assert styles[name]["locked"] is False
    for name in ("computed", "computed_c", "computed_pct"):
        assert styles[name].get("locked", True) is True


def test_every_header_has_a_hover_tip():
    sheet = next(s for s in SPEC["sheets"] if s["key"] == "assessment")
    headers = [c for c in sheet["cells"] if c.get("style") == "header" and c["ref"] != "A14"]
    assert headers and all(c.get("note") for c in headers)


@pytest.mark.parametrize("lang", LANGS)
def test_scale_has_four_ordered_steps_plus_na(lang):
    s = strings(lang)
    values = [s[f"scale_{k}"] for k in ("1", "2", "3", "4", "na")]
    assert len(set(values)) == 5


@pytest.mark.parametrize("lang", LANGS)
class TestGenericLadder:
    def test_shape(self, lang):
        lad = ladder(lang)
        assert lad["source"] == "generic"
        assert len(lad["pillars"]) == 4 and len(lad["levels"]) == 5
        for lvl in lad["levels"]:
            assert len(lvl["expectations"]) == len(lad["pillars"])
            assert all(e.strip() for e in lvl["expectations"])

    def test_fits_the_sheet_limits(self, lang):
        m = next(s for s in SPEC["sheets"] if s["key"] == "ladder")["matrix"]
        lad = ladder(lang)
        assert len(lad["pillars"]) <= m["max_pillars"] and len(lad["levels"]) <= m["max_levels"]

    def test_every_pillar_has_a_meaning(self, lang):
        assert all(p["meaning"].strip() for p in ladder(lang)["pillars"])
