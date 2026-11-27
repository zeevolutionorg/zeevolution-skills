# Same stages CI runs (.github/workflows/ci.yml), in the same order.  `make check` before opening a PR.
# markdownlint needs Node >= 22 (`nvm install 22`); CI's action v24 bundles markdownlint-cli2 0.23.2.
# Run when installed, otherwise left to CI: actionlint, LibreOffice (`make sheets` skips), Go (secret scan).
PY ?= python3
MDLINT ?= npx --yes markdownlint-cli2@0.23.2
MD_GLOBS = "*.md" "docs/**/*.md" "skills/**/*.md" "templates/*.md" "!skills/**/assets/**"
GITLEAKS ?= go run github.com/zricethezav/gitleaks/v8@v8.21.2

.PHONY: install lint ruff yamllint markdown actionlint consistency test e2e sheets security check build

install:
	$(PY) -m pip install -r requirements-dev.txt && $(PY) -m pre_commit install

lint: ruff yamllint markdown actionlint

ruff:
	$(PY) -m ruff check . && $(PY) -m ruff format --check .

yamllint:
	$(PY) -m yamllint -c .yamllint.yml .

markdown:
	$(MDLINT) $(MD_GLOBS)

actionlint:
	@if command -v actionlint >/dev/null; then actionlint; else echo "actionlint not installed: skipped here, CI runs it"; fi

consistency:
	$(PY) scripts/sync_skill_assets.py --check && $(PY) scripts/validate_skills.py && $(PY) scripts/check_parity.py

test:
	$(PY) -m pytest -m "unit or contract" --cov --cov-report=term

e2e:
	$(PY) -m pytest -m e2e && $(PY) scripts/dry_run.py --out .out/dry-run && $(PY) scripts/build.py --out dist

sheets:
	$(PY) -m pytest -m libreoffice

security:
	$(PY) scripts/check_leaks.py . dist
	@if command -v go >/dev/null; then $(GITLEAKS) detect --source . --redact; else echo "go not installed: secret scan skipped here, CI runs it"; fi

check: lint consistency test e2e sheets security

build:
	$(PY) scripts/build.py --out dist
