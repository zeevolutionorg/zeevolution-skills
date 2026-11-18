#!/usr/bin/env bash
# Build everything and run every check. Usage: scripts/build.sh
set -euo pipefail
cd "$(dirname "$0")/.."
python3 scripts/sync_skill_assets.py
python3 scripts/validate_skills.py
python3 scripts/check_parity.py
python3 scripts/dry_run.py
python3 scripts/build.py
python3 scripts/check_leaks.py
