# Module Boundaries

Each module under `src/` owns a single domain. Cross-module communication
goes through services, never through direct DB model imports.

| Module | Owns | Must NOT |
|---|---|---|
| `common` | Config, DB engine, Base, exceptions | Contain business logic |
| `register` | Merchant entity, status lifecycle | Touch checklists or purchases directly |
| `checklist` | Checklist templates, items, evaluation | Modify merchant status |
| `agent` | Screenshots, diffs, snapshots, alerts | Modify checklists or merchant status |
| `purchases` | Test purchase records, summaries | Modify merchant status |
| `crm` | Workflow stages, reminders, notes | Duplicate data owned by other modules |

## File structure per module

src/{module}/
├── _init_.py
├── db_models.py # SQLAlchemy ORM — only model definitions
├── repository.py # DB queries — no business logic
├── service.py # Business logic — no HTTP, no raw SQL
├── router.py # FastAPI routes — no business logic
└── schemas.py # Pydantic request/response models

## Rules

1. Routers call services. Services call repositories. Never skip layers.
2. `HTTPException` only in routers. Services raise domain exceptions from `common/exceptions.py`.
3. Cross-module queries go through the other module's **service**, not its repository.
