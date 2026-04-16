"""Tests for CRM workflow transitions and schemas."""
import pytest

from src.crm.db_models import VALID_WORKFLOW_TRANSITIONS, WorkflowStage
from src.crm.schemas import ReminderCreate, WorkflowCreate, WorkflowResponse


# --- Workflow transition tests ---

def test_new_can_go_to_sales_review():
    assert WorkflowStage.SALES_REVIEW in VALID_WORKFLOW_TRANSITIONS[WorkflowStage.NEW]


def test_new_cannot_skip_to_compliance():
    assert WorkflowStage.COMPLIANCE_REVIEW not in VALID_WORKFLOW_TRANSITIONS[WorkflowStage.NEW]


def test_sales_review_can_go_to_compliance_or_rejected():
    allowed = VALID_WORKFLOW_TRANSITIONS[WorkflowStage.SALES_REVIEW]
    assert WorkflowStage.COMPLIANCE_REVIEW in allowed
    assert WorkflowStage.REJECTED in allowed


def test_compliance_review_can_go_to_cards_or_rejected():
    allowed = VALID_WORKFLOW_TRANSITIONS[WorkflowStage.COMPLIANCE_REVIEW]
    assert WorkflowStage.CARDS_REVIEW in allowed
    assert WorkflowStage.REJECTED in allowed


def test_cards_review_can_go_to_pending_approval():
    assert WorkflowStage.PENDING_APPROVAL in VALID_WORKFLOW_TRANSITIONS[WorkflowStage.CARDS_REVIEW]


def test_pending_approval_can_approve_or_reject():
    allowed = VALID_WORKFLOW_TRANSITIONS[WorkflowStage.PENDING_APPROVAL]
    assert WorkflowStage.APPROVED in allowed
    assert WorkflowStage.REJECTED in allowed


def test_approved_is_terminal():
    assert len(VALID_WORKFLOW_TRANSITIONS[WorkflowStage.APPROVED]) == 0


def test_rejected_can_restart():
    assert WorkflowStage.SALES_REVIEW in VALID_WORKFLOW_TRANSITIONS[WorkflowStage.REJECTED]


def test_all_stages_have_transition_rules():
    for stage in WorkflowStage:
        assert stage in VALID_WORKFLOW_TRANSITIONS


# --- Schema tests ---

def test_workflow_create_minimal():
    data = WorkflowCreate(merchant_id="m_test")
    assert data.merchant_id == "m_test"
    assert data.assignee_id is None


def test_reminder_create_validates_channel():
    from pydantic import ValidationError
    with pytest.raises(ValidationError):
        ReminderCreate(
            merchant_id="m_test",
            message="test",
            scheduled_at="2026-01-01T00:00:00",
            channel="sms",
        )
