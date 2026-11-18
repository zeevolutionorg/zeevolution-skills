#!/usr/bin/env python3
"""Build a formatted .xlsx from a sheet spec (YAML) + strings (YAML) + optional data.

Usage:
  python3 build_sheet.py --spec SPEC.yaml --strings STRINGS.yaml --out OUT.xlsx \
      [--ladder LADDER.yaml|json] [--context CONTEXT.json]

The spec format is documented at the top of the spec files and in
skills/foundations/cloud-workspace/SHEETS.md. Requires: openpyxl, pyyaml.
The output opens in Excel and converts to Google Sheets on upload.
"""
import argparse
import json
import re
import sys

try:
    import yaml
    from openpyxl import Workbook
    from openpyxl.chart import BarChart, Reference
    from openpyxl.comments import Comment
    from openpyxl.formatting.rule import CellIsRule, FormulaRule
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Protection, Side
    from openpyxl.utils import column_index_from_string, get_column_letter
    from openpyxl.utils.cell import coordinate_from_string, range_boundaries
    from openpyxl.workbook.defined_name import DefinedName
    from openpyxl.worksheet.datavalidation import DataValidation
except ImportError as exc:  # pragma: no cover
    sys.exit(f"Missing dependency: {exc}. Install with: pip install openpyxl pyyaml")

THIN = Side(style="thin", color="D1D5DB")


def load(path):
    with open(path, encoding="utf-8") as fh:
        if path.endswith(".json"):
            return json.load(fh)
        return yaml.safe_load(fh)


class Tokens:
    """Resolves [[key]], [[q:key]], {sheet:key}, {{ctx}}, {i}/{r} tokens."""

    def __init__(self, strings, context, sheet_names):
        self.strings = strings or {}
        self.context = context or {}
        self.sheet_names = sheet_names

    def _str(self, key):
        if key not in self.strings:
            raise KeyError(f"missing string: {key}")
        return str(self.strings[key])

    def resolve(self, text, i=None, r=None):
        if text is None or not isinstance(text, str):
            return text
        out = re.sub(r"\[\[q:([a-zA-Z0-9_]+)\]\]",
                     lambda m: '"' + self._str(m.group(1)).replace('"', '""') + '"', text)
        out = re.sub(r"\[\[([a-zA-Z0-9_]+)\]\]", lambda m: self._str(m.group(1)), out)
        out = re.sub(r"\{sheet:([a-z_]+)\}",
                     lambda m: "'" + self.sheet_names[m.group(1)].replace("'", "''") + "'", out)
        out = re.sub(r"\{\{([a-zA-Z0-9_]+)\}\}",
                     lambda m: str(self.context.get(m.group(1), "") or ""), out)
        if i is not None:
            def arith(m):
                expr = m.group(1).replace("i", str(i)).replace("r", str(r))
                if not re.fullmatch(r"[0-9+\-* ]+", expr):
                    return m.group(0)
                return str(eval(expr))  # noqa: S307 - digits and + - * only
            out = re.sub(r"\{([ir][0-9+\-* ]*)\}", arith, out)
        return out


def make_style(defn):
    defn = defn or {}
    font = defn.get("font", {})
    align = defn.get("align", {})
    return {
        "font": Font(bold=font.get("bold", False), italic=font.get("italic", False),
                     size=font.get("size", 10), color=font.get("color", "111827"),
                     underline="single" if font.get("underline") else None, name="Arial"),
        "fill": PatternFill("solid", fgColor=defn["fill"]) if defn.get("fill") else None,
        "border": Border(left=THIN, right=THIN, top=THIN, bottom=THIN) if defn.get("border") else None,
        "alignment": Alignment(horizontal=align.get("h"), vertical=align.get("v"),
                               wrap_text=align.get("wrap", False)),
        "number_format": defn.get("number_format"),
        "locked": defn.get("locked", True),
    }


def apply_style(cell, style, extra=None):
    extra = extra or {}
    if style:
        cell.font = style["font"]
        if style["fill"]:
            cell.fill = style["fill"]
        if style["border"]:
            cell.border = style["border"]
        cell.alignment = style["alignment"]
        if style["number_format"]:
            cell.number_format = style["number_format"]
        cell.protection = Protection(locked=style["locked"])
    if extra.get("fill"):
        cell.fill = PatternFill("solid", fgColor=extra["fill"])
    if extra.get("number_format"):
        cell.number_format = extra["number_format"]


def style_range(ws, top_left, bottom_right, style):
    min_col, min_row, max_col, max_row = range_boundaries(f"{top_left}:{bottom_right}")
    for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
        for cell in row:
            apply_style(cell, style)


