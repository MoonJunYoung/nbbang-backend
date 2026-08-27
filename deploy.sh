#!/usr/bin/env bash
# nbbang-backend 배포 진입점
# 사용법: ./deploy.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "${SCRIPT_DIR}/infra/deploy.sh" "$@"
