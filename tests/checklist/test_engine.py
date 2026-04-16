"""Tests for checklist engine — template loading, evaluation, transitions."""

from src.checklist.engine import (
    evaluate,
    is_valid_transition,
    load_template,
)


def test_load_template_sales_v1():
    tpl = load_template("tpl_sales_v1")
    assert tpl.template_id == "tpl_sales_v1"
    assert tpl.name == "Sales Onboarding Checklist"
    assert len(tpl.items) == 10


def test_load_template_not_found():
    import pytest
    with pytest.raises(FileNotFoundError):
        load_template("nonexistent_template")


def test_evaluate_all_pending():
    result = evaluate(["pending"] * 5)
    assert result.total == 5
    assert result.pending == 5
    assert result.is_complete is False
    assert result.completion_pct == 0.0


def test_evaluate_all_passed():
    result = evaluate(["passed"] * 5)
    assert result.total == 5
    assert result.passed == 5
    assert result.is_complete is True
    assert result.completion_pct == 100.0


def test_evaluate_mixed():
    result = evaluate(["passed", "failed", "pending", "needs_review", "not_applicable"])
    assert result.total == 5
    assert result.passed == 1
    assert result.failed == 1
    assert result.pending == 1
    assert result.needs_review == 1
    assert result.not_applicable == 1
    assert result.is_blocked is True
    assert result.is_complete is False
    # completion_pct = 1 passed / 4 applicable = 25.0
    assert result.completion_pct == 25.0


def test_evaluate_with_not_applicable():
    result = evaluate(["passed", "passed", "not_applicable"])
    assert result.is_complete is True
    assert result.completion_pct == 100.0


def test_valid_transitions():
    assert is_valid_transition("pending", "in_progress") is True
    assert is_valid_transition("pending", "not_applicable") is True
    assert is_valid_transition("in_progress", "passed") is True
    assert is_valid_transition("in_progress", "failed") is True
    assert is_valid_transition("in_progress", "needs_review") is True
    assert is_valid_transition("needs_review", "passed") is True
    assert is_valid_transition("failed", "in_progress") is True


def test_invalid_transitions():
    assert is_valid_transition("pending", "passed") is False
    assert is_valid_transition("passed", "failed") is False
    assert is_valid_transition("passed", "in_progress") is False
    assert is_valid_transition("not_applicable", "pending") is False


def test_invalid_status_value():
    assert is_valid_transition("pending", "garbage") is False
    assert is_valid_transition("garbage", "passed") is False
