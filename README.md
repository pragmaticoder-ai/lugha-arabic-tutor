# Lugha — Adaptive Arabic Tutor (Monorepo)

Personal adaptive Arabic tutor (self + kids), aligned to the UAE "Arabic as an
Additional Language" framework. Fusha-first; 4 skills (Listening/Speaking/Reading/
Writing); adaptive quiz-driven lesson loop; read-as-a-book Library; gamification.
Mobile-first and responsive.

> Not a hackathon entry — a personal learning build. Monorepo, deployable as
> separate Cloud Run instances for frontend and backend if/when needed.

## Monorepo layout (modeled on arc-mira-retail)
```
frontend/web-app/   Next.js app (mobile-first, responsive, RTL-aware)
backend/app/        FastAPI "brain": adaptive loop + Gemini/TTS/STT calls
terraform/          GCP infra as code (APIs, Cloud Run x2, Cloud SQL, registry, security)
scripts/            setup_gcp.sh, deploy.sh, run_local.sh
specs/              layered specs 00→09 (each: reqs + validations + unit + integration + NFRs)
data/schema/        Postgres schema (learners, progress, schedule, verified lesson bank)
docs/               ARCHITECTURE, DATA_MODEL, DEPLOYMENT, CONTRIBUTING
BRAND-AND-DESIGN.md design system / name / layout / gamification
```

## Deploy as separate instances (frontend + backend)
Two Cloud Run services (`lugha-web`, `lugha-api`) from one repo — see `terraform/`
and `scripts/deploy.sh`. They can scale independently.

## Local dev
```bash
# frontend
cd frontend/web-app && npm install && npm run dev        # http://localhost:3000
# backend
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000
```

## Deploy (needs gcloud + terraform + a GCP project on your machine)
```bash
bash scripts/setup_gcp.sh <PROJECT_ID> <REGION>
bash scripts/deploy.sh    <PROJECT_ID> <REGION>
```
See `docs/DEPLOYMENT.md`. No secrets in this repo — keys stay in Secret Manager / env.
