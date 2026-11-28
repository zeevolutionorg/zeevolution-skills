"""Contract tests for skills/software-engineering/strong-programmer/ — the router, the knowledge map and every node."""

import re

import pytest
from helpers import assert_skill_contract, relative_links, skill_dir

pytestmark = pytest.mark.contract

SKILL = skill_dir("software-engineering", "strong-programmer")
TEXT = (SKILL / "SKILL.md").read_text(encoding="utf-8")
MAP = (SKILL / "map.md").read_text(encoding="utf-8")
ALL_FILES = sorted(SKILL.rglob("*.md"))
NODE_FILES = [p for p in ALL_FILES if p.parent != SKILL]
APPROACHES = ["Procedural", "Object-oriented", "Parallel", "Logic", "Functional", "Database"]
ITEM = re.compile(r"^\s*- ([✅🌱🔜]) (.+)$", re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")


def read(rel_path):
    return (SKILL / rel_path).read_text(encoding="utf-8")


def headings(text, level=2):
    return re.findall(rf"^{'#' * level} (.+)$", text, re.M)


def rel(path):
    return str(path.relative_to(SKILL))


def test_contract():
    assert_skill_contract(SKILL, user_invoked=False)


@pytest.mark.parametrize("md", ALL_FILES, ids=rel)
def test_relative_links_resolve(md):
    for link in relative_links(md):
        assert (md.parent / link.split("#")[0]).resolve().exists(), f"{rel(md)}: broken link {link}"


@pytest.mark.parametrize("node", NODE_FILES, ids=rel)
def test_map_links_every_node(node):
    linked = {(SKILL / link.split("#")[0]).resolve() for link in relative_links(SKILL / "map.md")}
    assert node.resolve() in linked, f"map.md does not link {rel(node)}"


def test_planned_nodes_have_no_link_and_the_others_do():
    items = ITEM.findall(MAP)
    assert items
    for status, text in items:
        assert bool(LINK.search(text)) is (status != "🔜"), f"{status} {text}"


def test_language_matrix_cells():
    assert f"| Language | {' | '.join(APPROACHES)} |" in MAP
    rows = [line for line in MAP.splitlines() if line.startswith("|") and "](languages/" in line]
    assert rows
    for row in rows:
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        assert len(cells) == 1 + len(APPROACHES), row
        assert all(c in {"✅", "🌱", "🔜", "—"} for c in cells[1:]), row


@pytest.mark.parametrize("mode", ["develop", "review-code", "review-pr"])
def test_modes(mode):
    assert f"`{mode}`" in TEXT


@pytest.mark.parametrize(
    "number, step",
    enumerate(
        ["Pick the mode", "Orient before judging", "Load the branch", "Tidy First", "Do the work", "Validate", "Report"],
        start=1,
    ),
)
def test_seven_steps(number, step):
    assert re.search(rf"^{number}\. \*\*{re.escape(step)}", TEXT, re.M)


@pytest.mark.parametrize(
    "shape, sections",
    [
        ("review", ["Verdict", "What I checked", "Context", "Findings", "Tidy First", "Not covered yet"]),
        ("develop", ["The change", "Design choices", "Tidyings", "Validation", "PR description", "Not covered yet"]),
    ],
    ids=["review", "develop"],
)
def test_report_sections_in_order(shape, sections):
    reviews, develop = TEXT.split("## Report", 1)[1].split("**Develop:**", 1)
    report = develop if shape == "develop" else reviews
    positions = [report.find(f"**{s}**") for s in sections]
    assert -1 not in positions and positions == sorted(positions), dict(zip(sections, positions))


@pytest.mark.parametrize("term", ["Approve", "Request changes", "Request a split", "`nit:`", "`suggestion:`", "2,000"])
def test_review_verdicts_and_labels(term):
    assert term in TEXT


@pytest.mark.parametrize(
    "path, expected",
    [
        ("practices/pull-requests.md", ["When you open one", "When you review one", "Applying it in each mode"]),
        (
            "practices/validating-work.md",
            ["Find the project's checks", "Run them locally", "Follow the pull request's CI", "Report what you ran"],
        ),
    ],
)
def test_practice_headings(path, expected):
    assert headings(read(path)) == expected


@pytest.mark.parametrize(
    "rule",
    [
        "Under 200",
        "200–800",
        "1,500",
        "3 or 4",
        "draft",
        "8 business hours",
        "2,000",
        "`nit:`",
        "`suggestion:`",
        "Request changes",
    ],
)
def test_pull_request_habits(rule):
    assert rule in read("practices/pull-requests.md")


@pytest.mark.parametrize("part", ["what changed", "why", "how you tested it", "where to start reading"])
def test_pr_description_parts(part):
    assert f"**{part}**" in read("practices/pull-requests.md")


def test_develop_report_lists_the_pr_description_parts():
    assert "what changed, why, how you tested it, where to start reading" in TEXT


@pytest.mark.parametrize("path", ["SKILL.md", "practices/pull-requests.md", "practices/validating-work.md"])
def test_opens_pull_requests_as_drafts(path):
    assert "as a draft" in read(path)


def test_follows_the_pull_requests_ci():
    assert "gh pr checks" in read("practices/validating-work.md")


@pytest.mark.parametrize("approach", APPROACHES)
def test_style_signals_cover_every_approach(approach):
    assert re.search(rf"^\|.*\| {approach} \|$", read("paradigms/README.md"), re.M)


@pytest.mark.parametrize("lang", ["kotlin", "java"])
def test_language_readme_headings(lang):
    assert headings(read(f"languages/{lang}/README.md")) == ["Approaches supported", "Detecting the version", "Sources"]


def test_router_word_budget():
    assert len(TEXT.split()) <= 800


@pytest.mark.parametrize("md", ALL_FILES, ids=rel)
def test_file_line_budget(md):
    assert len(md.read_text(encoding="utf-8").splitlines()) <= 250
