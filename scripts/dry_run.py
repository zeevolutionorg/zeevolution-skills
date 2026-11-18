#!/usr/bin/env python3
"""Dry run of /career-hub-toolkit with the Files adapter, for 4 fictional personas x 2 modes x 2 languages.

Does what the skill tells the agent to do (render every document, build the sheet, fill the hub last),
then checks the results: every file exists, no {{placeholder}} is left, the sheet opens and its
Assessment tab shows the person's name.

  python3 scripts/dry_run.py [--out DIR]   # default: <system temp>/zeevolution-skills-dry-run
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "career-management" / "career-hub-toolkit"
TPL = SKILL / "assets" / "templates"
OUT = Path(tempfile.gettempdir()) / "zeevolution-skills-dry-run"
sys.path.insert(0, str(ROOT / "scripts"))
from build import FILE_NAMES  # noqa: E402

PERSONAS = [  # fictional
    {"person_name": "Ana Souza", "role": "Data Scientist", "discipline": "Data Science", "level": "Contributing", "next_level": "Owning"},
    {"person_name": "Bruno Costa", "role": "Backend Engineer", "discipline": "Engineering", "level": "Owning", "next_level": "Leading"},
    {"person_name": "Carla Mendes", "role": "Product Designer", "discipline": "Design", "level": "Learning", "next_level": "Contributing"},
    {"person_name": "Diego Alves", "role": "Product Manager", "discipline": "Product Management", "level": "Leading", "next_level": "Shaping"},
]
DOCS = {"self": ["01", "02", "03", "04"], "lead": ["01", "02", "03", "04", "06", "07", "08"]}
LINK_KEYS = {"00": "hub", "01": "one_on_one", "02": "growth_plan", "03": "brag", "04": "focus_plan",
             "05": "ladder", "06": "review", "07": "evidence", "08": "onboarding"}
GENERIC = {"en": "Generic ladder", "pt-BR": "Trilha genérica"}


def docx_text(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    return re.sub(r"<[^>]+>", "", xml)


def render(src, out, ctx_path):
    subprocess.run([sys.executable, str(SKILL / "scripts" / "render_doc.py"), "--in", str(src), "--out", str(out),
                    "--context", str(ctx_path)], check=True, stdout=subprocess.DEVNULL)


def one(persona, mode, lang):
    names = FILE_NAMES[lang]
    folder = OUT / lang / mode / persona["person_name"].replace(" ", "_")
    folder.mkdir(parents=True)
    ctx = dict(persona, leader_name="Morgan Lee" if mode == "lead" else "Sam Rivera",
               start_date="2026-11-18", created_date="2026-11-18", next_meeting_date="2026-12-02",
               cycle="2027 H1" if lang == "en" else "2027 S1", ladder_source=GENERIC[lang],
               ladder_source_label=GENERIC[lang], lang=lang)
    if mode == "self":
        ctx["leader_name"] = "Sam Rivera"  # the user's own manager
    for num, key in LINK_KEYS.items():
        wanted = num in ("00", "05") or num in DOCS[mode]
        ext = "xlsx" if num == "05" else "docx"
        ctx[f"doc_link_{key}"] = f"{num} - {names[num]}.{ext}" if wanted else ""
    tmp = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(ctx, tmp, ensure_ascii=False)
    tmp.close()
    ctx_path = Path(tmp.name)  # outside the output folder: personal data isn't left next to the documents
    problems = []
    for num in DOCS[mode]:
        src = next(TPL.joinpath(lang).glob(f"{num}-*.md"))
        out = folder / f"{num} - {names[num]}.docx"
        render(src, out, ctx_path)
    subprocess.run([sys.executable, str(SKILL / "scripts" / "build_sheet.py"),
                    "--spec", str(TPL / "05-ladder-assessment.sheet.yaml"),
                    "--strings", str(TPL / lang / "05-ladder-assessment.strings.yaml"),
                    "--ladder", str(SKILL / "assets" / f"generic-ladder.{lang}.yaml"),
                    "--context", str(ctx_path), "--out", str(folder / f"05 - {names['05']}.xlsx")],
                   check=True, stdout=subprocess.DEVNULL)
    render(next(TPL.joinpath(lang).glob("00-*.md")), folder / f"00 - {names['00']}.docx", ctx_path)  # hub last
    ctx_path.unlink()  # personal data: don't keep the context
    for f in folder.glob("*.docx"):
        text = docx_text(f)
        if "{{" in text:
            problems.append(f"{f.name}: leftover placeholder {re.findall(r'{{[a-z_]+}}', text)[:3]}")
        if persona["person_name"] not in text:
            problems.append(f"{f.name}: person name missing")
    wb = load_workbook(folder / f"05 - {names['05']}.xlsx")
    ws = wb.worksheets[1]
    if ws["C5"].value != persona["person_name"]:
        problems.append("xlsx: person name not in Assessment!C5")
    expected = 1 + len(DOCS[mode]) + 1
    count = len(list(folder.iterdir()))
    if count != expected:
        problems.append(f"expected {expected} files, found {count}")
    return folder, problems


def main():
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    args = ap.parse_args()
    if args.out:
        OUT = Path(args.out)
    if OUT.exists():
        shutil.rmtree(OUT)
    failures = 0
    for lang in ("en", "pt-BR"):
        for mode in ("self", "lead"):
            for persona in PERSONAS:
                folder, problems = one(persona, mode, lang)
                status = "ok" if not problems else "FAIL: " + "; ".join(problems)
                failures += bool(problems)
                print(f"[{lang:5}] {mode:4} {persona['person_name']:13} {persona['discipline']:18} {status}")
    if failures:
        sys.exit(1)
    print(f"dry run ok -> {OUT}")


if __name__ == "__main__":
    main()
