from src.checklist.engine import CheckStatus, ChecklistItem, ChecklistResult, default_merchant_checklist


def test_default_checklist_has_expected_items():
    checklist = default_merchant_checklist()
    assert len(checklist.items) == 8


def test_checklist_not_blocked_when_only_needs_review():
    checklist = default_merchant_checklist()
    assert checklist.is_blocked() is False
    assert len(checklist.review_items()) == 8


def test_checklist_blocked_when_failed_item_present():
    checklist = ChecklistResult(
        items=[
            ChecklistItem("mcc-match", "MCC matches business model", CheckStatus.PASS),
            ChecklistItem("terms-policy", "Terms and policies are present", CheckStatus.FAIL),
        ]
    )
    assert checklist.is_blocked() is True
    assert len(checklist.failed_items()) == 1
