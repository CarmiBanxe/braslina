# Backup & Restore Runbook

## Automated Daily Backup
Cron job runs `scripts/backup_db.sh` daily at 02:00 UTC.

```crontab
0 2 * * * cd /opt/braslina && ./scripts/backup_db.sh >> /var/log/braslina-backup.log 2>&1
```

## Manual Backup
```bash
cd /opt/braslina
source .env.prod
./scripts/backup_db.sh
```

## List Available Backups
```bash
mc ls local/braslina-backups/
```

## Restore from Backup
```bash
cd /opt/braslina
source .env.prod
./scripts/restore_db.sh braslina_backup_20260417_020000.sql.gz
```

## Verify Restore
```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/onboarding/ | head
```

## Retention Policy
- Last 30 backups are retained
- Older backups are automatically deleted by backup script
