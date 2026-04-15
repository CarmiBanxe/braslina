"""Braslina — FastAPI application entry point."""

from fastapi import FastAPI

app = FastAPI(
    title="Braslina",
    description="Banxe Merchant Onboarding Automation API",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "braslina"}


# Routers will be added as modules mature:
# from src.agent.router import router as agent_router
# from src.checklist.router import router as checklist_router
# from src.register.router import router as register_router
# from src.purchases.router import router as purchases_router
# app.include_router(agent_router, prefix="/api/v1/agent", tags=["agent"])
# app.include_router(checklist_router, prefix="/api/v1/checklists", tags=["checklists"])
# app.include_router(register_router, prefix="/api/v1/merchants", tags=["merchants"])
# app.include_router(purchases_router, prefix="/api/v1/purchases", tags=["purchases"])
