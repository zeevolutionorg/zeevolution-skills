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
OO = "paradigms/imperative/object-oriented"
APPROACH_FILES = {
    "Procedural": "paradigms/imperative/procedural.md",
    "Object-oriented": f"{OO}/README.md",
    "Parallel": "paradigms/imperative/parallel.md",
    "Logic": "paradigms/declarative/logic.md",
    "Functional": "paradigms/declarative/functional.md",
    "Database": "paradigms/declarative/database.md",
}
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
    link = f"[{approach}]({APPROACH_FILES[approach].split('/', 1)[1]})"
    assert re.search(rf"^\|.*\| {re.escape(link)} \|$", read("paradigms/README.md"), re.M)


@pytest.mark.parametrize("lang", ["kotlin", "java"])
def test_language_readme_headings(lang):
    assert headings(read(f"languages/{lang}/README.md")) == ["Approaches supported", "Detecting the version", "Sources"]


def test_router_word_budget():
    assert len(TEXT.split()) <= 800


@pytest.mark.parametrize("md", ALL_FILES, ids=rel)
def test_file_line_budget(md):
    assert len(md.read_text(encoding="utf-8").splitlines()) <= 250


APPROACH_HEADINGS = [
    "Core idea",
    "Primitives",
    "Strengths and costs",
    "Signals the code is in this style",
    "Common failure modes",
    "Review questions",
    "Languages",
    "Branches",
]


def section(text, heading):
    """The body of `## heading`, up to the next level-2 heading."""
    return text.split(f"\n## {heading}\n", 1)[1].split("\n## ", 1)[0]


def table_rows(text):
    return [line for line in text.splitlines() if line.startswith("|") and not line.startswith("|---")]


@pytest.mark.parametrize("approach, path", APPROACH_FILES.items())
def test_approach_file(approach, path):
    text = read(path)
    assert text.startswith(f"# {approach}\n")
    assert headings(text) == APPROACH_HEADINGS
    rows = table_rows(section(text, "Primitives"))
    assert rows[0].startswith("| Primitive |") and len(rows) >= 5


@pytest.mark.parametrize("approach, path", APPROACH_FILES.items())
def test_approach_file_languages_questions_and_length(approach, path):
    text = read(path)
    assert 60 <= len(text.splitlines()) <= 110
    languages = section(text, "Languages")
    rows = table_rows(languages)
    assert rows[0] == "| Language | Support |"
    assert {"Kotlin", "Java"} <= {row.split("|")[1].strip() for row in rows}
    registry = (SKILL / "languages/README.md").resolve()
    assert any(((SKILL / path).parent / link).resolve() == registry for link in LINK.findall(languages))
    questions = re.findall(r"^\d+\. ", section(text, "Review questions"), re.M)
    assert 5 <= len(questions) <= 8


@pytest.mark.parametrize("approach, path", APPROACH_FILES.items())
def test_map_and_paradigm_readmes_link_the_approach(approach, path):
    assert re.search(rf"^\s*- [✅🌱] \[{approach}\]\({re.escape(path)}\)", MAP, re.M)
    parent = "paradigms/imperative/README.md" if "imperative" in path else "paradigms/declarative/README.md"
    assert path.split("/", 2)[2] in read(parent)


def test_object_oriented_is_detailed_on_the_map():
    assert re.search(rf"^\s*- ✅ \[Object-oriented\]\({OO}/README.md\)", MAP, re.M)


OO_FILES = {
    f"{OO}/principles.md": ["GoF principles", "The eight causes of redesign", "SOLID", "Review questions", "Sources"],
    f"{OO}/code-smells.md": ["How to use this list", "Smells", "Object-oriented anti-patterns", "Sources"],
    f"{OO}/pattern-misuse.md": [
        "The main check: is it the right problem?",
        "Overkill",
        "Absorbed by the language",
        "Named like a pattern but isn't",
        "Wrong for the version",
        "How to check a pattern fits",
        "Sources",
    ],
    f"{OO}/domain-driven-design.md": ["Building blocks", "In Kotlin and Java", "Review questions", "Sources"],
}


