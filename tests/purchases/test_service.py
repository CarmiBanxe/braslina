"""Tests for purchase service — validation, CRUD, summary."""
import pytest
from pydantic import ValidationError as PydanticValidationError

from src.common.exceptions import ValidationError
from src.purchases.schemas import PurchaseCreate, PurchaseSummary
from src.purchases.service import VALID_RESULTS, PurchaseService


# --- Schema validation tests ---

def test_purchase_create_accepts_passed():
    data = PurchaseCreate(
        merchant_id="m_test", amount=10.0, result="passed", performed_by="tester"
    )
    assert data.result == "passed"


def test_purchase_create_accepts_failed():
    data = PurchaseCreate(
        merchant_id="m_test", amount=10.0, result="failed", performed_by="tester"
    )
    assert data.result == "failed"


def test_purchase_create_accepts_partial():
    data = PurchaseCreate(
        merchant_id="m_test", amount=10.0, result="partial", performed_by="tester"
    )
    assert data.result == "partial"


def test_purchase_create_rejects_invalid_result():
    with pytest.raises(PydanticValidationError):
        PurchaseCreate(
            merchant_id="m_test", amount=10.0, result="unknown", performed_by="tester"
        )


def test_purchase_create_rejects_empty_result():
    with pytest.raises(PydanticValidationError):
        PurchaseCreate(
            merchant_id="m_test", amount=10.0, result="", performed_by="tester"
        )


# --- Service validation tests ---

def test_service_valid_results_set():
    assert VALID_RESULTS == {"passed", "failed", "partial"}


def test_service_validate_result_rejects_invalid():
    svc = PurchaseService.__new__(PurchaseService)
    with pytest.raises(ValidationError):
        svc._validate_result("bogus")


def test_service_validate_result_accepts_valid():
    svc = PurchaseService.__new__(PurchaseService)
    for r in VALID_RESULTS:
        svc._validate_result(r)  # should not raise


# --- Summary schema tests ---

def test_summary_schema_all_zeros():
    s = PurchaseSummary(
        merchant_id="m_test", total=0, passed=0, failed=0, partial=0, last_purchase_at=None
    )
    assert s.total == 0
    assert s.last_purchase_at is None


def test_summary_schema_with_counts():
    s = PurchaseSummary(
        merchant_id="m_test", total=5, passed=3, failed=1, partial=1, last_purchase_at=None
    )
    assert s.passed + s.failed + s.partial == s.total
