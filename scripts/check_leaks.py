#!/usr/bin/env python3
"""Leak check: make sure the repo and built files stay free of private traces.

Fails on:
  - any URL whose domain is not on the public allowlist below
  - personal-looking email addresses other than GitHub noreply
  - author / company / last-modified-by metadata in .docx / .xlsx / .pptx, and /Author in .pdf
  - EXIF / text metadata in images

  python3 scripts/check_leaks.py [PATHS...]   (default: repo root + dist/)
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
# Tool caches are local and gitignored. A pytest run writes docs.pytest.org into .pytest_cache.
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".out", ".pytest_cache", ".ruff_cache", ".mypy_cache", "htmlcov"}
TEXT_EXT = {".svg", ".md", ".yaml", ".yml", ".json", ".py", ".sh", ".txt", ".html", ".csv", ".toml", ".cfg", ""}
OFFICE_EXT = {".docx", ".xlsx", ".pptx"}
ALLOWED_DOMAINS = {
    "github.com",
    "raw.githubusercontent.com",
    "docs.github.com",
    "users.noreply.github.com",
    "claude.ai",
    "claude.com",
    "docs.claude.com",
    "support.claude.com",
    "anthropic.com",
    "www.anthropic.com",
    "code.claude.com",
    "cursor.com",
    "www.cursor.com",
    "cursor.directory",
    "agentskills.io",
    "agent-plugins.org",
    "skills.sh",
    "support.google.com",
    "workspace.google.com",
    "support.microsoft.com",
    "learn.microsoft.com",
    "example.com",
    "example.org",
    "www.aihero.dev",
    "img.shields.io",
    "localhost",
    "adr.github.io",
    "jvns.ca",
    "www.ccl.org",
    "ccl.org",
    "www.oreilly.com",
    "oreilly.com",
    "lethain.com",
    "hbr.org",
    "openpyxl.readthedocs.io",
    "python-docx.readthedocs.io",
    "pyyaml.org",
    "opensource.org",
    "keepachangelog.com",
    "semver.org",
    "www.python.org",
    "python.org",
    "schemas.openxmlformats.org",
    "schemas.microsoft.com",
    "purl.org",
    "www.w3.org",
    "www.geeksforgeeks.org",
    "kotlinlang.org",
    "docs.oracle.com",
    "openjdk.org",
}
URL = re.compile(r"https?://([a-zA-Z0-9.\-]+)")
EMAIL = re.compile(r"[a-zA-Z0-9._%+\-]+@([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})")
EMAIL_OK = {"users.noreply.github.com", "example.com", "example.org"}


def iter_files(paths):
    for base in paths:
        base = Path(base)
        if base.is_file():
            yield base
            continue
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_file() and not (set(p.relative_to(base).parts) & SKIP_DIRS):
                yield p


def office_texts(path):
    """Yield (part, text) for every XML part of an Office file (content + metadata)."""
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if name.endswith((".xml", ".rels")):
                yield name, z.read(name).decode("utf-8", "ignore")


def check_text(where, text, problems, check_urls=True):
    if check_urls:
        for m in URL.finditer(text):
            dom = m.group(1).lower().rstrip(".")
            if dom not in ALLOWED_DOMAINS and not dom.endswith(".example.com"):
                problems.append(f"{where}: non-allowlisted URL domain: {dom}")
        for m in EMAIL.finditer(text):
            dom = m.group(1).lower()
            if dom not in EMAIL_OK:
                problems.append(f"{where}: email address with domain {dom}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args()
    paths = args.paths or [ROOT, ROOT / "dist"]
    problems = []
    checked = 0
    self_path = Path(__file__).resolve()
    for f in iter_files(paths):
        rel = f.relative_to(ROOT) if str(f).startswith(str(ROOT)) else f
        ext = f.suffix.lower()
        checked += 1
        if f.resolve() == self_path:
            continue  # don't flag our own allowlist
        if ext in OFFICE_EXT:
            for part, text in office_texts(f):
                xml_text = re.sub(r"<[^>]+>", " ", text)
                is_rels = part.endswith(".rels")
                check_text(
                    f"{rel}:{part}",
                    text if is_rels else xml_text,
                    problems,
                    check_urls=is_rels and "hyperlink" in text,
                )
                if part == "docProps/core.xml":
                    for tag in ("dc:creator", "cp:lastModifiedBy"):
                        m = re.search(rf"<{tag}>(.*?)</{tag}>", text)
                        if m and m.group(1) not in ("", "zeevolution-skills", "Zeevolution"):
                            problems.append(f"{rel}: metadata {tag} = '{m.group(1)}'")
                if part == "docProps/app.xml":
                    m = re.search(r"<Company>(.*?)</Company>", text)
                    if m and m.group(1).strip():
                        problems.append(f"{rel}: metadata Company = '{m.group(1)}'")
        elif ext == ".pdf":
            data = f.read_bytes().decode("latin-1", "ignore")
            m = re.search(r"/Author\s*\((.*?)\)", data)
            if m and m.group(1) not in ("", "zeevolution-skills", "Zeevolution"):
                problems.append(f"{rel}: PDF Author = '{m.group(1)}'")
        elif ext in {".png", ".jpg", ".jpeg"}:
            try:
                from PIL import Image

                img = Image.open(f)
                if img.getexif():
                    problems.append(f"{rel}: image has EXIF metadata (strip it)")
                if getattr(img, "text", None):
                    check_text(rel, " ".join(map(str, img.text.values())), problems)
            except ImportError:
                pass
        elif ext in TEXT_EXT or f.name in {"LICENSE", "CODEOWNERS"}:
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            check_text(rel, text, problems)
    if problems:
        print(f"Leak check FAILED ({len(problems)} problem(s) in {checked} files):")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print(f"leak check ok ({checked} files)")


if __name__ == "__main__":
    main()
