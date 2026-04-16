"""Website Monitor Agent — fallback-safe screenshot capture."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

try:
    from playwright.async_api import async_playwright  # type: ignore
except ImportError:
    async_playwright = None


@dataclass(slots=True)
class ScreenshotJob:
    merchant_id: str
    url: str


def build_storage_path(base_dir: str | Path, merchant_id: str, url: str) -> Path:
    parsed = urlparse(url)
    host = parsed.netloc.replace(":", "_") or "unknown-host"
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    return Path(base_dir) / merchant_id / f"{host}-{ts}.png"


def ensure_parent_dir(path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def create_placeholder_screenshot(path: str | Path, url: str) -> Path:
    path = ensure_parent_dir(path)
    path.write_text(f"placeholder screenshot for {url}\n", encoding="utf-8")
    return path


def run_job(base_dir: str | Path, job: ScreenshotJob) -> Path:
    target = build_storage_path(base_dir=base_dir, merchant_id=job.merchant_id, url=job.url)
    return create_placeholder_screenshot(target, job.url)
