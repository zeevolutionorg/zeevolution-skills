"""Shared helpers for the test suite (imported as `helpers`).

The tests/ tree mirrors the repository: the test for `scripts/build.py` lives at
`tests/scripts/test_build.py`, the test for `skills/foundations/cloud-workspace/scripts/render_doc.py`
at `tests/skills/foundations/cloud-workspace/scripts/test_render_doc.py`, and so on.
tests/test_repo_layout.py enforces it.
"""

import importlib.util
import re
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LANGS = ["en", "pt-BR"]
CW_SCRIPTS = ROOT / "skills" / "foundations" / "cloud-workspace" / "scripts"
TPL = ROOT / "templates" / "career-management"

# shared scripts import each other by name (make_bundle -> render_doc, build_sheet)
for p in (CW_SCRIPTS, ROOT / "scripts"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


def load_script(relpath):
    """Import a script by its path in the repo, e.g. load_script('scripts/build.py')."""
    path = ROOT / relpath
    name = "zs_" + re.sub(r"\W", "_", relpath)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def frontmatter(skill_md: Path) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", skill_md.read_text(encoding="utf-8"), re.S)
    assert m, f"{skill_md} has no frontmatter"
    return yaml.safe_load(m.group(1))


def docx_text(path) -> str:
    with zipfile.ZipFile(path) as z:
        return re.sub(r"<[^>]+>", "", z.read("word/document.xml").decode("utf-8"))


SKILLS = ROOT / "skills"


def skill_dir(category, name):
    return SKILLS / category / name


def relative_links(md_path: Path):
    """Relative links in a Markdown file: [text](path) that aren't URLs or anchors."""
    text = md_path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)  # ignore code blocks
    text = re.sub(r"`[^`\n]*`", "", text)  # and inline code
    links = re.findall(r"\]\(([^)\s]+)\)", text)
    links = [l for l in links if not l.startswith(("http", "#", "mailto:", "{{", "<"))]
    return [l for l in links if "<" not in l and "NNN" not in l]  # template placeholders, not real links


def assert_skill_contract(path: Path, user_invoked: bool):
    """Rules every skill follows: frontmatter, invocation mode, links that resolve."""
    fm = frontmatter(path / "SKILL.md")
    assert fm["name"] == path.name
    assert len(fm["description"]) >= 40
    assert bool(fm.get("disable-model-invocation")) is user_invoked
    for md in path.glob("*.md"):
        for link in relative_links(md):
            target = (md.parent / link.split("#")[0]).resolve()
            assert target.exists(), f"{md.name}: broken link {link}"
    return fm
