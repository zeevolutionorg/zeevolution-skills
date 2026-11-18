"""The test tree mirrors the source tree — like src/main vs src/test in a Java service.

  scripts/<name>.py                                   -> tests/scripts/test_<name>.py
  skills/<category>/<skill>/scripts/<name>.py         -> tests/skills/<category>/<skill>/scripts/test_<name>.py
  skills/<category>/<skill>/SKILL.md                  -> tests/skills/<category>/<skill>/test_skill.py
  templates/<category>/                               -> tests/templates/<category>/test_*.py
  .claude-plugin/ + .cursor-plugin/                   -> tests/plugin-manifests/test_manifests.py

Generated copies (listed in scripts/sync_skill_assets.py) are covered by their source's tests
plus the sync check, so they don't need their own.
"""

import pytest
from helpers import ROOT, load_script

pytestmark = pytest.mark.contract

sync = load_script("scripts/sync_skill_assets.py")
GENERATED = {dst.resolve() for _, dst in sync.planned()}


def sources():
    yield from (ROOT / "scripts").glob("*.py")
    for p in (ROOT / "skills").rglob("scripts/*.py"):
        if p.resolve() not in GENERATED:
            yield p


@pytest.mark.parametrize("src", sorted(sources()), ids=lambda p: str(p.relative_to(ROOT)))
def test_every_script_has_a_mirrored_test(src):
    rel = src.relative_to(ROOT)
    expected = ROOT / "tests" / rel.parent / f"test_{src.name}"
    assert expected.exists(), f"missing {expected.relative_to(ROOT)}"


@pytest.mark.parametrize(
    "skill", sorted(p.parent for p in (ROOT / "skills").rglob("SKILL.md")), ids=lambda p: str(p.relative_to(ROOT))
)
def test_every_skill_has_a_contract_test(skill):
    expected = ROOT / "tests" / skill.relative_to(ROOT) / "test_skill.py"
    assert expected.exists(), f"missing {expected.relative_to(ROOT)}"


@pytest.mark.parametrize("category", sorted(p for p in (ROOT / "templates").iterdir() if p.is_dir()), ids=lambda p: p.name)
def test_every_template_category_has_tests(category):
    assert list((ROOT / "tests" / "templates" / category.name).glob("test_*.py"))


def test_no_orphan_tests():
    """A test file whose source was deleted or renamed should go too."""
    for t in (ROOT / "tests" / "scripts").glob("test_*.py"):
        assert (ROOT / "scripts" / t.name.removeprefix("test_")).exists(), t
    for t in (ROOT / "tests" / "skills").rglob("scripts/test_*.py"):
        src = ROOT / t.relative_to(ROOT / "tests").parent / t.name.removeprefix("test_")
        assert src.exists(), t
