#!/usr/bin/env bash
set -euo pipefail

case ${1:-} in
    backend|browser|compose) suite=$1; shift ;;
    *) echo "Usage: bash scripts/test-isolated.sh {backend|browser|compose} [test arguments...]" >&2; exit 2 ;;
esac

cd "$(dirname "${BASH_SOURCE[0]}")/.."
project="fullstack-test-$(date +%s)-$$"
compose=(docker compose -p "$project" -f compose.yml -f compose.override.yml -f compose.test.yml)

export POSTGRES_PASSWORD=fullstack-test-postgres
export SECRET_KEY=fullstack-isolated-test-signing-key
export FIRST_SUPERUSER=admin@example.com
export FIRST_SUPERUSER_PASSWORD=fullstack-test-admin
export EMAILS_FROM_EMAIL=tests@example.com
export FASTAPI_ENV=development

trap '"${compose[@]}" down --volumes --remove-orphans --rmi local' EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
"${compose[@]}" up -d --wait --wait-timeout 60 db mailpit

if [[ $suite == backend ]]; then
    db_address=$("${compose[@]}" port db 5432)
    smtp_address=$("${compose[@]}" port mailpit 1025)
    export DATABASE_URL="postgresql://postgres:$POSTGRES_PASSWORD@$db_address/app"
    export SMTP_HOST=127.0.0.1 SMTP_PORT="${smtp_address##*:}" SMTP_TLS=false SMTP_SSL=false
    (
        cd backend
        uv run --locked bash scripts/prestart.sh
        uv run --locked pytest "$@"
    )
else
    "${compose[@]}" build backend
    "${compose[@]}" run --rm --no-deps backend bash scripts/prestart.sh
    "${compose[@]}" up -d --wait --wait-timeout 90 backend

    if [[ $suite == browser ]]; then
        "${compose[@]}" run --rm --no-deps --build playwright bunx playwright test --reporter=line "$@"
    else
        "${compose[@]}" exec -T backend curl -fsS http://localhost:8000/api/v1/utils/health-check/
        "${compose[@]}" exec -T backend curl -fsS -o /dev/null http://localhost:8000/login
    fi
fi
