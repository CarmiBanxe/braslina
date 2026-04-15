# Merchant Onboarding Automation Feature Spec

## Working title

Braslina Merchant Onboarding Automation

## Background

BANXE currently performs merchant onboarding through a manual process involving website review, merchant questionnaires, checklist completion, screenshots, test purchases, refund verification, and cross-team coordination.

The process is operationally expensive and vulnerable to missing evidence, delayed detection of merchant website changes, and fragmented execution across spreadsheets and folders.

## Product goal

Build an internal automation layer that improves merchant onboarding quality, preserves evidence, reduces manual operational effort, and enables recurring merchant website monitoring after go-live.

## Primary users

- Sales
- IML / Compliance
- Cards / Card Operations
- Internal operations managers
- Future audit / QA reviewers

## Problem statements

### Problem 1 — evidence is fragile

Website screenshots are not always captured, preserved, or easily retrieved.

### Problem 2 — website changes are not monitored reliably

A merchant can materially change the website or business presentation after onboarding, and the team may not detect this quickly enough.

### Problem 3 — onboarding workflow is fragmented

Current process spans forms, folders, spreadsheets, emails, and manual reminders.

### Problem 4 — checklist enforcement is weak

Critical items may be reviewed, but blocking logic and traceability are inconsistent.

## Scope

### In scope

- Merchant onboarding case creation
- Merchant website metadata capture
- Screenshot capture and evidence storage
- Historical comparison of screenshots / website versions
- Checklist execution and statusing
- Assignment of tasks to internal teams
- Merchant onboarding register fields
- Test purchase / refund logging
- Recurring monitoring scheduling
- Alerts for detected website changes
- Audit trail of decisions and evidence

### Out of scope for MVP

- Full merchant self-service portal
- Full card processing integration
- Automated legal conclusioning
- Full AML / sanctions engine replacement
- Turnover anomaly engine beyond basic placeholders

## Functional requirements

### 1. Onboarding case creation

The system must allow creation of a merchant onboarding case with:
- merchant legal name
- merchant website
- desired MCC
- business description
- regions
- expected turnover
- onboarding start date
- responsible teams / owners

### 2. Website evidence capture

The system must:
- capture website screenshots
- timestamp them
- preserve them in storage
- link them to the merchant case
- support multiple captures over time

### 3. Website comparison

The monitoring agent must:
- compare latest capture with previous baseline
- detect meaningful differences
- create an alert when thresholds are exceeded
- attach evidence to the case timeline

### 4. Checklist engine

The checklist engine must support:
- website completeness checks
- policy checks
- merchant identity/contact checks
- payment logo / checkout checks
- MCC/business model review status
- pass / fail / needs-fix statuses
- blocking conditions for go-live

### 5. Test purchase log

The system must allow:
- storing test purchase date
- storing screenshots and receipts
- storing refund request and refund completion status
- linking all evidence to the merchant case

### 6. Onboarding register

The system must maintain:
- merchant status
- Date Started Work
- current onboarding stage
- next review date
- latest evidence status
- latest monitoring status

### 7. Recurring review

The system must support:
- scheduled re-checks
- reminders for periodic reviews
- recurring screenshot captures
- recurring alert generation

## Non-functional requirements

- Full audit trail
- Immutable evidence references
- Role-based access
- Searchable case history
- Human-review-first workflow
- API-first architecture
- Production suitability for internal regulated operations

## Proposed bounded contexts

- Case Management
- Website Evidence
- Checklist & Rules
- Monitoring & Alerts
- CRM / Workflow Integration
- Test Purchase Operations

## Proposed MVP phases

### Phase 1 — foundation
- Case model
- Register fields
- Checklist model
- Evidence storage
- Manual screenshot upload support

### Phase 2 — automation
- Playwright screenshot agent
- Periodic scheduling
- Diff detection
- Alert creation

### Phase 3 — workflow integration
- Task routing
- CRM synchronization
- Escalations and reminders
- Dashboard / reporting

## Open questions

- What is the authoritative source for merchant master data?
- Which team owns final checklist approval?
- What threshold defines a “material website change”?
- Which CRM system should be the system of engagement?
- What evidence retention period is required?
- How should recurring review cadence vary by merchant risk profile?
