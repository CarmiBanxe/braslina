"""Prometheus metrics for braslina."""
from prometheus_client import Counter, Histogram, Info

# Application info
app_info = Info("braslina", "Braslina application info")
app_info.info({"version": "0.1.0"})

# Business metrics
merchant_created_total = Counter(
    "braslina_merchant_created_total",
    "Total merchants created",
)

checklist_evaluated_total = Counter(
    "braslina_checklist_evaluated_total",
    "Total checklist evaluations",
    ["result"],
)

snapshot_captured_total = Counter(
    "braslina_snapshot_captured_total",
    "Total website snapshots captured",
)

test_purchase_logged_total = Counter(
    "braslina_test_purchase_logged_total",
    "Total test purchases logged",
    ["result"],
)

workflow_advanced_total = Counter(
    "braslina_workflow_advanced_total",
    "Total CRM workflow stage advances",
)

# Latency
request_duration_seconds = Histogram(
    "braslina_request_duration_seconds",
    "Request duration in seconds",
    ["method", "endpoint"],
)
