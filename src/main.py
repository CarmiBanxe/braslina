from fastapi import FastAPI

from src.agent import router as website_monitor
from src.checklist import router as merchant_checklist
from src.register import router as onboarding_register
from src.purchases import router as test_purchase

app = FastAPI(
    title="Braslina — Merchant Onboarding Automation",
    version="0.1.0",
    description="Open-source merchant monitoring & onboarding for BANXE EMI",
)

app.include_router(
    website_monitor.router,
    prefix="/api/v1/website-monitor",
    tags=["Website Monitor"],
)
app.include_router(
    merchant_checklist.router,
    prefix="/api/v1/checklist",
    tags=["Merchant Checklist"],
)
app.include_router(
    onboarding_register.router,
    prefix="/api/v1/onboarding",
    tags=["Onboarding"],
)
app.include_router(
    test_purchase.router,
    prefix="/api/v1/test-purchase",
    tags=["Test Purchase"],
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "braslina"}
