"""Contract tests for .claude-plugin/ and .cursor-plugin/ manifests."""

import json

import pytest
from helpers import ROOT

pytestmark = pytest.mark.contract


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


@pytest.mark.parametrize("folder", [".claude-plugin", ".cursor-plugin"])
def test_plugin_fields(folder):
    p = load(f"{folder}/plugin.json")
    assert p["name"] == "zeevolution-skills"
    assert p["license"] == "MIT"
    assert p["repository"] == "https://github.com/zeevolution/zeevolution-skills"
    assert p["author"]["name"] == "Zeevolution"


@pytest.mark.parametrize("folder", [".claude-plugin", ".cursor-plugin"])
def test_marketplace_lists_the_plugin_from_repo_root(folder):
    m = load(f"{folder}/marketplace.json")
    assert m["name"] == "zeevolution"
    assert [(p["name"], p["source"]) for p in m["plugins"]] == [("zeevolution-skills", "./")]


def test_claude_skill_paths_exist():
    for rel in load(".claude-plugin/plugin.json")["skills"]:
        assert (ROOT / rel / "SKILL.md").exists(), rel


def test_cursor_points_at_skills_tree():
    assert load(".cursor-plugin/plugin.json")["skills"] == "./skills/"
