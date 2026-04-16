# Braslina MVP Plan

## Goal

Deliver a working internal bootstrap for merchant onboarding automation that is deployable locally and extensible toward BANXE production workflows.

## Phase 1 — Runtime foundation
- FastAPI app with health endpoint
- Docker Compose stack
- PostgreSQL / Redis / MinIO / n8n services
- Celery app bootstrap
- Environment file template

## Phase 2 — Core domain modules
- Merchant register models
- Checklist engine
- Screenshot storage path logic
- CRM webhook client
- Purchase log module

## Phase 3 — Persistence
- SQLAlchemy engine/session setup
- Base ORM model
- Initial ORM entities for register, checklist, purchases, screenshots

## Phase 4 — Verification
- Basic pytest coverage
- Import/runtime verification
- Health endpoint verification
- Container startup verification

## Phase 5 — First workflow
- Merchant created
- Checklist initialized
- Screenshot captured
- Register updated with review date
- CRM webhook payload generated

## Next phase after MVP
- Real Playwright capture
- Diff detection
- Evidence upload to MinIO
- Alembic migrations
- AuthN/AuthZ
- Backoffice UI
- Full CRM synchronization
