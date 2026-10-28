#!/usr/bin/env bash
# Enable APIs + provision infra via Terraform. Run on your machine (needs gcloud+terraform).
set -euo pipefail
PROJECT="${1:?usage: setup_gcp.sh <PROJECT_ID> [REGION]}"
REGION="${2:-us-central1}"

gcloud config set project "$PROJECT"
gcloud auth application-default login

cd "$(dirname "$0")/../terraform"
terraform init
# First pass: enable APIs + registry + DB (images not built yet — use placeholders).
terraform apply \
  -target=google_project_service.enabled \
  -target=google_artifact_registry_repository.repo \
  -target=google_sql_database_instance.pg \
  -target=google_sql_database.lugha \
  -var="project_id=$PROJECT" -var="region=$REGION" \
  -var="web_image=placeholder" -var="api_image=placeholder"
echo "APIs + registry + Cloud SQL ready. Next: scripts/deploy.sh $PROJECT $REGION"
