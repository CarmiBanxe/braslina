"""Tests for merchant status transitions."""

from src.register.db_models import VALID_STATUS_TRANSITIONS, MerchantStatus


def test_new_can_go_to_under_review():
    assert MerchantStatus.UNDER_REVIEW in VALID_STATUS_TRANSITIONS[MerchantStatus.NEW]


def test_new_cannot_go_to_approved():
    assert MerchantStatus.APPROVED not in VALID_STATUS_TRANSITIONS[MerchantStatus.NEW]


def test_under_review_can_approve_or_reject():
    allowed = VALID_STATUS_TRANSITIONS[MerchantStatus.UNDER_REVIEW]
    assert MerchantStatus.APPROVED in allowed
    assert MerchantStatus.REJECTED in allowed


def test_approved_can_suspend():
    assert MerchantStatus.SUSPENDED in VALID_STATUS_TRANSITIONS[MerchantStatus.APPROVED]


def test_approved_cannot_reject():
    assert MerchantStatus.REJECTED not in VALID_STATUS_TRANSITIONS[MerchantStatus.APPROVED]


def test_rejected_can_go_back_to_review():
    assert MerchantStatus.UNDER_REVIEW in VALID_STATUS_TRANSITIONS[MerchantStatus.REJECTED]


def test_suspended_can_go_back_to_review():
    assert MerchantStatus.UNDER_REVIEW in VALID_STATUS_TRANSITIONS[MerchantStatus.SUSPENDED]


def test_all_statuses_have_transition_rules():
    for status in MerchantStatus:
        assert status in VALID_STATUS_TRANSITIONS
