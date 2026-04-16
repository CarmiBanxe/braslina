# Rollback Runbook

## When to Rollback
- Health check fails after deploy
- Critical errors in logs
- API returning 500s

## Steps

### 1. Identify the previous working commit
```bash
git log --oneline -10
```

### 2. Checkout previous version
```bash
git checkout <commit-hash>
```

### 3. Rebuild and restart
```bash
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
```

### 4. Rollback migrations if needed
```bash
docker exec braslina-api alembic downgrade -1
```

### 5. Verify
```bash
curl http://localhost:8000/health
```

### 6. Restore database if corrupted
See [backup-restore.md](./backup-restore.md)
