# Braslina

Banxe Merchant Onboarding Automation repository.

## Purpose

Braslina is a BANXE internal product for automating merchant onboarding operations around website review, checklist execution, evidence collection, recurring monitoring, and CRM workflow orchestration.

The initial business context comes from the Braslina demo meeting held on 2026-04-15, where the team described a merchant onboarding process involving Sales, IML/Compliance, and Cards teams.

## Core problem

The current process is fragmented across manual website reviews, screenshots with dates, spreadsheets/registers, Google Drive folders, test purchases, refund checks, and cross-team handoffs.

The biggest operational gap identified in the meeting is the lack of reliable, repeatable evidence collection and website-change monitoring.

## Target feature set

- Website Monitor Agent
  - Capture merchant website screenshots on schedule
  - Store timestamped evidence
  - Compare current version with previous baseline
  - Alert when relevant changes are detected

- Merchant Checklist Engine
  - Website review checklist for Sales / Compliance
  - MCC and business model checks
  - Terms and Conditions / Privacy / Refund / Return checks
  - Payment logo and 3DS checks
  - Blocking rules before go-live

- Onboarding Register
  - Merchant onboarding register
  - Date Started Work
  - Status tracking
  - Review cadence
  - Turnover metadata

- CRM Integration
  - Replace spreadsheet-driven reminders and fragmented tracking
  - Route tasks across Sales / IML / Cards
  - Preserve audit trail

- Test Purchase Log
  - Log test purchases
  - Store screenshots, receipts, and refund evidence
  - Track unresolved issues

## Proposed architecture direction

Current preferred technical direction:

- Backend: FastAPI
- Frontend: Next.js
- Database: PostgreSQL
- Object storage: S3 / MinIO
- Browser automation: Playwright
- Workflow orchestration: n8n or Temporal
- Notifications: email / Slack / CRM task queue

## Repository structure

- `docs/spec/` — product and technical specifications
- `docs/meetings/` — structured notes from source meetings
- `docs/screenshots/` — sample evidence or references
- `src/agent/` — website monitoring and evidence automation
- `src/checklist/` — checklist and rule evaluation logic
- `src/crm/` — CRM/workflow integration adapters
- `tests/` — automated tests

## Initial deliverables

1. Feature specification
2. Domain model
3. Workflow/state machine
4. MVP implementation plan
5. Monitoring agent prototype
6. Checklist engine prototype
