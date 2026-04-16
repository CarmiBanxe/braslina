# Coding Conventions

## Naming

- Files: snake_case.py
- Classes: PascalCase. DB models end with DB (e.g. MerchantDB)
- Pydantic schemas: {Entity}Create, {Entity}Response, {Entity}Update
- Router functions: create_X, get_X, list_X, update_X, delete_X
- ID prefixes: mer_ (merchant), mcl_ (checklist), chi_ (check item),
  snp_ (snapshot), tpr_ (test purchase), crm_ (workflow), rem_ (reminder)

## Async patterns

- All DB operations are async/await via AsyncSession.
- Never use run_sync except in Alembic env.py.
- Background tasks use Celery, not asyncio.create_task.

## Error handling

- Routers: catch BraslinaError subclasses and translate to HTTP codes.
  - NotFoundError -> 404
  - InvalidStateTransition -> 422
  - ValidationError -> 422
  - DuplicateError -> 409
- Services: raise domain exceptions, never HTTP exceptions.
- Repositories: raise nothing special; let SQLAlchemy errors propagate to services.

## Imports

- Always absolute: from src.common.config import settings
- No circular imports: enforce via module-boundary rules.

## Testing

- Test files mirror src/ structure under tests/.
- Use pytest-asyncio with asyncio_mode = auto.
- Each test that needs DB creates its own data via fixtures; no shared mutable state.

## Git

- Branch: phase/{N}-short-description
- Commit: type(scope): description
  - type: feat | fix | docs | test | refactor | chore
  - scope: phase1 | checklist | monitor | register | crm | ...
