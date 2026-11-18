#!/usr/bin/env python3
"""Build release assets into dist/.

  dist/career-management-kit-<lang>.zip   Manual Kit: markdown/, word/, sheets/, START-HERE.pdf
  dist/skills/<skill>.skill                one zip per skill (upload to the Claude app)
  dist/zeevolution-skills-all-skills.zip   every .skill file together

Requires: python-docx, openpyxl, pyyaml. START-HERE.pdf needs LibreOffice (`soffice`); skipped with a warning otherwise.

  python3 scripts/build.py [--out DIR]
"""
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
TPL = ROOT / "templates" / "career-management"
SCRIPTS = ROOT / "skills" / "foundations" / "cloud-workspace" / "scripts"
LANGS = ["en", "pt-BR"]
FALLBACK = {"en": "text fallback", "pt-BR": "versão em texto"}
FILE_NAMES = {
    "en": {"00": "🚀 Career Hub", "01": "🎶 1:1 Notes", "02": "🌱 Growth Plan", "03": "😎 Brag Document",
           "04": "🧭 Focus Plan", "05": "🪜 Ladder Assessment", "06": "📝 Performance Review",
           "07": "🔎 Evidence Doc", "08": "🛬 Onboarding Plan"},
    "pt-BR": {"00": "🚀 Hub de Carreira", "01": "🎶 Notas de 1:1", "02": "🌱 PDI", "03": "😎 Brag Document",
              "04": "🧭 Plano de Foco", "05": "🪜 Avaliação de Trilha", "06": "📝 Avaliação de Desempenho",
              "07": "🔎 Documento de Evidências", "08": "🛬 Plano de Onboarding"},
}


def run(*args):
    subprocess.run([sys.executable, *map(str, args)], check=True, stdout=subprocess.DEVNULL)


def zip_dir(src_dir, zip_path, arc_root):
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src_dir.rglob("*")):
            if p.is_file() and "__pycache__" not in p.parts:
                z.write(p, Path(arc_root) / p.relative_to(src_dir))


def build_kit(lang):
    kit = DIST / f"career-management-kit-{lang}"
    (kit / "markdown").mkdir(parents=True)
    (kit / "word").mkdir()
    (kit / "sheets").mkdir()
    names = FILE_NAMES[lang]
    for md in sorted((TPL / lang).glob("0*.md")):
        num = md.name[:2]
        stem = f"{num} - {names[num]}"
        if num == "05":
            # the real Ladder Assessment is the spreadsheet; keep the text fallback in markdown/ only
            shutil.copyfile(md, kit / "markdown" / f"{stem} ({FALLBACK[lang]}).md")
            continue
        shutil.copyfile(md, kit / "markdown" / f"{stem}.md")
        run(SCRIPTS / "render_doc.py", "--in", md, "--out", kit / "word" / f"{stem}.docx", "--keep-missing")
    run(SCRIPTS / "build_sheet.py", "--spec", TPL / "05-ladder-assessment.sheet.yaml",
        "--strings", TPL / lang / "05-ladder-assessment.strings.yaml",
        "--ladder", TPL / lang / "generic-ladder.yaml",
        "--out", kit / "sheets" / f"05 - {names['05']}.xlsx")
    start = ROOT / "docs" / f"START-HERE.{lang}.md"
    if start.exists():
        with tempfile.TemporaryDirectory() as tmp:
            docx = Path(tmp) / "START-HERE.docx"
            run(SCRIPTS / "render_doc.py", "--in", start, "--out", docx, "--keep-missing")
            soffice = shutil.which("soffice") or shutil.which("libreoffice")
            if soffice:
                subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir", tmp, str(docx)],
                               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                shutil.copyfile(Path(tmp) / "START-HERE.pdf", kit / "START-HERE.pdf")
            else:
                print("WARNING: LibreOffice not found; START-HERE.docx shipped instead of PDF")
                shutil.copyfile(docx, kit / "START-HERE.docx")
    zip_dir(kit, DIST / f"career-management-kit-{lang}.zip", kit.name)
    return kit


def build_skills():
    out = DIST / "skills"
    out.mkdir(parents=True)
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    files = []
    for rel in plugin["skills"]:
        src = ROOT / rel
        target = out / f"{src.name}.skill"
        zip_dir(src, target, src.name)
        files.append(target)
    with zipfile.ZipFile(DIST / "zeevolution-skills-all-skills.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            z.write(f, f.name)
    return files


def main():
    global DIST
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", help="output folder (default: dist/)")
    args = ap.parse_args()
    if args.out:
        DIST = Path(args.out).resolve()
    run(ROOT / "scripts" / "sync_skill_assets.py", "--check")
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()
    for lang in LANGS:
        kit = build_kit(lang)
        print(f"kit: {kit}.zip")
    for f in build_skills():
        print(f"skill: {f.name}")
    print(f"built {DIST}")


if __name__ == "__main__":
    main()
