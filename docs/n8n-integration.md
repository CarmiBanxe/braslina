# n8n Integration Guide

## Overview

Braslina uses n8n (self-hosted at port 5680) for workflow orchestration.
Two workflows are provided:

1. **Merchant Onboarding** (`merchant_onboarding.json`) - triggered on new merchant creation
2. **Website Monitor Cron** (`website_monitor_cron.json`) - runs on daily schedule

## Setup

### 1. Import Workflows

1. Open n8n at `http://<server-ip>:5680`
2. Go to **Workflows > Import from File**
3. Import `n8n/workflows/merchant_onboarding.json`
4. Import `n8n/workflows/website_monitor_cron.json`

### 2. Configure Credentials

Create an HTTP Request credential in n8n:
- **Name:** `braslina-api`
- **Base URL:** `http://braslina-api:8000` (Docker internal) or `http://localhost:8000`
- **Authentication:** None (Phase 9 will add API key auth)

### 3. Activate Workflows

- **merchant_onboarding**: Set trigger to Webhook mode or Manual
- **website_monitor_cron**: Activate the Schedule Trigger node (daily at 02:00 UTC)

## Webhook Endpoints

The braslina-api provides webhook triggers via `src/crm/webhooks.py`:

| Event | n8n Webhook Path | Payload |
|-------|-----------------|----------|
| Merchant Created | `/webhook/merchant-created` | `{merchant_id, name, website, mcc}` |
| Status Changed | `/webhook/status-changed` | `{merchant_id, old_status, new_status}` |
| Monitor Alert | `/webhook/monitor-alert` | `{merchant_id, diff_pct, diff_url}` |
| Checklist Completed | `/webhook/checklist-completed` | `{merchant_id, checklist_id}` |
| Review Reminder | `/webhook/review-reminder` | `{merchant_id, review_date}` |

## Workflow Nodes

### merchant_onboarding (6 nodes)
1. Schedule Trigger / Webhook
2. HTTP Request: Create merchant via `POST /api/v1/onboarding/`
3. HTTP Request: Evaluate checklist via `POST /api/v1/checklist/evaluate/{merchant_id}`
4. HTTP Request: Capture screenshot via `POST /api/v1/monitor/monitor`
5. HTTP Request: Log test purchase via `POST /api/v1/test-purchase/`
6. HTTP Request: Advance status via `PATCH /api/v1/onboarding/{merchant_id}/status`

### website_monitor_cron
1. Schedule Trigger (daily)
2. HTTP Request: List active merchants
3. Loop: For each merchant, call `POST /api/v1/monitor/monitor`
4. IF: Check if alert triggered
5. HTTP Request: Send alert webhook

## Verification

```bash
# Test merchant onboarding workflow manually
curl -X POST http://localhost:5680/webhook/merchant-created \
  -H 'Content-Type: application/json' \
  -d '{"merchant_id": "m_test", "name": "Test Shop", "website": "https://example.com"}'
```

## Troubleshooting

- Check n8n execution log at `http://<server-ip>:5680/executions`
- Ensure braslina-api is reachable from n8n container (same Docker network)
- Redis must be running for n8n queue mode
