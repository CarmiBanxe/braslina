# Braslina Domain Model

## Core aggregates

### MerchantRegisterEntry
Represents the merchant onboarding register row and lifecycle state.

Key fields:
- merchant_id
- legal_name
- website
- desired_mcc
- status
- date_started_work
- next_review_date
- expected_turnover_eur

### ChecklistResult
Represents the onboarding checklist attached to a merchant case.

Key fields:
- items[]
- failed_items()
- review_items()
- is_blocked()

### ChecklistItem
Represents one individual control item.

Key fields:
- code
- label
- status
- notes

### ScreenshotJob
Represents a website monitoring capture request.

Key fields:
- merchant_id
- url

### Purchase log entry
Represents test purchase / refund evidence linked to a merchant.

Expected fields:
- merchant_id
- purchase_date
- amount
- receipt_path
- refund_status
- notes

## Supporting bounded contexts

- Case Management
- Checklist & Rules
- Website Evidence
- Test Purchase Operations
- CRM / Workflow Integration
- Monitoring & Alerts
