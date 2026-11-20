#!/usr/bin/env bash
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

if [[ $# -ne 1 ]]; then
    echo "Usage: bash scripts/check-duplication.sh <target-branch-commit>" >&2
    exit 2
fi
base_commit=$(git rev-parse --verify --end-of-options "$1^{commit}")

npx --yes --package @ast-grep/cli@0.51.3 -- ast-grep test --skip-snapshot-tests
npx --yes --package @ast-grep/cli@0.51.3 -- ast-grep scan backend/app/api/routes

npx --yes --package jscpd@5.4.3 -- jscpd backend/app frontend/src \
    --format python,javascript,jsx,typescript,tsx \
    --ignore 'frontend/src/client/**,frontend/src/routeTree.gen.ts' \
    --mode weak --ignore-identifiers=consistent --fail-on-empty \
    --baseline-from-ref "$base_commit" --fail-on-new-clones 0 \
    --reporters console --no-colors --no-tips
