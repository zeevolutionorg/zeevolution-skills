#!/usr/bin/env python3
"""Check that every language version of every template has the same structure.

Compares, per file: heading levels in order, table row count, callout emojis in order,
and the multiset of {{placeholders}}. YAML strings files must have the same keys.

  python3 scripts/check_parity.py
"""

import re
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
BASE = "en"
CALLOUTS = ("🗓️", "ℹ️", "💡", "✍️", "⚠️")


def shape(text):
    lines = text.splitlines()
    headings = [len(m.group(1)) for l in lines if (m := re.match(r"^(#{1,6})\s", l))]
    tables = sum(1 for l in lines if l.lstrip().startswith("|"))
    callouts = []
    prev_quote = False
    for l in lines:
        is_quote = l.startswith(">")
        if is_quote and not prev_quote:
            body = l[1:].lstrip()
            callouts.append(next((e for e in CALLOUTS if body.startswith(e)), "?"))
        prev_quote = is_quote
    placeholders = Counter(re.findall(r"\{\{([a-zA-Z0-9_]+)\}\}", text))
    return {"headings": headings, "table rows": tables, "callouts": callouts, "placeholders": placeholders}


def main():
    errors = []
    for cat in sorted((ROOT / "templates").iterdir()):
        if not cat.is_dir():
            continue
        langs = [d for d in cat.iterdir() if d.is_dir()]
        base = cat / BASE
        for other in langs:
            if other.name == BASE:
                continue
            for src in sorted(base.iterdir()):
                twin = other / src.name
                rel = f"{cat.name}/{other.name}/{src.name}"
                if not twin.exists():
                    errors.append(f"{rel}: missing")
                    continue
                if src.suffix == ".md":
                    a, b = shape(src.read_text(encoding="utf-8")), shape(twin.read_text(encoding="utf-8"))
                    for key in a:
                        if a[key] != b[key]:
                            errors.append(f"{rel}: {key} differ\n    {BASE}: {a[key]}\n    {other.name}: {b[key]}")
                elif src.suffix in (".yaml", ".yml"):

                    def keys(d, p=""):
                        if isinstance(d, dict):
                            return set().union(*[keys(v, f"{p}.{k}") for k, v in d.items()], {p})
                        if isinstance(d, list):
                            return set().union(*[keys(v, f"{p}[{i}]") for i, v in enumerate(d)], {p})
                        return {p}

                    ka = keys(yaml.safe_load(src.read_text(encoding="utf-8")))
                    kb = keys(yaml.safe_load(twin.read_text(encoding="utf-8")))
                    if ka != kb:
                        errors.append(f"{rel}: keys differ: {sorted(ka ^ kb)[:10]}")
    if errors:
        print("Parity check FAILED:\n- " + "\n- ".join(errors))
        sys.exit(1)
    print("parity ok")


if __name__ == "__main__":
    main()
