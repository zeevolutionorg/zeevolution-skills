#!/usr/bin/env python3
"""End-to-end dry run of /career-hub-toolkit with the Files and Manual adapters.

4 fictional personas x 2 modes (self, lead) x 2 languages x 2 formats (files, manual) = 32 hubs,
built with the bundled copy of make_bundle.py exactly as the skill tells the agent to.
Checks: expected files exist, no {{placeholder}} left, the person's name is in every document,
the hub links to every other document, the spreadsheet opens with the person in the header,
and the manual paste guide lists every document.

  python3 scripts/dry_run.py [--out DIR]   # default: <system temp>/zeevolution-skills-dry-run
"""

import argparse
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "career-management" / "career-hub-toolkit"
TPL = SKILL / "assets" / "templates"
OUT = Path(tempfile.gettempdir()) / "zeevolution-skills-dry-run"
sys.path.insert(0, str(SKILL / "scripts"))
import make_bundle  # noqa: E402  (the copy the skill ships)

PERSONAS = [  # fictional
    {
        "person_name": "Ana Souza",
        "role": "Data Scientist",
        "discipline": "Data Science",
        "level": "Contributing",
        "next_level": "Owning",
    },
    {
        "person_name": "Bruno Costa",
        "role": "Backend Engineer",
        "discipline": "Engineering",
        "level": "Owning",
        "next_level": "Leading",
    },
    {
        "person_name": "Carla Mendes",
        "role": "Product Designer",
        "discipline": "Design",
        "level": "Learning",
        "next_level": "Contributing",
    },
    {
        "person_name": "Diego Alves",
        "role": "Product Manager",
        "discipline": "Product Management",
        "level": "Leading",
        "next_level": "Shaping",
    },
]
GENERIC = {"en": "Generic ladder", "pt-BR": "Trilha genérica"}
EXPECTED_DOCS = {"self": 6, "lead": 9}  # lead includes the two optional docs in this run


def text_of(path):
    if path.suffix == ".docx":
        with zipfile.ZipFile(path) as z:
            return re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode("utf-8"))
    return path.read_text(encoding="utf-8")


def context(persona, mode, lang):
    return dict(
        persona,
        leader_name="Morgan Lee" if mode == "lead" else "Sam Rivera",
        start_date="2026-11-18",
        created_date="2026-11-18",
        next_meeting_date="2026-12-02",
        cycle="2027 H1" if lang == "en" else "2027 S1",
        ladder_source=GENERIC[lang],
        ladder_source_label=GENERIC[lang],
        lang=lang,
    )


def run_one(persona, mode, lang, fmt, out_root):
    folder = out_root / fmt / lang / mode / persona["person_name"].replace(" ", "_")
    include = ["evidence", "onboarding"] if mode == "lead" else []
    created = make_bundle.make(
        TPL / "bundle.yaml",
        TPL,
        lang,
        mode,
        fmt,
        context(persona, mode, lang),
        folder,
        include,
        SKILL / "assets" / f"generic-ladder.{lang}.yaml",
        SKILL / "assets" / f"paste-guide.{lang}.md",
    )
    problems = []
    docs = [p for p in created if p.name != "HOW-TO-PASTE.md"]
    if len(docs) != EXPECTED_DOCS[mode]:
        problems.append(f"expected {EXPECTED_DOCS[mode]} documents, got {len(docs)}")
    for p in created:
        if p.suffix == ".xlsx":
            ws = load_workbook(p).worksheets[1]
            if ws["C5"].value != persona["person_name"]:
                problems.append(f"{p.name}: person not in Assessment!C5")
            continue
        text = text_of(p)
        left = re.findall(r"\{\{[a-z_]+\}\}", text)
        if left:
            problems.append(f"{p.name}: leftover {left[:3]}")
        if p.name != "HOW-TO-PASTE.md" and persona["person_name"] not in text:
            problems.append(f"{p.name}: person name missing")
    hub = next(p for p in created if p.name.startswith("00 - "))
    hub_text = (
        hub.read_text(encoding="utf-8")
        if hub.suffix == ".md"
        else zipfile.ZipFile(hub).read("word/_rels/document.xml.rels").decode() + text_of(hub)
    )
    for p in docs:
        if p is not hub and p.name not in hub_text:
            problems.append(f"hub does not link {p.name}")
    if fmt == "manual":
        guide = folder / "HOW-TO-PASTE.md"
        if not guide.exists():
            problems.append("HOW-TO-PASTE.md missing")
        else:
            g = guide.read_text(encoding="utf-8")
            problems += [f"paste guide misses {p.name}" for p in docs if p.name not in g]
    return problems


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    args = ap.parse_args()
    out_root = Path(args.out) if args.out else OUT
    if out_root.exists():
        shutil.rmtree(out_root)
    failures = 0
    for fmt in ("files", "manual"):
        for lang in ("en", "pt-BR"):
            for mode in ("self", "lead"):
                for persona in PERSONAS:
                    problems = run_one(persona, mode, lang, fmt, out_root)
                    failures += bool(problems)
                    status = "ok" if not problems else "FAIL: " + "; ".join(problems)
                    print(f"[{fmt:6}] [{lang:5}] {mode:4} {persona['person_name']:13} {status}")
    if failures:
        sys.exit(1)
    print(f"dry run ok -> {out_root}")


if __name__ == "__main__":
    main()
