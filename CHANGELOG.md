# Changelog

## [1.0.0] - 2026-04-19

### Added
- Branch protection compliance for `release/1.0.0`
- gitleaks job in CI workflow
- `.gitleaks.toml` + `.gitleaksignore` (exclude `.venv` from secret scan)
- CORS + TrustedHost middleware (production only)
- Structured JSON logging via `setup_logging()`
- HEALTHCHECK in Dockerfile
- Non-root `braslina` user in container
- `BRASLINA_SCREENSHOT_DIR` env var (no more `/app` hardcode)
- minio==7.2.9 in requirements

### Changed
- Auth: dev bypass (`return "dev"`) only when `APP_ENV != production`
- Config: `API_KEY` renamed to `BRASLINA_API_KEY` (aligned with auth)
- Version bump 0.1.0 → 1.0.0 in pyproject.toml + main.py
- CI Python 3.11 → 3.12 (synced with Dockerfile)
- requirements-dev.txt: pinned exact versions
- `print()` → `logger.info()` in lifespan
- `pytest.ini`: asyncio_default_fixture_loop_scope=function

### Fixed
- workflow.py: use `evaluate()` to produce `EvaluationResult`
- engine.py: added `ChecklistResult` alias + `default_merchant_checklist()`
- 15 ruff errors (B904, UP042, I001, F401, UP017)
- E2E test: payload aligned with real schema (name/website/mcc)
- test_api: purchase result `passed`, health accepts `degraded`

### Security
- gitleaks scan: 0 findings on application code
- Compliant with IL-AccessPolicy-01 (`ACCESS-AND-SECRETS.md`)

### QA
- pytest: 52/52 passed
- ruff check src/: All checks passed
- Coverage gate: --cov-fail-under=80
