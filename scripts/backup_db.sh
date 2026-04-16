#!/usr/bin/env bash
set -euo pipefail

# Braslina DB backup script
# Dumps PostgreSQL to timestamped file and uploads to MinIO

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="braslina_backup_${TIMESTAMP}.sql.gz"
BUCKET="braslina-backups"

DB_USER=${POSTGRES_USER:-braslina}
DB_NAME=${POSTGRES_DB:-braslina}
DB_HOST=${DB_HOST:-braslina-db}

MINIO_ALIAS=${MINIO_ALIAS:-local}
MINIO_ENDPOINT=${MINIO_ENDPOINT:-http://braslina-minio:9000}

echo "[$(date)] Starting backup: ${BACKUP_FILE}"

# Dump and compress
docker exec braslina-db pg_dump -U "${DB_USER}" "${DB_NAME}" | gzip > "/tmp/${BACKUP_FILE}"

echo "[$(date)] Dump complete. Size: $(du -h /tmp/${BACKUP_FILE} | cut -f1)"

# Upload to MinIO
mc alias set ${MINIO_ALIAS} ${MINIO_ENDPOINT} ${MINIO_ACCESS_KEY} ${MINIO_SECRET_KEY} 2>/dev/null || true
mc mb --ignore-existing ${MINIO_ALIAS}/${BUCKET}
mc cp "/tmp/${BACKUP_FILE}" "${MINIO_ALIAS}/${BUCKET}/${BACKUP_FILE}"

echo "[$(date)] Uploaded to MinIO: ${BUCKET}/${BACKUP_FILE}"

# Cleanup local
rm -f "/tmp/${BACKUP_FILE}"

# Retain last 30 backups
mc ls ${MINIO_ALIAS}/${BUCKET}/ | sort | head -n -30 | awk '{print $NF}' | while read old; do
  mc rm "${MINIO_ALIAS}/${BUCKET}/${old}"
done

echo "[$(date)] Backup complete."
