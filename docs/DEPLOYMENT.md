# Lugha — Deployment

Prereqs on YOUR machine: `gcloud`, `terraform`, Docker (or Cloud Build), a GCP project.

## 1. One-time setup
```bash
bash scripts/setup_gcp.sh <PROJECT_ID> <REGION>   # enables APIs, registry, Cloud SQL
```

## 2. Deploy (builds + pushes both images, applies Terraform)
```bash
bash scripts/deploy.sh <PROJECT_ID> <REGION>
# prints lugha-web URL (open on phone) and lugha-api URL
```

## 3. Load the DB schema
```bash
# via Cloud SQL connection (psql) — one time
psql "<cloud-sql-connection>" -f data/schema/schema.sql
```

## Separate instances
`terraform/cloud_run.tf` defines TWO services (lugha-web, lugha-api) — redeploy or
scale either independently. lugha-web gets the api URL via NEXT_PUBLIC_API_BASE.

## Mobile
lugha-web is mobile-first (viewport meta, bottom tab bar, responsive container,
44px tap targets). Open the web URL on a phone; it responds. A native wrapper
(Capacitor/Expo) is a later option if an app-store presence is wanted.

## Secrets
None in repo. DB password → Secret Manager; Gemini/TTS/STT use the Cloud Run
service account (ADC). Never commit `.env` or service-account JSON.

## Cost note
Smallest DB tier (db-f1-micro) + scale-to-low Cloud Run for family use. Vertex/TTS
billed per call — pennies at family scale; don't call the model per keystroke.
```
