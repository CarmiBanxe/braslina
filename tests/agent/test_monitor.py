"""Tests for website monitor agent — capture, diff, service."""

import pytest
from unittest.mock import AsyncMock, patch
from pathlib import Path

from src.agent.monitor import ScreenshotResult, _ts, STORAGE_BASE


def test_timestamp_format():
    ts = _ts()
    assert len(ts) == 16  # YYYYMMDDTHHMMSSz
    assert ts.endswith("Z")


def test_screenshot_result_dataclass():
    r = ScreenshotResult(screenshot_path="/tmp/test.png")
    assert r.screenshot_path == "/tmp/test.png"
    assert r.diff_path is None
    assert r.diff_pct is None


def test_screenshot_result_with_diff():
    r = ScreenshotResult(screenshot_path="/a.png", diff_path="/d.png", diff_pct=3.5)
    assert r.diff_pct == 3.5
    assert r.diff_path == "/d.png"


def test_storage_base_is_path():
    assert isinstance(STORAGE_BASE, Path)
