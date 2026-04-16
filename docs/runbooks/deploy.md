# Deploy Runbook

## Prerequisites
- SSH access to `banxe@banxe-NucBox-EVO-X2` (Tailscale `100.68.102.48:2222`)
- `.env.prod` configured (copy from `.env.prod.example`)
- Docker and Docker Compose installed

## Steps

### 1. Pull latest code
```bash
cd /opt/braslina
git pull origin main
```

### 2. Build and deploy
```bash
docker compose -f docker-compose.prod.yml build
docker compose -f docker-compose.prod.yml up -d
```

### 3. Run migrations
```bash
docker exec braslina-api alembic upgrade head
```

### 4. Verify
```bash
curl http://localhost:8000/health
# Expected: {"status": "ok", "db": "ok", "redis": "ok", "minio": "ok"}
```

### 5. Check logs
```bash
docker logs braslina-api --tail 50
```

## Rollback
See [rollback.md](./rollback.md)
