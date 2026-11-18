"""Tests for skills/foundations/cloud-workspace/scripts/build_sheet.py"""

import subprocess

import pytest
import yaml
from helpers import LANGS, TPL, load_script
from openpyxl import load_workbook

bs = load_script("skills/foundations/cloud-workspace/scripts/build_sheet.py")

SPEC = TPL / "05-ladder-assessment.sheet.yaml"


def build(tmp_path, lang="en", ctx=None, ladder=True):
    out = tmp_path / f"ladder-{lang}.xlsx"
    args = ["--spec", str(SPEC), "--strings", str(TPL / lang / "05-ladder-assessment.strings.yaml"), "--out", str(out)]
    if ladder:
        args += ["--ladder", str(TPL / lang / "generic-ladder.yaml")]
    if ctx:
        args += ["--context", str(ctx)]
    bs.main(args)
    return out


@pytest.mark.unit
class TestTokens:
    def tok(self):
        return bs.Tokens({"a": 'say "hi"', "b": "B"}, {"person_name": "Ana"}, {"assessment": "✍️ Assessment"})

    def test_string_and_quoted_string(self):
        t = self.tok()
        assert t.resolve("[[b]]") == "B"
        assert t.resolve("=[[q:a]]") == '="say ""hi"""'

    def test_sheet_names_are_quoted(self):
        assert self.tok().resolve("{sheet:assessment}!A1") == "'✍️ Assessment'!A1"

    def test_context_and_missing_context(self):
        t = self.tok()
        assert t.resolve("{{person_name}}") == "Ana"
        assert t.resolve("{{role}}") == ""

    def test_repeat_arithmetic(self):
        assert self.tok().resolve("B{r+11}:{i}", i=2, r=5) == "B16:2"

    def test_missing_string_raises(self):
        with pytest.raises(KeyError):
            self.tok().resolve("[[nope]]")


@pytest.mark.unit
class TestWorkbook:
    @pytest.mark.parametrize("lang", LANGS)
    def test_tabs_and_hidden_lists(self, tmp_path, lang):
        wb = load_workbook(build(tmp_path, lang))
        assert len(wb.sheetnames) == 6
        assert wb.worksheets[-1].sheet_state == "hidden"
        assert wb.active.title == wb.worksheets[1].title  # Assessment opens first

    def test_context_fills_header(self, tmp_path, ctx_file):
        ws = load_workbook(build(tmp_path, ctx=ctx_file)).worksheets[1]
        assert ws["C5"].value == "Ana Souza"
        assert ws["C8"].value == "Contributing"
        assert ws["C11"].value == "Generic ladder"  # derived from the generic ladder

    def test_inputs_unlocked_and_computed_locked(self, tmp_path):
        ws = load_workbook(build(tmp_path)).worksheets[1]
        assert ws.protection.sheet is True
        assert ws["E15"].protection.locked is False  # self score: input
        assert ws["C15"].protection.locked is True  # expectation: computed

    def test_dropdowns_exist(self, tmp_path):
        ws = load_workbook(build(tmp_path)).worksheets[1]
        formulas = {dv.formula1 for dv in ws.data_validations.dataValidation}
        assert {"=ScaleAll", "=Levels", "=Disciplines", "=LadderSources"} <= formulas

    def test_defined_names_and_chart(self, tmp_path):
        wb = load_workbook(build(tmp_path))
        assert {"ScaleAll", "Scale4", "Levels"} <= set(wb.defined_names.keys())
        assert len(wb.worksheets[2]._charts) == 1

    def test_ladder_matrix_written(self, tmp_path):
        ws = load_workbook(build(tmp_path)).worksheets[3]
        lad = yaml.safe_load((TPL / "en" / "generic-ladder.yaml").read_text(encoding="utf-8"))
        assert ws["B4"].value == lad["pillars"][0]["name"]
        assert ws["A5"].value == lad["levels"][0]["name"]
        assert ws["B5"].value == lad["levels"][0]["expectations"][0]

    def test_without_ladder_the_matrix_is_empty(self, tmp_path):
        ws = load_workbook(build(tmp_path, ladder=False)).worksheets[3]
        assert ws["B4"].value is None and ws["A5"].value is None

    def test_metadata_is_neutral(self, tmp_path):
        wb = load_workbook(build(tmp_path))
        assert wb.properties.creator == "zeevolution-skills"


@pytest.mark.libreoffice
@pytest.mark.parametrize("lang", LANGS)
def test_formulas_recalculate(tmp_path, soffice, lang, ctx_file):
    """Fill scores like a user would, let LibreOffice recalculate, and read the results back."""
    strings = yaml.safe_load((TPL / lang / "05-ladder-assessment.strings.yaml").read_text(encoding="utf-8"))
    lad = yaml.safe_load((TPL / lang / "generic-ladder.yaml").read_text(encoding="utf-8"))
    path = build(tmp_path, lang)
    wb = load_workbook(path)
    ws = wb.worksheets[1]
    ws["C8"], ws["C9"] = lad["levels"][1]["name"], lad["levels"][2]["name"]
    ws["E15"], ws["F15"] = strings["scale_2"], strings["scale_3"]
    ws["E16"], ws["F16"] = strings["scale_1"], strings["scale_4"]
    wb.save(path)
    out = tmp_path / "calc"
    subprocess.run(
        [soffice, "--headless", "--convert-to", "xlsx", "--outdir", str(out), str(path)],
        check=True,
        capture_output=True,
        timeout=180,
    )
    calc = load_workbook(out / path.name, data_only=True)
    a, s = calc.worksheets[1], calc.worksheets[2]
    assert a["B15"].value == lad["pillars"][0]["name"]
    assert a["C15"].value == lad["levels"][1]["expectations"][0]
    assert a["D15"].value == lad["levels"][2]["expectations"][0]
    assert a["G15"].value == 1 and a["H15"].value in (None, "")
    assert a["G16"].value == 3 and a["H16"].value == strings["flag_talk"]
    assert a["N16"].value == "✅"
    assert s["B13"].value == 1 and s["B14"].value == 2
    assert s["B16"].value == strings["ready_close"]
