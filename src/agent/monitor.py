"""Website Monitor Agent — Playwright screenshots + pixelmatch diff."""

from __future__ import annotations

import asyncio
from pathlib import Path

from playwright.async_api import async_playwright


async def capture_screenshot(url: str, output_path: Path) -> Path:
    """Take a full-page screenshot of *url* and save to *output_path*."""
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})
        await page.goto(url, wait_until="networkidle", timeout=30_000)
        await page.screenshot(path=str(output_path), full_page=True)
        await browser.close()
    return output_path


def compare_screenshots(
    baseline: Path,
    current: Path,
    diff_out: Path,
    threshold: float = 0.1,
) -> dict:
    """Pixel-level comparison using pixelmatch. Returns diff stats."""
    from PIL import Image
    import numpy as np
    from pixelmatch import pixelmatch

    img1 = np.array(Image.open(baseline).convert("RGBA"))
    img2 = np.array(Image.open(current).convert("RGBA"))
    h, w = img1.shape[:2]

    # resize if dimensions differ
    if img2.shape[:2] != (h, w):
        img2 = np.array(Image.open(current).convert("RGBA").resize((w, h)))

    diff = np.zeros_like(img1)
    mismatch = pixelmatch(img1, img2, w, h, diff, threshold=threshold)
    total = w * h
    pct = round(mismatch / total * 100, 2)

    Image.fromarray(diff).save(diff_out)
    return {
        "mismatch_pixels": mismatch,
        "total_pixels": total,
        "diff_pct": pct,
        "diff_path": str(diff_out),
    }


async def monitor_merchant(
    merchant_id: str,
    url: str,
    storage_dir: Path,
    alert_threshold_pct: float = 5.0,
) -> dict:
    """Full monitoring cycle: screenshot → compare → alert decision."""
    storage_dir.mkdir(parents=True, exist_ok=True)
    baseline = storage_dir / f"{merchant_id}_baseline.png"
    current = storage_dir / f"{merchant_id}_current.png"
    diff_path = storage_dir / f"{merchant_id}_diff.png"

    await capture_screenshot(url, current)

    if not baseline.exists():
        current.rename(baseline)
        return {"merchant_id": merchant_id, "action": "baseline_created"}

    result = compare_screenshots(baseline, current, diff_path)
    result["merchant_id"] = merchant_id
    result["alert"] = result["diff_pct"] > alert_threshold_pct

    # rotate: current becomes new baseline
    current.replace(baseline)
    return result


if __name__ == "__main__":
    res = asyncio.run(
        monitor_merchant(
            merchant_id="demo_001",
            url="https://example.com",
            storage_dir=Path("storage/screenshots"),
        )
    )
    print(res)
