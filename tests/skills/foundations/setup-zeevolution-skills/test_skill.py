"""Contract tests for skills/foundations/setup-zeevolution-skills/"""

import re

import pytest
from helpers import assert_skill_contract, skill_dir

pytestmark = pytest.mark.contract
SKILL = skill_dir("foundations", "setup-zeevolution-skills")
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")


def test_contract():
    assert_skill_contract(SKILL, user_invoked=True)


def test_asks_exactly_s1_to_s6():
    assert re.findall(r"^\| (S\d) \|", TEXT, re.M) == [f"S{i}" for i in range(1, 7)]


def test_platform_options_include_every_adapter():
    s3 = next(ln for ln in TEXT.splitlines() if ln.startswith("| S3 |"))
    for option in ("Google Workspace", "Microsoft 365", "Files", "Markdown"):
        assert option in s3


def test_saved_platform_values():
    assert '"platform": "google | microsoft | files | manual"' in TEXT
