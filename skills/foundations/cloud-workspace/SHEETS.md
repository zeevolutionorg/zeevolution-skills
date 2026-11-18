# Sheet specs

Spreadsheets in zeevolution-skills are described as **YAML specs** and built by `scripts/build_sheet.py` into a formatted `.xlsx`. The same `.xlsx` works in Excel and converts to Google Sheets. A new skill that needs a spreadsheet writes a spec; it never writes a new script.

## Files

- `<name>.sheet.yaml` — structure: tabs, cells, styles, validations, formulas, conditional colors, charts. Language-neutral.
- `<lang>/<name>.strings.yaml` — every visible word, one file per language.
- Optional data file (e.g. a ladder) passed with `--ladder`.

## Tokens inside the spec

| Token | Becomes |
|---|---|
| `[[key]]` | the string `key` from the strings file |
| `[[q:key]]` | the same string as a quoted formula literal (`"..."`) |
| `{sheet:key}` | the quoted name of the tab with that key, e.g. `'✍️ Assessment'` |
| `{{name}}` | a context value (`person_name`, `role`, …); empty if not given |
| `{i}`, `{r}`, `{r+11}` | repeat index / row number, simple arithmetic allowed |

## Building blocks

- `styles:` named styles (`font`, `fill`, `border`, `align`, `number_format`, `locked`). Use **`locked: false` for input cells**; everything else stays protected.
- `sheets[]:` `key`, `name`, `tab_color`, `col_widths`, `row_heights`, `freeze`, `protect`, `hidden`, `landscape`, `active`.
- `cells[]:` `ref`, `v` (value) or `f` (formula), `style`, `merge`, `note` (hover tip), `link`, `validation` (`list_name`, `custom`, `date`), `fill`, `number_format`.
- `repeat:` `count`, `start_row`, `cells[]` with `col` instead of `ref`.
- `matrix:` writes a data grid (used for the career ladder: pillars × levels + meanings).
- `fill_range:` styles an empty input area.
- `cond_formats[]:` `range` + `rules[]` (`equals` text or `formula`) with `fill` / `font` colors.
- `charts[]:` bar charts from a data range.
- `workbook.defined_names:` named ranges used by validations and formulas.

## Design rules

1. **Inputs look like inputs:** light yellow fill, thin border, unlocked. **Computed cells look read-only:** light grey, protected.
2. Every column header has a `note` with "what to put here" and a one-line example.
3. Colors always come with text (colorblind-safe): never rely on color alone.
4. **Portable formulas only:** `INDEX`, `MATCH`, `IF`, `IFERROR`, `COUNTIF`, `AVERAGE`, `ABS`, `OR`, `LEFT`. No Excel-only or Sheets-only functions.
5. Protect sheets **without a password**, so users can unprotect if they really need to.
6. One "How to use" tab first; a hidden "Lists" tab for dropdown values.