@pytest.mark.parametrize("path, expected", OO_FILES.items())
def test_oo_foundation_headings(path, expected):
    assert headings(read(path)) == expected


@pytest.mark.parametrize(
    "maxim",
    [
        "Program to an interface, not an implementation",
        "Favor object composition over class inheritance",
        "Delegation",
        "Encapsulate the concept that varies",
    ],
)
def test_gof_principles(maxim):
    assert maxim in section(read(f"{OO}/principles.md"), "GoF principles")


@pytest.mark.parametrize("page", ["p. 18", "p. 20", "p. 24", "p. 28"])
def test_principles_cite_gof_pages(page):
    assert page in read(f"{OO}/principles.md")


def test_eight_causes_of_redesign():
    rows = table_rows(section(read(f"{OO}/principles.md"), "The eight causes of redesign"))
    assert rows[0] == "| Cause | What it looks like in code | Patterns that address it |"
    assert len(rows) == 1 + 8


@pytest.mark.parametrize(
    "principle", ["Single responsibility", "Open/closed", "Liskov substitution", "Interface segregation", "Dependency inversion"]
)
def test_solid(principle):
    assert f"| {principle} |" in section(read(f"{OO}/principles.md"), "SOLID")


SMELLS = [
    "Mysterious Name",
    "Duplicated Code",
    "Long Function",
    "Long Parameter List",
    "Global Data",
    "Mutable Data",
    "Divergent Change",
    "Shotgun Surgery",
    "Feature Envy",
    "Data Clumps",
    "Primitive Obsession",
    "Repeated Switches",
    "Loops",
    "Lazy Element",
    "Speculative Generality",
    "Temporary Field",
    "Message Chains",
    "Middle Man",
    "Insider Trading",
    "Large Class",
    "Alternative Classes with Different Interfaces",
    "Data Class",
    "Refused Bequest",
    "Comments",
]


@pytest.mark.parametrize("smell", SMELLS)
def test_every_smell(smell):
    assert f"| {smell} |" in section(read(f"{OO}/code-smells.md"), "Smells")


@pytest.mark.parametrize(
    "anti_pattern", ["God class", "Anemic domain model", "Inheritance for reuse", "Singleton as global state", "Service locator"]
)
def test_anti_patterns(anti_pattern):
    assert f"| {anti_pattern} |" in section(read(f"{OO}/code-smells.md"), "Object-oriented anti-patterns")


def test_absorbed_by_the_language_table():
    rows = table_rows(section(read(f"{OO}/pattern-misuse.md"), "Absorbed by the language"))
    assert rows[0] == "| Pattern | Kotlin | Java |"
    assert len(rows) >= 1 + 10


def test_fit_check_is_numbered():
    steps = re.findall(r"^\d\. ", section(read(f"{OO}/pattern-misuse.md"), "How to check a pattern fits"), re.M)
    assert len(steps) >= 5


@pytest.mark.parametrize("block", ["Entity", "Value object", "Aggregate", "Repository"])
def test_ddd_building_blocks(block):
    assert f"| {block} |" in section(read(f"{OO}/domain-driven-design.md"), "Building blocks")


GOF = {
    "Abstract Factory": 87,
    "Builder": 97,
    "Factory Method": 107,
    "Prototype": 117,
    "Singleton": 127,
    "Adapter": 139,
    "Bridge": 151,
    "Composite": 163,
    "Decorator": 175,
    "Facade": 185,
    "Flyweight": 195,
    "Proxy": 207,
    "Chain of Responsibility": 223,
    "Command": 233,
    "Interpreter": 243,
    "Iterator": 257,
    "Mediator": 273,
    "Memento": 283,
    "Observer": 293,
    "State": 305,
    "Strategy": 315,
    "Template Method": 325,
    "Visitor": 331,
}


def slug(name):
    return name.lower().replace(" ", "-")


def version_table(path):
    rows = [[c.strip() for c in row.strip("|").split("|")] for row in table_rows(read(path))]
    assert rows[0] == ["Feature", "Since", "Replaces or enables", "Review note"]
    return rows[1:]


