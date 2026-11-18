# 0003 — Spreadsheets are YAML specs built into .xlsx

**Status:** accepted

**Context.** The Ladder Assessment must work in Excel, Google Sheets and by hand, with dropdowns, formulas, colors and protection. Writing it per platform would mean three implementations.

**Decision.** Describe spreadsheets as a language-neutral YAML spec plus per-language strings, and build a single formatted `.xlsx` with `build_sheet.py` (openpyxl). Excel opens it natively; Google Drive converts it. Formulas are limited to functions that behave the same in both.

**Consequences.** New spreadsheets need only a spec. Features that don't survive Google conversion must not be used (verified in the release checklist).
