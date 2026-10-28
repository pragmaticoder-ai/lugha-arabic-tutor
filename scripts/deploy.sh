#!/usr/bin/env bash
# Build + push BOTH images, then deploy two Cloud Run services via Terraform.
set -euo pipefail
PROJECT="${1:?usage: deploy.sh <PROJECT_ID> [REGION]}"
REGION="${2:-us-central1}"
REPO="$REGION-docker.pkg.dev/$PROJECT/lugha"
TAG="$(date +%Y%m%d-%H%M%S)"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"

gcloud config set project "$PROJECT"
gcloud auth configure-docker "$REGION-docker.pkg.dev" -q

# Backend image
gcloud builds submit "$ROOT/backend" --tag "$REPO/lugha-api:$TAG"
# Frontend image
gcloud builds submit "$ROOT/frontend/web-app" --tag "$REPO/lugha-web:$TAG"

cd "$ROOT/terraform"
terraform init
terraform apply \
  -var="project_id=$PROJECT" -var="region=$REGION" \
  -var="api_image=$REPO/lugha-api:$TAG" \
  -var="web_image=$REPO/lugha-web:$TAG"

echo "Deployed. URLs:"
terraform output web_url
terraform output api_url