class Builder:
    def __init__(self, spec, strings, context, ladder):
        self.spec = spec
        self.ladder = ladder
        self.sheet_names = {s["key"]: Tokens(strings, {}, {}).resolve(s["name"]) for s in spec["sheets"]}
        self.tok = Tokens(strings, context, self.sheet_names)
        self.styles = {k: make_style(v) for k, v in (spec.get("styles") or {}).items()}
        self.wb = Workbook()
        self.wb.remove(self.wb.active)
        self.validations = {}

    # -- cells -------------------------------------------------------------
    def write_cell(self, ws, ref, c, i=None, r=None):
        cell = ws[ref]
        if "f" in c:
            cell.value = self.tok.resolve(c["f"], i, r)
        elif "v" in c:
            val = self.tok.resolve(c["v"], i, r)
            if isinstance(val, str) and re.fullmatch(r"-?\d+", val):
                val = int(val)
            cell.value = val if val != "" else None
        style = self.styles.get(c.get("style"))
        apply_style(cell, style, c)
        if c.get("merge"):
            end = self.tok.resolve(c["merge"], i, r)
            ws.merge_cells(f"{ref}:{end}")
            style_range(ws, ref, end, style)
        if c.get("note"):
            cell.comment = Comment(self.tok.resolve(c["note"], i, r), "zeevolution-skills")
            cell.comment.width, cell.comment.height = 320, 120
        if c.get("link"):
            url = self.tok.resolve(c["link"], i, r)
            if url:
                cell.hyperlink = url
        if c.get("validation"):
            self.add_validation(ws, ref, c["validation"], i, r)

    def add_validation(self, ws, ref, v, i=None, r=None):
        if "list_name" in v:
            key = ("list", v["list_name"])
            formula = f"={v['list_name']}"
            kind = dict(type="list", formula1=formula, allow_blank=True)
        elif "custom" in v:
            # custom formulas are relative to the top-left cell; group by repeat column
            formula = self.tok.resolve(v["custom"], i, r)
            col = re.match(r"[A-Z]+", ref).group(0)
            key = ("custom", col)
            kind = dict(type="custom", formula1=formula.lstrip("="), allow_blank=True)
        elif v.get("date"):
            key = ("date", ref)
            kind = dict(type="date", operator="greaterThan", formula1="DATE(2000,1,1)", allow_blank=True)
        else:
            return
        full_key = (ws.title,) + key
        dv = self.validations.get(full_key)
        if dv is None:
            dv = DataValidation(**kind)
            dv.error = self.tok.strings.get("validation_error", "Please pick a value from the list or follow the hint.")
            dv.errorTitle = "zeevolution-skills"
            dv.showErrorMessage = kind["type"] == "list"
            ws.add_data_validation(dv)
            self.validations[full_key] = dv
        dv.add(ref)

    # -- blocks ------------------------------------------------------------
    def write_matrix(self, ws, m):
        lad = self.ladder or {"pillars": [], "levels": []}
        pillars = lad.get("pillars", [])[: m["max_pillars"]]
        levels = lad.get("levels", [])[: m["max_levels"]]
        pc, pr = coordinate_from_string(m["pillars_at"])
        lc, lr = coordinate_from_string(m["levels_at"])
        bc, br = coordinate_from_string(m["body_at"])
        pci, lci, bci = map(column_index_from_string, (pc, lc, bc))
        head, lvl, body = (self.styles[m[k]] for k in ("head_style", "level_style", "body_style"))
        for j in range(m["max_pillars"]):
            cell = ws.cell(row=pr, column=pci + j)
            cell.value = pillars[j]["name"] if j < len(pillars) else None
            apply_style(cell, head)
        for k in range(m["max_levels"]):
            cell = ws.cell(row=lr + k, column=lci)
            cell.value = levels[k]["name"] if k < len(levels) else None
            apply_style(cell, lvl)
            ws.row_dimensions[lr + k].height = m.get("body_row_height", 45)
            exps = levels[k].get("expectations", []) if k < len(levels) else []
            for j in range(m["max_pillars"]):
                c = ws.cell(row=br + k, column=bci + j)
                c.value = exps[j] if j < len(exps) else None
                apply_style(c, body)
        if m.get("meanings_at"):
            ws[m["meanings_title_at"]] = self.tok.resolve(m["meanings_title"])
            apply_style(ws[m["meanings_title_at"]], self.styles.get("section"))
            mc, mr = coordinate_from_string(m["meanings_at"])
            mci = column_index_from_string(mc)
            last = get_column_letter(bci + m["max_pillars"] - 1)
            for j, p in enumerate(pillars):
                a = ws.cell(row=mr + j, column=mci, value=p["name"])
                apply_style(a, self.styles.get("label"))
                b = ws.cell(row=mr + j, column=mci + 1, value=p.get("meaning", ""))
                ws.merge_cells(f"{get_column_letter(mci + 1)}{mr + j}:{last}{mr + j}")
                apply_style(b, self.styles.get(m.get("meanings_style")))

    def write_cond_formats(self, ws, cfs):
        for cf in cfs or []:
            rng = cf["range"]
            first = rng.split(":")[0]
            for rule in cf.get("rules", []):
                fill = PatternFill("solid", fgColor=rule["fill"], bgColor=rule["fill"])
                font = Font(color=rule["font"], bold=True) if rule.get("font") else None
                if "equals" in rule:
                    lit = '"' + self.tok.resolve(rule["equals"]).replace('"', '""') + '"'
                    ws.conditional_formatting.add(
                        rng, CellIsRule(operator="equal", formula=[lit], fill=fill, font=font))
                elif "formula" in rule:
                    ws.conditional_formatting.add(
                        rng, FormulaRule(formula=[self.tok.resolve(rule["formula"])], fill=fill, font=font))
            _ = first

    def write_charts(self, ws, charts):
        for ch in charts or []:
            chart = BarChart()
            chart.type = "col"
            chart.title = self.tok.resolve(ch["title"])
            chart.y_axis.scaling.min = ch.get("y_min")
            chart.y_axis.scaling.max = ch.get("y_max")
            chart.y_axis.majorUnit = 1
            dmin_c, dmin_r, dmax_c, dmax_r = range_boundaries(ch["data"])
            cmin_c, cmin_r, cmax_c, cmax_r = range_boundaries(ch["cats"])
            data = Reference(ws, min_col=dmin_c, min_row=dmin_r, max_col=dmax_c, max_row=dmax_r)
            cats = Reference(ws, min_col=cmin_c, min_row=cmin_r, max_col=cmax_c, max_row=cmax_r)
            chart.add_data(data, titles_from_data=True)
            chart.set_categories(cats)
            chart.width, chart.height = ch.get("width", 15), ch.get("height", 7.5)
            ws.add_chart(chart, ch["anchor"])

    # -- sheets ------------------------------------------------------------
    def build(self):
        for wdef in self.spec["sheets"]:
            ws = self.wb.create_sheet(self.sheet_names[wdef["key"]])
            if wdef.get("tab_color"):
                ws.sheet_properties.tabColor = wdef["tab_color"]
            for col, w in (wdef.get("col_widths") or {}).items():
                ws.column_dimensions[col].width = w
            for row, h in (wdef.get("row_heights") or {}).items():
                ws.row_dimensions[int(row)].height = h
            rh = wdef.get("rows_height_range")
            if rh:
                for row in range(rh["from"], rh["to"] + 1):
                    ws.row_dimensions[row].height = rh["height"]
            if wdef.get("fill_range"):
                a, b = wdef["fill_range"]["range"].split(":")
                style_range(ws, a, b, self.styles[wdef["fill_range"]["style"]])
            for c in wdef.get("cells", []):
                self.write_cell(ws, c["ref"], c)
            rep = wdef.get("repeat")
            if rep:
                for n in range(rep["count"]):
                    i, r = n + 1, rep["start_row"] + n
                    for c in rep["cells"]:
                        self.write_cell(ws, f"{c['col']}{r}", c, i, r)
            if wdef.get("matrix"):
                self.write_matrix(ws, wdef["matrix"])
            self.write_cond_formats(ws, wdef.get("cond_formats"))
            self.write_charts(ws, wdef.get("charts"))
            if wdef.get("freeze"):
                ws.freeze_panes = wdef["freeze"]
            if wdef.get("landscape"):
                ws.page_setup.orientation = "landscape"
                ws.page_setup.fitToWidth = 1
                ws.sheet_properties.pageSetUpPr.fitToPage = True
            ws.sheet_view.showGridLines = False
            if wdef.get("hidden"):
                ws.sheet_state = "hidden"
            if wdef.get("protect"):
                ws.protection.sheet = True  # no password: users can unprotect if they need to
                ws.protection.formatColumns = False
                ws.protection.formatRows = False
            if wdef.get("active"):
                self.wb.active = self.wb.index(ws)
        for name, ref in (self.spec.get("workbook", {}).get("defined_names") or {}).items():
            dn = DefinedName(name, attr_text=self.tok.resolve(ref))
            try:
                self.wb.defined_names[name] = dn
            except TypeError:  # older openpyxl
                self.wb.defined_names.append(dn)
        props = self.wb.properties
        props.creator = props.lastModifiedBy = "zeevolution-skills"
        props.title = self.tok.resolve(self.spec.get("title", "")) or None
        props.company = None
        return self.wb


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--strings", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ladder")
    ap.add_argument("--context")
    args = ap.parse_args(argv)
    spec = load(args.spec)
    strings = load(args.strings)
    ladder = load(args.ladder) if args.ladder else None
    context = load(args.context) if args.context else {}
    if ladder and "ladder_source_label" not in context:
        context["ladder_source_label"] = strings["src_generic"] if ladder.get("source") == "generic" else strings["src_company"]
    wb = Builder(spec, strings, context, ladder).build()
    wb.save(args.out)
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
