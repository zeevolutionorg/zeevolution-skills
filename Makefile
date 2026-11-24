# Same commands CI runs, in the same order.  `make check` before opening a PR.
PY ?= python3

.PHONY: install lint consistency test e2e sheets security check build

install:
	$(PY) -m pip install -r requirements-dev.txt && pre-commit install

lint:
	ruff check . && ruff format --check . && yamllint -c .yamllint.yml .

consistency:
	$(PY) scripts/sync_skill_assets.py --check && $(PY) scripts/validate_skills.py && $(PY) scripts/check_parity.py

test:
	$(PY) -m pytest -m "unit or contract" --cov --cov-report=term

e2e:
	$(PY) -m pytest -m e2e

sheets:
	$(PY) -m pytest -m libreoffice

security:
	$(PY) scripts/check_leaks.py

check: lint consistency test e2e sheets security

build:
	$(PY) scripts/build.py --out dist
