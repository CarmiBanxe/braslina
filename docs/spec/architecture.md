# Braslina Architecture

## Purpose

Braslina is an internal BANXE service for merchant onboarding automation. It combines website evidence capture, checklist enforcement, onboarding register management, test purchase logging, and CRM/workflow triggering.

## Main components

- FastAPI API layer
- Checklist engine
- Onboarding register domain
- Website monitor agent
- Purchase evidence log
- CRM webhook integration
- PostgreSQL persistence layer
- Redis + Celery for asynchronous jobs
- MinIO for evidence storage
- n8n for operational workflow orchestration

## Runtime flow

1. API receives merchant onboarding case creation.
2. Register entry is created.
3. Default checklist is initialized.
4. Monitoring job captures website evidence.
5. Evidence metadata is stored.
6. CRM/n8n webhook is triggered for downstream workflow.
7. Periodic review jobs are scheduled via Celery.

## Deployment shape

- `api` — FastAPI application
- `db` — PostgreSQL
- `redis` — queue/cache broker
- `celery-worker` — async job execution
- `celery-beat` — scheduled jobs
- `minio` — object/evidence storage
- `n8n` — workflow automation surface

## Technical notes

Current MVP uses a simplified screenshot placeholder path and basic module boundaries. Playwright-based capture should remain an isolated concern inside the monitoring module so that the rest of the platform stays testable without browser dependencies.
