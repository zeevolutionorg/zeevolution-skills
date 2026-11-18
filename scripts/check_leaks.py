#!/usr/bin/env python3
"""Leak check: make sure nothing in the repo (or in built files) points to an employer.

The denylist is NEVER stored in this repository (committing it would itself be a trace).
It is read from, in order:
  1. --denylist FILE
  2. $LEAK_DENYLIST_FILE
  3. $LEAK_DENYLIST   (newline-separated terms; this is how CI passes the GitHub Actions secret)
  4. ~/.config/zeevolution/denylist.txt
One term per line, case-insensitive; lines starting with # are comments.

Also fails on:
  - any URL whose domain is not on the public allowlist below
  - personal-looking email addresses other than GitHub noreply
  - author / company / last-modified-by metadata in .docx / .xlsx / .pptx, and /Author in .pdf
  - EXIF / text metadata in images

  python3 scripts/check_leaks.py [--denylist FILE] [PATHS...]   (default: repo root + dist/)
"""
import argparse
import os
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".out"}
TEXT_EXT = {".md", ".yaml", ".yml", ".json", ".py", ".sh", ".txt", ".html", ".csv", ".toml", ".cfg", ""}
OFFICE_EXT = {".docx", ".xlsx", ".pptx"}
ALLOWED_DOMAINS = {
    "github.com", "raw.githubusercontent.com", "docs.github.com", "users.noreply.github.com",
    "claude.ai", "claude.com", "docs.claude.com", "support.claude.com", "anthropic.com", "www.anthropic.com",
    "code.claude.com", "cursor.com", "www.cursor.com", "cursor.directory", "agentskills.io", "agent-plugins.org",
    "skills.sh", "support.google.com", "workspace.google.com", "support.microsoft.com", "learn.microsoft.com",
    "example.com", "example.org", "www.aihero.dev",
    "jvns.ca", "www.ccl.org", "ccl.org", "www.oreilly.com", "oreilly.com", "lethain.com", "hbr.org",
    "openpyxl.readthedocs.io", "python-docx.readthedocs.io", "pyyaml.org", "opensource.org", "keepachangelog.com",
    "semver.org", "www.python.org", "python.org",
    "schemas.openxmlformats.org", "schemas.microsoft.com", "purl.org", "www.w3.org",
}
URL = re.compile(r"https?://([a-zA-Z0-9.\-]+)")
EMAIL = re.compile(r"[a-zA-Z0-9._%+\-]+@([a-zA-Z0-9.\-]+\.[a-zA-Z]{2,})")
EMAIL_OK = {"users.noreply.github.com", "example.com", "example.org"}


def load_denylist(arg):
    text = None
    if arg:
        text = Path(arg).read_text(encoding="utf-8")
    elif os.environ.get("LEAK_DENYLIST_FILE"):
        text = Path(os.environ["LEAK_DENYLIST_FILE"]).read_text(encoding="utf-8")
    elif os.environ.get("LEAK_DENYLIST"):
        text = os.environ["LEAK_DENYLIST"]
    else:
        p = Path.home() / ".config" / "zeevolution" / "denylist.txt"
        if p.exists():
            text = p.read_text(encoding="utf-8")
    if text is None:
        return None
    return [t.strip().lower() for t in text.splitlines() if t.strip() and not t.strip().startswith("#")]


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


def check_text(where, text, deny, problems, check_urls=True):
    low = text.lower()
    for term in deny or []:
        # whole-word match, so "performa" doesn't hit "performance"
        if re.search(r"(?<![\w])" + re.escape(term) + r"(?![\w])", low):
            problems.append(f"{where}: denylisted term found ({term[:2]}…)")
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
    ap.add_argument("--denylist")
    ap.add_argument("paths", nargs="*")
    args = ap.parse_args()
    deny = load_denylist(args.denylist)
    if deny is None:
        print("WARNING: no denylist found (see script header). Only URL/email/metadata checks will run.")
    paths = args.paths or [ROOT, ROOT / "dist"]
    problems = []
    checked = 0
    self_path = Path(__file__).resolve()
    for f in iter_files(paths):
        rel = f.relative_to(ROOT) if str(f).startswith(str(ROOT)) else f
        ext = f.suffix.lower()
        checked += 1
        if f.resolve() == self_path:
            check_text(rel, "", deny, problems)  # don't flag our own allowlist
            continue
        if ext in OFFICE_EXT:
            for part, text in office_texts(f):
                xml_text = re.sub(r"<[^>]+>", " ", text)
                is_rels = part.endswith(".rels")
                check_text(f"{rel}:{part}", text if is_rels else xml_text, deny, problems,
                           check_urls=is_rels and "hyperlink" in text)
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
            check_text(rel, data, deny, problems, check_urls=False)
        elif ext in {".png", ".jpg", ".jpeg"}:
            try:
                from PIL import Image
                img = Image.open(f)
                if img.getexif():
                    problems.append(f"{rel}: image has EXIF metadata (strip it)")
                if getattr(img, "text", None):
                    check_text(rel, " ".join(map(str, img.text.values())), deny, problems)
            except ImportError:
                pass
        elif ext in TEXT_EXT or f.name in {"LICENSE", "CODEOWNERS"}:
            try:
                text = f.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            check_text(rel, text, deny, problems)
    if problems:
        print(f"Leak check FAILED ({len(problems)} problem(s) in {checked} files):")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print(f"leak check ok ({checked} files{'' if deny else ', no denylist'})")


if __name__ == "__main__":
    main()
