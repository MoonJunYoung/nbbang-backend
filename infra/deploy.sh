#!/usr/bin/env bash
# nbbang-backend: Docker 빌드 → ECR push → Lambda 이미지 업데이트
# 사용법: ./deploy.sh   (또는 infra/deploy.sh)
# 사전 조건: AWS CLI(AWS_PROFILE), Docker

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/config.env"

export AWS_PROFILE AWS_REGION AWS_DEFAULT_REGION="${AWS_REGION}"

ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
IMAGE_URI="${ECR_REGISTRY}/${ECR_REPOSITORY}:${IMAGE_TAG}"
DOCKERFILE="${BACKEND_ROOT}/dockerfile"

require_cmd() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Required command not found: $1" >&2
        exit 1
    fi
}

require_cmd aws
require_cmd docker

if [[ ! -f "${DOCKERFILE}" ]]; then
    echo "Dockerfile not found: ${DOCKERFILE}" >&2
    exit 1
fi

echo "==> AWS identity (profile=${AWS_PROFILE}, region=${AWS_REGION})"
aws sts get-caller-identity --output table

echo "==> Checking Docker daemon"
docker info >/dev/null

echo "==> ECR login: ${ECR_REGISTRY}"
aws ecr get-login-password --region "${AWS_REGION}" \
    | docker login --username AWS --password-stdin "${ECR_REGISTRY}"

echo "==> Building image (linux/arm64): ${IMAGE_URI}"
docker build \
    --platform linux/arm64 \
    -f "${DOCKERFILE}" \
    -t "${IMAGE_URI}" \
    "${BACKEND_ROOT}"

echo "==> Pushing image: ${IMAGE_URI}"
docker push "${IMAGE_URI}"

echo "==> Updating Lambda: ${LAMBDA_FUNCTION_NAME}"
aws lambda update-function-code \
    --function-name "${LAMBDA_FUNCTION_NAME}" \
    --image-uri "${IMAGE_URI}" \
    --query '{FunctionName:FunctionName,LastUpdateStatus:LastUpdateStatus,CodeSha256:CodeSha256}' \
    --output table

echo "==> Waiting for Lambda update to complete..."
aws lambda wait function-updated --function-name "${LAMBDA_FUNCTION_NAME}"

echo "==> Lambda configuration after update"
aws lambda get-function-configuration \
    --function-name "${LAMBDA_FUNCTION_NAME}" \
    --query '{FunctionName:FunctionName,LastUpdateStatus:LastUpdateStatus,State:State,CodeSize:CodeSize,LastModified:LastModified}' \
    --output table

if [[ -n "${HEALTHCHECK_URL}" ]]; then
    echo "==> Healthcheck: ${HEALTHCHECK_URL}"
    HTTP_CODE="$(curl -sS -o /tmp/nbbang-backend-health.json -w '%{http_code}' "${HEALTHCHECK_URL}" || true)"
    echo "    HTTP ${HTTP_CODE}"
    if [[ -f /tmp/nbbang-backend-health.json ]]; then
        cat /tmp/nbbang-backend-health.json
        echo ""
    fi
    if [[ "${HTTP_CODE}" != "200" ]]; then
        echo "Healthcheck failed (expected HTTP 200)." >&2
        exit 1
    fi
fi

cleanup_old_ecr_images() {
    local keep_uri keep_digest digest
    local -a delete_ids=()

    keep_uri="$(aws lambda get-function \
        --function-name "${LAMBDA_FUNCTION_NAME}" \
        --query 'Code.ImageUri' \
        --output text)"
    keep_digest="${keep_uri##*@}"

    if [[ -z "${keep_digest}" || "${keep_digest}" == "${keep_uri}" ]]; then
        echo "Could not resolve Lambda image digest to keep; skipping ECR cleanup." >&2
        return 0
    fi

    echo "==> ECR cleanup: keep ${keep_digest}"
    while IFS= read -r digest; do
        [[ -z "${digest}" || "${digest}" == "${keep_digest}" ]] && continue
        delete_ids+=("imageDigest=${digest}")
    done < <(
        aws ecr describe-images \
            --repository-name "${ECR_REPOSITORY}" \
            --query 'imageDetails[].imageDigest' \
            --output text \
            | tr '\t' '\n'
    )

    if ((${#delete_ids[@]} == 0)); then
        echo "    No old images to delete."
        return 0
    fi

    echo "    Deleting ${#delete_ids[@]} old image(s)..."
    # batch-delete-image accepts up to 100 ids per call
    local start=0 chunk_size=100
    while ((start < ${#delete_ids[@]})); do
        local chunk=("${delete_ids[@]:start:chunk_size}")
        aws ecr batch-delete-image \
            --repository-name "${ECR_REPOSITORY}" \
            --image-ids "${chunk[@]}" \
            --query '{deleted:length(imageIds),failures:failures}' \
            --output table
        start=$((start + chunk_size))
    done
}

if [[ "${CLEANUP_OLD_IMAGES:-false}" == "true" ]]; then
    cleanup_old_ecr_images
fi

echo ""
echo "Done. Deployed ${IMAGE_URI} → ${LAMBDA_FUNCTION_NAME}"
