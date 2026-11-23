#!/usr/bin/env python3
"""Copy the source-of-truth templates and shared scripts into the skills that bundle them.

Skills must work on their own (a user may install a single skill, or upload one .skill file
to the Claude app), so career-hub-toolkit and career-ladder carry their own copies.
The source of truth stays in templates/ and skills/foundations/cloud-workspace/scripts/.

  python3 scripts/sync_skill_assets.py          # write copies
  python3 scripts/sync_skill_assets.py --check  # fail if copies are out of date (CI)
"""

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TPL = ROOT / "templates" / "career-management"
LANGS = ["en", "pt-BR"]
SHARED_SCRIPTS = ROOT / "skills" / "foundations" / "cloud-workspace" / "scripts"
SHARED_ASSETS = ROOT / "skills" / "foundations" / "cloud-workspace" / "assets"
TOOLKIT = ROOT / "skills" / "career-management" / "career-hub-toolkit"
LADDER_SKILL = ROOT / "skills" / "career-management" / "career-ladder"

HEADER = {
    "en": (
        "## Generic career ladder",
        "Shape sample only. Pillar names differ by company and are filled in after the documents are generated. "
        "Generated from `assets/generic-ladder.en.yaml` — edit the YAML in `templates/`, not this file.",
        "Pillars",
        "Levels",
        "Level",
    ),
    "pt-BR": (
        "## Trilha de carreira genérica",
        "Só um exemplo de formato. Os nomes dos pilares mudam de empresa para empresa e são preenchidos depois que os documentos forem gerados. "
        "Gerada a partir de `assets/generic-ladder.pt-BR.yaml` — edite o YAML em `templates/`, não este arquivo.",
        "Pilares",
        "Níveis",
        "Nível",
    ),
}


def planned():
    """Yield (source, destination) pairs."""
    for lang in LANGS:
        for src in sorted((TPL / lang).glob("*.md")):
            yield src, TOOLKIT / "assets" / "templates" / lang / src.name
        yield (
            TPL / lang / "05-ladder-assessment.strings.yaml",
            TOOLKIT / "assets" / "templates" / lang / "05-ladder-assessment.strings.yaml",
        )
        for dest in (TOOLKIT, LADDER_SKILL):
            yield TPL / lang / "generic-ladder.yaml", dest / "assets" / f"generic-ladder.{lang}.yaml"
    yield TPL / "05-ladder-assessment.sheet.yaml", TOOLKIT / "assets" / "templates" / "05-ladder-assessment.sheet.yaml"
    yield TPL / "bundle.yaml", TOOLKIT / "assets" / "templates" / "bundle.yaml"
    for name in ("render_doc.py", "build_sheet.py", "make_bundle.py"):
        yield SHARED_SCRIPTS / name, TOOLKIT / "scripts" / name
    for lang in LANGS:
        yield SHARED_ASSETS / f"paste-guide.{lang}.md", TOOLKIT / "assets" / f"paste-guide.{lang}.md"


def generic_ladder_md():
    parts = ["# Generic career ladder · Trilha de carreira genérica\n"]
    for lang in LANGS:
        title, intro, h_p, h_l, h_level = HEADER[lang]
        lad = yaml.safe_load((TPL / lang / "generic-ladder.yaml").read_text(encoding="utf-8"))
        parts.append(f"{title} ({lang})\n\n{intro}\n\n### {h_p}\n")
        parts += [f"- **{p['name']}** — {p['meaning']}" for p in lad["pillars"]]
        parts.append(f"\n### {h_l}\n")
        head = "| " + h_level + " | " + " | ".join(p["name"] for p in lad["pillars"]) + " |"
        parts.append(head)
        parts.append("|" + "---|" * (len(lad["pillars"]) + 1))
        for lvl in lad["levels"]:
            parts.append(f"| **{lvl['name']}** | " + " | ".join(lvl["expectations"]) + " |")
        parts.append("")
    return "\n".join(parts).rstrip("\n") + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    stale = []
    for src, dst in planned():
        if args.check:
            if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                stale.append(str(dst.relative_to(ROOT)))
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
    md = generic_ladder_md()
    md_path = LADDER_SKILL / "GENERIC-LADDER.md"
    if args.check:
        if not md_path.exists() or md_path.read_text(encoding="utf-8") != md:
            stale.append(str(md_path.relative_to(ROOT)))
        if stale:
            print("Out of date (run: python3 scripts/sync_skill_assets.py):\n  " + "\n  ".join(stale))
            sys.exit(1)
        print("skill assets in sync")
    else:
        md_path.write_text(md, encoding="utf-8")
        print("synced skill assets")


if __name__ == "__main__":
    main()