def since_column(path):
    return [row[1] for row in version_table(path)]


def intro(path):
    """The text before the versions table."""
    return read(path).split("\n| Feature |", 1)[0]


def version_tuple(text):
    return tuple(int(part) for part in text.split("."))


def test_java_versions_are_8_to_25():
    since = since_column("languages/java/versions.md")
    assert len(since) >= 30
    for cell in since:
        m = re.fullmatch(r"Java (\d+)", cell)
        assert m and 8 <= int(m.group(1)) <= 25, cell


def test_java_versions_are_in_order():
    numbers = [int(cell.split()[1]) for cell in since_column("languages/java/versions.md")]
    assert numbers == sorted(numbers)


@pytest.mark.parametrize("feature", ["StructuredTaskScope", "StableValue", "stable value", "string template"])
def test_java_table_leaves_out_features_that_are_not_standard(feature):
    features = [row[0].lower() for row in version_table("languages/java/versions.md")]
    assert not any(feature.lower() in cell for cell in features), feature


def test_kotlin_versions_are_tagged():
    since = since_column("languages/kotlin/versions.md")
    assert len(since) >= 25
    for cell in since:
        assert re.fullmatch(r"Kotlin \d+\.\d+(\.\d+)?|kotlinx\.coroutines \d+\.\d+", cell), cell


def test_kotlin_versions_are_in_order_up_to_the_intro():
    path = "languages/kotlin/versions.md"
    latest = re.search(r"up to Kotlin (\d+\.\d+\.\d+)", intro(path))
    assert latest, "the intro names the last Kotlin release it covers"
    versions = [version_tuple(cell.split()[1]) for cell in since_column(path) if cell.startswith("Kotlin ")]
    assert versions == sorted(versions)
    assert max(versions) <= version_tuple(latest.group(1))


@pytest.mark.parametrize("lang", ["kotlin", "java"])
def test_versions_intro_says_an_upgrade_is_not_a_fix(lang):
    assert "team's decision, never a review fix" in intro(f"languages/{lang}/versions.md")


@pytest.mark.parametrize(
    "lang, expected",
    [
        ("kotlin", ["Idioms that matter in review", "Pitfalls", "Patterns the language absorbs", "Java interop"]),
        ("java", ["Idioms that matter in review", "Pitfalls", "Patterns the language absorbs"]),
    ],
)
def test_language_oo_headings(lang, expected):
    assert headings(read(f"languages/{lang}/object-oriented.md")) == expected


@pytest.mark.parametrize("lang", ["kotlin", "java"])
@pytest.mark.parametrize("pattern", GOF)
def test_language_covers_every_pattern(lang, pattern):
    absorbed = section(read(f"languages/{lang}/object-oriented.md"), "Patterns the language absorbs")
    assert re.search(rf"^\| \[?{re.escape(pattern)}\b", absorbed, re.M), pattern


def test_kotlin_idioms_cite_the_book():
    idioms = section(read("languages/kotlin/object-oriented.md"), "Idioms that matter in review")
    assert len(re.findall(r"KiA §\d+(\.\d+)*", idioms)) >= 15


def test_java_idioms_tag_versions():
    assert len(re.findall(r"Java \d+", section(read("languages/java/object-oriented.md"), "Idioms that matter in review"))) >= 8


@pytest.mark.parametrize("lang", ["kotlin", "java"])
def test_language_readme_links_its_files(lang):
    text = read(f"languages/{lang}/README.md")
    assert "(versions.md)" in text and "(object-oriented.md)" in text


@pytest.mark.parametrize("lang", ["Kotlin", "Java"])
def test_matrix_marks_object_oriented_detailed(lang):
    row = next((line for line in MAP.splitlines() if line.startswith((f"| 🌱 [{lang}]", f"| ✅ [{lang}]"))), None)
    assert row, f"map.md has no {lang} row in the matrix"
    assert [c.strip() for c in row.strip("|").split("|")][2] == "✅"
