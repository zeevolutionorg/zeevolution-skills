# 🧪 Testing and CI/CD

Every change to a skill, template or script is checked automatically on the pull request. Locally, `make check` runs the same stages in the same order.

## 📑 Contents

- [🪞 Where tests live: a mirror of the repo](#-where-tests-live-a-mirror-of-the-repo)
- [🎚️ Test levels (pytest markers)](#️-test-levels-pytest-markers)
- [🚦 The CI/CD sequence](#-the-cicd-sequence)
  - [🔀 On every pull request (.github/workflows/ci.yml)](#-on-every-pull-request-githubworkflowsciyml)
  - [🌙 Nightly (.github/workflows/nightly.yml)](#-nightly-githubworkflowsnightlyyml)
  - [🏷️ On a release tag v* (.github/workflows/release.yml)](#️-on-a-release-tag-v-githubworkflowsreleaseyml)
  - [🪝 Before every commit (.pre-commit-config.yaml)](#-before-every-commit-pre-commit-configyaml)
  - [📅 Weekly (.github/dependabot.yml)](#-weekly-githubdependabotyml)
- [🧰 Tools — what each one is for](#-tools--what-each-one-is-for)
- [✍️ Writing a new test](#️-writing-a-new-test)

---

## 🪞 Where tests live: a mirror of the repo

Like `src/main` ↔ `src/test` in a Java service, `tests/` mirrors the files it tests. Find a file, and its test is at the same path under `tests/`:

| Source | Test |
|---|---|
| `scripts/build.py` | `tests/scripts/test_build.py` |
| `scripts/check_leaks.py` | `tests/scripts/test_check_leaks.py` |
| `scripts/check_parity.py` | `tests/scripts/test_check_parity.py` |
| `scripts/dry_run.py` | `tests/scripts/test_dry_run.py` |
| `scripts/sync_skill_assets.py` | `tests/scripts/test_sync_skill_assets.py` |
| `scripts/validate_skills.py` | `tests/scripts/test_validate_skills.py` |
| `skills/foundations/cloud-workspace/scripts/render_doc.py` | `tests/skills/foundations/cloud-workspace/scripts/test_render_doc.py` |
| `skills/foundations/cloud-workspace/scripts/build_sheet.py` | `tests/skills/foundations/cloud-workspace/scripts/test_build_sheet.py` |
| `skills/foundations/cloud-workspace/scripts/make_bundle.py` | `tests/skills/foundations/cloud-workspace/scripts/test_make_bundle.py` |
| `skills/<category>/<skill>/SKILL.md` (+ its `.md` files) | `tests/skills/<category>/<skill>/test_skill.py` |
| `skills/software-engineering/create-adr/` · `service-handoff/` | `tests/skills/software-engineering/<skill>/test_skill.py` |
| `skills/career-management/career-hub-toolkit/INTERVIEW.md` | `tests/skills/career-management/career-hub-toolkit/test_interview.py` |
| `templates/career-management/*` | `tests/templates/career-management/test_documents.py`, `test_bundle.py`, `test_ladder_assessment_sheet.py` |
| `.claude-plugin/`, `.cursor-plugin/` | `tests/plugin-manifests/test_manifests.py` |
| `evals/<case>/` | `tests/evals/test_cases.py` |

`tests/test_repo_layout.py` **enforces the mirror**: a new script without `tests/<same path>/test_<name>.py`, or a new skill without `tests/skills/<category>/<skill>/test_skill.py`, fails CI. A test whose source was deleted fails too. Generated copies (bundled into `career-hub-toolkit`) are covered by their source's tests plus the sync check.

Shared helpers: `tests/helpers.py` (paths, `load_script`, `assert_skill_contract`). Fixtures: `tests/conftest.py`.

## 🎚️ Test levels (pytest markers)

Every test declares exactly what kind it is — a test without a marker is rejected at collection time.

| Marker | What it checks | Speed |
|---|---|---|
| `unit` | One function or script in isolation (rendering, tokens, leak rules, parity rules, validation rules), including failure cases on a temporary copy of the repo | seconds |
| `contract` | The promises the skills make: frontmatter, links between skill files, the exact interview questions in EN + pt-BR, template rules (one ℹ️ per doc, back-link to the hub, known placeholders, Growth/Focus banners, bi-weekly block), sheet spec tokens and portable formulas, manifests, eval cases, the mirror layout | seconds |
| `e2e` | Whole flows: the dry run of `/career-hub-toolkit` (4 personas × self/lead × EN/pt-BR × Files/Manual = 32 hubs) and the release build (Manual Kits, `.skill` files) | ~10 s |
| `libreoffice` | Opens the generated spreadsheet in LibreOffice, recalculates every formula and checks expectations by level, gaps, flags and readiness — in both languages | ~30 s |

```bash
make install            # dev dependencies + pre-commit hooks
make test               # unit + contract, with coverage (gate: 80%)
make e2e                # end-to-end
make sheets             # spreadsheet formulas (needs LibreOffice)
make check              # everything CI runs, in order
```

## 🚦 The CI/CD sequence

### 🔀 On every pull request (`.github/workflows/ci.yml`)

Stages run in order and stop at the first failure, cheapest first:

```text
lint ──► consistency ──► tests ──┬─► e2e ──► security ──┐
                                  └─► sheets ────────────┴─► evals (label: run-evals)
```

| # | Stage | Steps | Why it's there |
|---|---|---|---|
| 1 | **lint** | `ruff check`, `ruff format --check`, `yamllint`, `markdownlint-cli2`, `actionlint` | Style and broken YAML/Markdown/workflows caught in seconds |
| 2 | **consistency** | `sync_skill_assets.py --check`, `validate_skills.py`, `check_parity.py` | Bundled copies match sources; every skill listed and named right; EN and pt-BR stay identical in structure |
| 3 | **tests** | `pytest -m "unit or contract"` on Ubuntu, Python 3.12, with the coverage gate | One run of the suite. Ruff already targets Python 3.10, and the scripts have no OS-specific code |
| 4 | **e2e** | `pytest -m e2e`, dry run report, `build.py` → `dist/` artifact | The toolkit still produces complete, linked hubs in every mode, language and fallback |
| 5 | **sheets** | LibreOffice + `pytest -m libreoffice` | Formulas really compute — not just "the cell has a formula" |
| 6 | **security** | `check_leaks.py` on repo **and** `dist/` (denylist from the `LEAK_DENYLIST` secret), `gitleaks` | Nothing points to an employer; no secrets committed |
| 7 | **evals** *(opt-in)* | `claude plugin eval . --tag smoke` | The skills still *behave*: fire, ask before creating, fall back without connectors, report the bi-weekly rhythm |

Add the **`run-evals`** label to a PR that changes how a skill behaves (`skills/**/SKILL.md`, `INTERVIEW.md`, adapters). Evals call a real model, so they cost money and need the `ANTHROPIC_API_KEY` secret.

### 🌙 Nightly (`.github/workflows/nightly.yml`)

- **lychee** — external links in README, docs and skills still work.
- **Full eval suite** — every case, 3 runs each, threshold 0.8.

### 🏷️ On a release tag `v*` (`.github/workflows/release.yml`)

1. Re-runs the whole CI gate (`ci.yml` as a reusable workflow).
2. Checks the tag matches the version in both plugin manifests.
3. Builds `dist/`, leak-checks the built files, publishes the GitHub Release (Manual Kits + `.skill` files).

### 🪝 Before every commit (`.pre-commit-config.yaml`)

ruff, yamllint, markdownlint, gitleaks, the consistency scripts, the local leak check and the fast tests. Install once with `make install`.

### 📅 Weekly (`.github/dependabot.yml`)

Grouped updates for Python packages and GitHub Actions.

## 🧰 Tools — what each one is for

| Tool | Where | Validates | Why this one |
|---|---|---|---|
| **pytest** + markers | stages 3–5 | Scripts, contracts, e2e flows | Standard, fast, markers map 1:1 to CI stages |
| **pytest-cov** | stage 3 | Coverage of every script (gate 80%, currently ~96%) | Catches untested branches in renderers and builders |
| **ruff** (lint + format) | stage 1, pre-commit | Python style and common bugs | One fast tool instead of flake8 + isort + black |
| **yamllint** | stage 1 | Sheet specs, strings, ladders, workflows | YAML drives the spreadsheet and the bundle |
| **markdownlint-cli2** | stage 1 | Skills and docs Markdown | Agents read these files; broken structure = misread instructions |
| **actionlint** | stage 1 | GitHub workflow files | Typos in workflows otherwise only fail after merge |
| **LibreOffice (headless)** | stage 5 | Real formula results in the `.xlsx` | The only free engine that recalculates Excel formulas in CI |
| **check_leaks.py** | stage 6, pre-commit | Employer terms, non-public URLs, emails, document/PDF/image metadata | The repo's core promise; denylist kept outside the repo |
| **gitleaks** | stage 6, pre-commit | Secrets in commits | Cheap insurance for a public repo |
| **`claude plugin eval`** | stage 7, nightly | Agent behavior with the skills (`evals/`) | Unit tests can't see whether the agent follows the skill |
| **lychee** | nightly | External links | Docs point to Claude, Cursor and Google help pages that move |
| **pre-commit** | local | Same checks before pushing | Fewer red PRs |
| **Dependabot** | weekly | Dependency and action updates | Keeps CI green over time |

**Worth adding later**

- **Codecov** (or the GitHub coverage summary) to comment coverage changes on PRs.
- **Promptfoo** as a second, model-agnostic eval runner if you want the same evals against Cursor-style prompts or other models.
- **typos** spell checker, configured with a Portuguese word list, once the docs settle.
- **Renovate** instead of Dependabot if you want auto-merge for safe updates.

## ✍️ Writing a new test

1. Put it at the mirrored path (see [🪞 Where tests live](#-where-tests-live-a-mirror-of-the-repo)). `tests/test_repo_layout.py` tells you if you got it wrong.
2. Mark the module: `pytestmark = pytest.mark.unit` (or `contract`, `e2e`).
3. Use fictional people only — the leak check scans `tests/` too.
4. For failure cases, copy what you need of the repo to `tmp_path` and point the script's `ROOT` at it with `monkeypatch` (see `tests/scripts/test_check_parity.py`).
