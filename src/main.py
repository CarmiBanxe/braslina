"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.agent.router import router as agent_router
from src.checklist.router import router as checklist_router
from src.crm.router import router as crm_router
from src.purchases.router import router as purchases_router
from src.register.router import router as register_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tables are managed by Alembic
    print("braslina started")
    yield


app = FastAPI(
    title="Braslina - Merchant Onboarding Automation",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(agent_router, prefix="/api/v1/monitor", tags=["Website Monitor"])
app.include_router(checklist_router, prefix="/api/v1/checklist", tags=["Checklist"])
app.include_router(register_router, prefix="/api/v1/onboarding", tags=["Onboarding"])
app.include_router(purchases_router, prefix="/api/v1/test-purchase", tags=["Test Purchase"])
app.include_router(crm_router, prefix="/api/v1/crm", tags=["CRM"])

# Serve admin UI static files
ui_dir = Path(__file__).resolve().parent.parent / "ui"
if ui_dir.exists():
    app.mount("/admin", StaticFiles(directory=str(ui_dir), html=True), name="admin-ui")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "braslina"}
