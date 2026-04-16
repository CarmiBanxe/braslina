"""Checklist engine — template loading and evaluation logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

import yaml


class CheckStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    NEEDS_REVIEW = "needs_review"
    NOT_APPLICABLE = "not_applicable"


# Valid transitions: from_status -> set of allowed to_statuses
VALID_TRANSITIONS: dict[CheckStatus, set[CheckStatus]] = {
    CheckStatus.PENDING: {CheckStatus.IN_PROGRESS, CheckStatus.NOT_APPLICABLE},
    CheckStatus.IN_PROGRESS: {CheckStatus.PASSED, CheckStatus.FAILED, CheckStatus.NEEDS_REVIEW},
    CheckStatus.NEEDS_REVIEW: {CheckStatus.PASSED, CheckStatus.FAILED, CheckStatus.IN_PROGRESS},
    CheckStatus.FAILED: {CheckStatus.IN_PROGRESS},
    CheckStatus.PASSED: set(),
    CheckStatus.NOT_APPLICABLE: set(),
}

TEMPLATES_DIR = Path(__file__).parent / "templates"


@dataclass
class ChecklistItem:
    code: str
    label: str
    category: str = ""
    auto_verifiable: bool = False


@dataclass
class ChecklistTemplate:
    template_id: str
    name: str
    version: int
    items: list[ChecklistItem] = field(default_factory=list)


@dataclass
class EvaluationResult:
    total: int = 0
    passed: int = 0
    failed: int = 0
    needs_review: int = 0
    pending: int = 0
    not_applicable: int = 0
    is_complete: bool = False
    is_blocked: bool = False
    completion_pct: float = 0.0


def load_template(template_id: str) -> ChecklistTemplate:
    """Load a checklist template from YAML file."""
    path = TEMPLATES_DIR / f"{template_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Template {template_id} not found at {path}")
    with open(path) as f:
        data = yaml.safe_load(f)
    items = [ChecklistItem(**item) for item in data.get("items", [])]
    return ChecklistTemplate(
        template_id=data["template_id"],
        name=data["name"],
        version=data["version"],
        items=items,
    )


def evaluate(statuses: list[str]) -> EvaluationResult:
    """Evaluate a list of item statuses and return aggregated result."""
    result = EvaluationResult(total=len(statuses))
    for s in statuses:
        status = CheckStatus(s)
        if status == CheckStatus.PASSED:
            result.passed += 1
        elif status == CheckStatus.FAILED:
            result.failed += 1
        elif status == CheckStatus.NEEDS_REVIEW:
            result.needs_review += 1
        elif status == CheckStatus.PENDING:
            result.pending += 1
        elif status == CheckStatus.NOT_APPLICABLE:
            result.not_applicable += 1

    applicable = result.total - result.not_applicable
    result.is_blocked = result.failed > 0
    result.is_complete = applicable > 0 and (result.passed + result.not_applicable) == result.total
    result.completion_pct = round((result.passed / applicable) * 100, 1) if applicable > 0 else 0.0
    return result


def is_valid_transition(current: str, target: str) -> bool:
    """Check if a status transition is allowed."""
    try:
        c = CheckStatus(current)
        t = CheckStatus(target)
    except ValueError:
        return False
    return t in VALID_TRANSITIONS.get(c, set())


# Backward compat alias used by router
SALES_CHECKLIST = load_template("tpl_sales_v1")
