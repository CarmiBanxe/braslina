"""Website Monitor Agent — Playwright screenshot + pixelmatch diff.

Falls back to placeholder if Playwright is not installed.
"""

from __future__ import annotations

from collections.abc import MutableSequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

try:
    from playwright.async_api import async_playwright
except ImportError:
    async_playwright = None  # type: ignore[assignment]

try:
    import numpy as np
    from PIL import Image
    from pixelmatch import pixelmatch as _pixelmatch

    HAS_PIXELMATCH = True
except ImportError:
    HAS_PIXELMATCH = False


import os

STORAGE_BASE = Path(os.getenv("BRASLINA_SCREENSHOT_DIR", Path.cwd() / "storage" / "screenshots"))


@dataclass
class ScreenshotResult:
    screenshot_path: str
    diff_path: str | None = None
    diff_pct: float | None = None


@dataclass(slots=True)
class ScreenshotJob:
    merchant_id: str
    url: str
    previous_screenshot_path: str | None = None


def _ts() -> str:
    return datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")


async def _take_screenshot(url: str, dest: Path) -> Path:
    """Take a real screenshot via Playwright, or create placeholder."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if async_playwright is not None:
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page(viewport={"width": 1280, "height": 960})
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.screenshot(path=str(dest), full_page=True)
            await browser.close()
    else:
        dest.write_text(f"placeholder screenshot for {url}\n", encoding="utf-8")
    return dest


def _compute_diff(img_a_path: str, img_b_path: str, diff_out_path: str) -> float:
    """Compute pixel diff percentage between two PNG images."""
    if not HAS_PIXELMATCH:
        return 0.0

    img_a = np.array(Image.open(img_a_path).convert("RGBA"))
    img_b = np.array(Image.open(img_b_path).convert("RGBA"))
    h = min(img_a.shape[0], img_b.shape[0])
    w = min(img_a.shape[1], img_b.shape[1])
    img_a = img_a[:h, :w]
    img_b = img_b[:h, :w]

    flat_a = cast(list[int], img_a.flatten().tolist())
    flat_b = cast(list[int], img_b.flatten().tolist())
    diff_img: MutableSequence[int | float] = cast(MutableSequence[int | float], [0] * len(flat_a))

    num_diff = _pixelmatch(flat_a, flat_b, w, h, diff_img, threshold=0.1)

    diff_arr = np.array(diff_img, dtype=np.uint8).reshape((h, w, 4))
    Image.fromarray(diff_arr, mode="RGBA").save(diff_out_path)

    total = w * h
    return round((num_diff / total) * 100, 2) if total > 0 else 0.0


async def capture_and_diff(
    merchant_id: str,
    url: str,
    previous_screenshot_path: str | None = None,
) -> ScreenshotResult:
    """Capture screenshot and optionally diff against previous."""
    ts = _ts()
    dest = STORAGE_BASE / merchant_id / f"{ts}.png"
    await _take_screenshot(url, dest)

    diff_path = None
    diff_pct = None

    if previous_screenshot_path and Path(previous_screenshot_path).exists():
        diff_dest = STORAGE_BASE / merchant_id / f"{ts}_diff.png"
        diff_pct = _compute_diff(previous_screenshot_path, str(dest), str(diff_dest))
        diff_path = str(diff_dest)

    return ScreenshotResult(
        screenshot_path=str(dest),
        diff_path=diff_path,
        diff_pct=diff_pct,
    )


def run_job(base_dir: str, job: ScreenshotJob) -> Path:
    base = Path(base_dir)
    base.mkdir(parents=True, exist_ok=True)
    ts = _ts()
    dest = base / job.merchant_id / f"{ts}.png"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(f"placeholder screenshot for {job.url}\n", encoding="utf-8")
    return dest
