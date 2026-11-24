#!/usr/bin/env bash
set -euo pipefail

project="${1:?Usage: bash scripts/deploy-docker-compose.sh <project-name>}"
cd "$(dirname "${BASH_SOURCE[0]}")/.."

compose=(docker compose -p "$project" -f compose.yml -f compose.deploy.yml)
"${compose[@]}" config --quiet
"${compose[@]}" build
"${compose[@]}" run --rm backend bash scripts/prestart.sh
"${compose[@]}" up -d --wait
